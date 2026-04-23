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


def availability_dataframe(facts: Iterable[Fact], spaces: Sequence[str], slots: Sequence[str]) -> pd.DataFrame:
    rows = []
    facts = set(facts)

    for space in spaces:
        row = {"Espacio": space}
        for slot in slots:
            if ("Reservada", space) in facts:
                # Este caso no debería ocurrir con la convención actual.
                status = "Reservada"
            elif filter_facts(facts, "Reservada", space, None, slot):
                status = "Reservada"
            elif ("Ocupada", space, slot) in facts:
                status = "Ocupada"
            elif ("Libre", space, slot) in facts:
                status = "Libre"
            else:
                status = "Desconocido"
            row[slot] = STATUS_TO_EMOJI[status]
        rows.append(row)

    return pd.DataFrame(rows)


def comparison_dataframe(results_v1: List[dict], results_v2: List[dict]) -> pd.DataFrame:
    rows = []
    for r1, r2 in zip(results_v1, results_v2):
        case_name = r1["case_name"]
        rows.append(
            {
                "Caso": case_name,
                "KB_v1_asignables": r1["assignable_count"],
                "KB_v2_asignables": r2["assignable_count"],
                "KB_v1_recomendables": r1["recommendable_count"],
                "KB_v2_recomendables": r2["recommendable_count"],
            }
        )
    return pd.DataFrame(rows).set_index("Caso")
