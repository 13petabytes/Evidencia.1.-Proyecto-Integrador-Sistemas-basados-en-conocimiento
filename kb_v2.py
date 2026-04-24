from __future__ import annotations

from engine import Rule
from kb_v1 import BASE_FACTS as V1_BASE_FACTS
from kb_v1 import REQUEST_TYPES as V1_REQUEST_TYPES
from kb_v1 import RULES as V1_RULES
from kb_v1 import SLOTS, SPACES


TITLE = "KB V2 - plantilla para extender V1"

# Esta lista ya incluye el nuevo tipo de solicitud para que la app lo muestre.
REQUEST_TYPES = list(V1_REQUEST_TYPES) + ["ReunionAccesible"]

# -------------------------------------------------------------------
# TODO:
# Agrega aquí los nuevos hechos de V2.
#
# Sugerencia mínima:
# ("Accesible", "AulaA")
# ("Accesible", "SalaReuniones")
# ("Centrico", "AulaA")
# ("Centrico", "SalaReuniones")
# -------------------------------------------------------------------
EXTRA_FACTS = {
    # Ejemplo:
    # ("Accesible", "AulaA"),
}

# -------------------------------------------------------------------
# TODO:

EXTRA_RULES = [
    Rule(
        name="R11_prioridad_presentacion",
        antecedents=(("PresentacionGrande", "?g"),),
        consequent=("AltaPrioridad", "?g"),
    ),

    Rule(
        name="R12_preferir_prioridad",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("AltaPrioridad", "?g"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
    ),

    Rule(
        name="R13_prioridad_director",
        antecedents=(
            ("Solicita", "Director1", "?t"),
            ("Libre", "?s", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "Director1", "?t"),
        description="El usuario Director1 tiene prioridad sobre espacios libres.",
    ),

    Rule(
        name="R14_requiere_continuidad",
        antecedents=(("Requiere2Horas", "?g"),),
        consequent=("NecesitaSlotsConsecutivos", "?g"),
    ),
]


def build_kb() -> dict:
    return {
        "title": TITLE,
        "facts": set(V1_BASE_FACTS) | set(EXTRA_FACTS),
        "rules": list(V1_RULES) + list(EXTRA_RULES),
        "spaces": list(SPACES),
        "slots": list(SLOTS),
        "request_types": list(REQUEST_TYPES),
    }
