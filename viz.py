from __future__ import annotations

from typing import Iterable, List, Sequence

import pandas as pd

from engine import Fact, filter_facts


STATUS_TO_EMOJI = {
    "Libre": "🟩 Libre",
    "Ocupada": "🟥 Ocupada",
    "Reservada": "🟦 Reservada",
    "Desconocido": "⬜ Desconocido",
}


# ---------------------------------------------------------------------------
# Disponibilidad
# ---------------------------------------------------------------------------

def availability_dataframe(
    facts: Iterable[Fact], spaces: Sequence[str], slots: Sequence[str]
) -> pd.DataFrame:
    rows = []
    facts = set(facts)

    for space in spaces:
        row = {"Espacio": space}
        for slot in slots:
            reservada_facts = filter_facts(facts, "Reservada", space, None, slot)
            if reservada_facts:
                # Cambio de código para mostrar ID de la request en la UI
                request_ids = [f[2] for f in reservada_facts]
                row[slot] = f"🟦 Reservada ({', '.join(request_ids)})"
            elif ("Ocupada", space, slot) in facts:
                row[slot] = STATUS_TO_EMOJI["Ocupada"]
            elif ("Libre", space, slot) in facts:
                row[slot] = STATUS_TO_EMOJI["Libre"]
            else:
                row[slot] = STATUS_TO_EMOJI["Desconocido"]
        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Comparación principal V1 vs V2
# ---------------------------------------------------------------------------

def comparison_dataframe(
    results_v1: List[dict], results_v2: List[dict]
) -> pd.DataFrame:
    """
    Compara asignables y recomendables en los casos compartidos (primeros 5).
    Devuelve un DataFrame indexado por caso para st.bar_chart.
    """
    shared_v1 = results_v1[:5]
    shared_v2 = results_v2[:5]

    rows = []
    for r1, r2 in zip(shared_v1, shared_v2):
        rows.append(
            {
                "Caso": r1["case_name"],
                "V1 asignables": r1["assignable_count"],
                "V2 asignables": r2["assignable_count"],
                "V1 recomendables": r1["recommendable_count"],
                "V2 recomendables": r2["recommendable_count"],
            }
        )
    return pd.DataFrame(rows).set_index("Caso")


# ---------------------------------------------------------------------------
# Métricas exclusivas de KB V2
# ---------------------------------------------------------------------------

def v2_metrics_dataframe(results_v2: List[dict]) -> pd.DataFrame:
    """
    DataFrame con las métricas adicionales derivadas de las reglas R9–R22
    para TODOS los casos de V2 (compartidos + exclusivos).
    Útil para una gráfica de barras apiladas o agrupada.
    """
    rows = []
    for r in results_v2:
        rows.append(
            {
                "Caso": r["case_name"],
                "Asignables": r["assignable_count"],
                "Recomendables": r["recommendable_count"],
                "Alta prioridad (R14-R15)": r.get("alta_prioridad_count", 0),
                "Prioritario director (R16)": r.get("asignable_prioritario_count", 0),
                "Rec. accesible (R11)": r.get("recomendable_accesible_count", 0),
                "Rec. céntrico (R12)": r.get("recomendable_centrico_count", 0),
            }
        )
    return pd.DataFrame(rows).set_index("Caso")


def v2_pass_rate_dataframe(results_v2: List[dict]) -> pd.DataFrame:
    """
    DataFrame booleano (0/1) que indica si cada caso de V2 pasa
    la verificación mínima de espacios esperados.
    """
    rows = []
    for r in results_v2:
        rows.append(
            {
                "Caso": r["case_name"],
                "Pasa verificación": int(r["passes_minimum_check"]),
            }
        )
    return pd.DataFrame(rows).set_index("Caso")


def v2_exclusive_summary(results_v2: List[dict]) -> pd.DataFrame:
    """
    Resumen comparativo de los casos exclusivos de V2 (índices 5+).
    Muestra asignables y cada métrica de mejora en columnas separadas.
    """
    exclusive = results_v2[5:]
    if not exclusive:
        return pd.DataFrame()

    rows = []
    for r in exclusive:
        rows.append(
            {
                "Caso V2 exclusivo": r["case_name"],
                "Asignables": r["assignable_count"],
                "Recomendables": r["recommendable_count"],
                "Alta prioridad": r.get("alta_prioridad_count", 0),
                "Rec. accesible": r.get("recomendable_accesible_count", 0),
                "Rec. céntrico": r.get("recomendable_centrico_count", 0),
                "Pasa": r["passes_minimum_check"],
            }
        )
    return pd.DataFrame(rows)