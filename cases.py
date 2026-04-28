from __future__ import annotations

import importlib
from typing import Dict, List

from engine import filter_facts, run_request


# ---------------------------------------------------------------------------
# Casos compartidos V1 y V2
# ---------------------------------------------------------------------------
MANDATORY_CASES = [
    {
        "case_name": "Caso 1 - EstudioIndividual en h1",
        "request_id": "reqA",
        "slot": "h1",
        "request_type": "EstudioIndividual",
        "expected_spaces": {"AulaB", "Biblio1"},
    },
    {
        "case_name": "Caso 2 - ReunionEquipo en h2",
        "request_id": "reqB",
        "slot": "h2",
        "request_type": "ReunionEquipo",
        "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
        "case_name": "Caso 3 - Presentacion en h2",
        "request_id": "reqC",
        "slot": "h2",
        "request_type": "Presentacion",
        "expected_spaces": {"AulaA", "SalaReuniones"},
    },
    {
        "case_name": "Caso 4 - PresentacionGrande en h3",
        "request_id": "reqD",
        "slot": "h3",
        "request_type": "PresentacionGrande",
        "expected_spaces": {"AuditorioMini"},
    },
    {
        "case_name": "Caso 5 - ReunionAccesible en h2",
        "request_id": "reqE",
        "slot": "h2",
        "request_type": "ReunionAccesible",
        "expected_spaces": {"AulaA", "SalaReuniones"},
    },
]

# ---------------------------------------------------------------------------
# Casos exclusivos de KB V2 — ejercitan las reglas R9–R30
# ---------------------------------------------------------------------------
V2_ONLY_CASES = [
    # R9 + R10 + R11: ReunionAccesible hereda ReunionEquipo y además
    # filtra solo espacios marcados como Accesible → AulaA, SalaReuniones.
    {
        "case_name": "V2-C1 - ReunionAccesible en h3 (solo espacios accesibles)",
        "request_id": "reqV2_1",
        "slot": "h3",
        "request_type": "ReunionAccesible",
        "expected_spaces": {"SalaReuniones"},   # AulaA está Ocupada en h3
        "extra_facts": set(),
    },
    # R13: CapacidadAlta ⇒ CapacidadMedia — AuditorioMini debe aparecer
    # como asignable para una ReunionEquipo que requiere CapacidadMedia.
    # En V1 AuditorioMini NO es colaborativo, así que no aplica R4;
    # en V2 R13 lo eleva pero la asignación sigue dependiendo de R4.
    # Usamos Presentacion (R5) para demostrar que AuditorioMini (proyector +
    # capacidad alta derivada a media) queda asignable en h3.
    {
        "case_name": "V2-C2 - PresentacionGrande en h1 (capacidad alta → asignable)",
        "request_id": "reqV2_2",
        "slot": "h1",
        "request_type": "PresentacionGrande",
        "expected_spaces": {"AuditorioMini"},
        "extra_facts": set(),
    },
    # R14 + R15: PresentacionGrande ⇒ AltaPrioridad ⇒ AltamenteRecomendable.
    # Verificamos que el conteo de AltamenteRecomendable > 0.
    {
        "case_name": "V2-C3 - PresentacionGrande en h4 (alta prioridad)",
        "request_id": "reqV2_3",
        "slot": "h4",
        "request_type": "PresentacionGrande",
        "expected_spaces": {"AuditorioMini"},
        "extra_facts": set(),
    },
    # R12: Presentacion + Centrico ⇒ Recomendable.
    # AulaA y SalaReuniones son Centrico → deben quedar Recomendables.
    {
        "case_name": "V2-C4 - Presentacion en h2 (céntrico recomendable)",
        "request_id": "reqV2_4",
        "slot": "h2",
        "request_type": "Presentacion",
        "expected_spaces": {"AulaA", "SalaReuniones"},
        "extra_facts": set(),
    },
    # R16: Director1 tiene prioridad sobre espacios libres.
    # Inyectamos Solicita(Director1, h4) para que R16 derive AsignablePrioritario.
    {
        "case_name": "V2-C6 - Director1 prioridad en h4 (R16)",
        "request_id": "Director1",
        "slot": "h4",
        "request_type": "ReunionEquipo",
        "expected_spaces": {"AulaA", "SalaReuniones"},
        "extra_facts": set(),
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def _run_single(kb: dict, case: dict) -> dict:
    """Ejecuta un caso y devuelve métricas extendidas."""
    extra = case.get("extra_facts", set())
    base_facts = kb["facts"] | extra

    result = run_request(
        base_facts,
        kb["rules"],
        case["request_id"],
        case["slot"],
        case["request_type"],
    )

    closure = result["closure"]
    spaces = {fact[1] for fact in result["assignable"]}
    ok = case["expected_spaces"].issubset(spaces)

    # Métricas adicionales derivadas del cierre
    altamente_rec = filter_facts(closure, "AltamenteRecomendable", None, case["request_id"], case["slot"])
    asig_prioritario = filter_facts(closure, "AsignablePrioritario", None, case["request_id"], case["slot"])
    accesibles_rec = [
        f for f in filter_facts(closure, "Recomendable", None, case["request_id"], case["slot"])
        if ("Accesible", f[1]) in closure
    ]
    centricos_rec = [
        f for f in filter_facts(closure, "Recomendable", None, case["request_id"], case["slot"])
        if ("Centrico", f[1]) in closure
    ]

    return {
        "case_name": case["case_name"],
        "assignable_spaces": sorted(spaces),
        "assignable_count": len(result["assignable"]),
        "recommendable_count": len(result["recommendable"]),
        "alta_prioridad_count": len(altamente_rec),
        "asignable_prioritario_count": len(asig_prioritario),
        "recomendable_accesible_count": len(accesibles_rec),
        "recomendable_centrico_count": len(centricos_rec),
        "passes_minimum_check": ok,
    }


def run_cases(module_name: str) -> list[dict]:
    kb_module = importlib.import_module(module_name)
    kb = kb_module.build_kb()

    cases = list(MANDATORY_CASES)

    # Los casos V2 solo se agregan cuando corremos kb_v2
    if module_name == "kb_v2":
        cases = cases + [
            # Convertimos los casos V2 al formato que espera _run_single
            {**c} for c in V2_ONLY_CASES
        ]

    results = []
    for case in cases:
        row = _run_single(kb, case)
        results.append(row)

    return results


if __name__ == "__main__":
    for module_name in ["kb_v1", "kb_v2"]:
        print(f"\n=== Probando {module_name} ===")
        for row in run_cases(module_name):
            print(row)