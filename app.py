from __future__ import annotations

import importlib

import streamlit as st

from cases import run_cases
from engine import fact_to_string, reserve_space, run_request
from viz import availability_dataframe, comparison_dataframe


st.set_page_config(page_title="Mini agente lógico", layout="wide")
st.title("Mini agente lógico para asignación de espacios")


def get_kb_module(module_name: str):
    return importlib.import_module(module_name)


def get_base_kb(module_name: str) -> dict:
    module = get_kb_module(module_name)
    return module.build_kb()


def ensure_session_kb(module_name: str):
    session_key = f"facts::{module_name}"
    if session_key not in st.session_state:
        st.session_state[session_key] = set(get_base_kb(module_name)["facts"])
    return session_key


st.sidebar.header("Configuración")
selected_module_name = st.sidebar.radio(
    "Versión de KB",
    options=["kb_v1", "kb_v2"],
    format_func=lambda x: "KB V1" if x == "kb_v1" else "KB V2",
)

kb = get_base_kb(selected_module_name)
session_key = ensure_session_kb(selected_module_name)
current_facts = st.session_state[session_key]
rules = kb["rules"]

reset_col, title_col = st.columns([1, 4])
with reset_col:
    if st.button("Resetear KB"):
        st.session_state[session_key] = set(kb["facts"])
        st.session_state.pop("last_result", None)
        st.rerun()

with title_col:
    st.subheader(kb["title"])

left_col, right_col = st.columns([1.1, 1.2])

with left_col:
    st.markdown("### Disponibilidad actual")
    matrix_df = availability_dataframe(current_facts, kb["spaces"], kb["slots"])
    st.dataframe(matrix_df, hide_index=True, use_container_width=True)

    st.markdown("### Nueva solicitud")
    with st.form("request_form"):
        request_id = st.text_input("ID de solicitud", value="req1")
        slot = st.selectbox("Franja horaria", kb["slots"])
        request_type = st.selectbox("Tipo de solicitud", kb["request_types"])
        submit = st.form_submit_button("Correr inferencia")

    if submit:
        result = run_request(current_facts, rules, request_id, slot, request_type)
        st.session_state["last_result"] = {
            "module_name": selected_module_name,
            "request_id": request_id,
            "slot": slot,
            "request_type": request_type,
            "result": result,
        }

with right_col:
    st.markdown("### Resultado de la inferencia")
    last = st.session_state.get("last_result")

    if last and last["module_name"] == selected_module_name:
        request_id = last["request_id"]
        slot = last["slot"]
        request_type = last["request_type"]
        result = last["result"]

        st.write(f"Solicitud: **{request_type}({request_id})** en **{slot}**")

        assignable_spaces = [fact[1] for fact in result["assignable"]]
        recommendable_spaces = [fact[1] for fact in result["recommendable"]]

        if assignable_spaces:
            st.success("La consulta ∃s Asignable(s, g, t) es verdadera.")
            st.write("**Espacios asignables:**", ", ".join(assignable_spaces))
        else:
            st.error("No se encontró ningún espacio asignable para esta solicitud.")

        if recommendable_spaces:
            st.write("**Espacios recomendables:**", ", ".join(recommendable_spaces))
        else:
            st.write("**Espacios recomendables:** ninguno derivado todavía.")

        st.markdown("#### Reservar")
        if assignable_spaces:
            reserve_cols = st.columns(len(assignable_spaces))
            for col, space in zip(reserve_cols, assignable_spaces):
                with col:
                    if st.button(f"Reservar {space}", key=f"reserve::{selected_module_name}::{space}::{request_id}::{slot}"):
                        updated = reserve_space(current_facts, space, request_id, slot)
                        st.session_state[session_key] = updated
                        st.session_state.pop("last_result", None)
                        st.rerun()

        st.markdown("#### Traza")
        if result["trace"]:
            st.dataframe(result["trace"], hide_index=True, use_container_width=True)
        else:
            st.info("No se derivaron hechos nuevos.")

        with st.expander("Ver todos los hechos de cierre"):
            for fact in sorted(result["closure"]):
                st.write("-", fact_to_string(fact))
    else:
        st.info("Envía una solicitud para ver asignaciones, recomendaciones y traza.")

st.markdown("---")
st.markdown("### Comparación rápida KB V1 vs KB V2")

results_v1 = run_cases("kb_v1")
results_v2 = run_cases("kb_v2")
comparison_df = comparison_dataframe(results_v1, results_v2)
st.bar_chart(comparison_df)

with st.expander("Ver resultados detallados de casos de prueba"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### KB V1")
        st.dataframe(results_v1, hide_index=True, use_container_width=True)
    with col2:
        st.markdown("#### KB V2")
        st.dataframe(results_v2, hide_index=True, use_container_width=True)
