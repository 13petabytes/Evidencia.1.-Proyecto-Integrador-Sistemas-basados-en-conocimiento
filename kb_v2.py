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
# Agrega aquí las nuevas reglas de V2.
#
# Sugerencias mínimas:
# 1) ReunionAccesible(g) ==> ReunionEquipo(g)
# 2) ReunionAccesible(g) ==> NecesitaAccesibilidad(g)
# 3) Asignable(s,g,t) & NecesitaAccesibilidad(g) & Accesible(s) ==> Recomendable(s,g,t)
# 4) Asignable(s,g,t) & Presentacion(g) & Centrico(s) ==> Recomendable(s,g,t)
# -------------------------------------------------------------------
EXTRA_RULES = [
    # Ejemplo:
    # Rule(
    #     name="R9_reunion_accesible_es_reunion",
    #     antecedents=(("ReunionAccesible", "?g"),),
    #     consequent=("ReunionEquipo", "?g"),
    #     description="Toda reunión accesible también es una reunión de equipo.",
    # ),
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
