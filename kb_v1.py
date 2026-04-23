from __future__ import annotations

from engine import Rule


TITLE = "KB V1 - versión base"

SPACES = ["AulaA", "AulaB", "Biblio1", "SalaReuniones", "AuditorioMini"]
SLOTS = ["h1", "h2", "h3", "h4"]
REQUEST_TYPES = ["EstudioIndividual", "ReunionEquipo", "Presentacion", "PresentacionGrande"]


BASE_FACTS = {
    # Propiedades de espacios
    ("Silenciosa", "Biblio1"),
    ("Silenciosa", "AulaB"),
    ("Colaborativo", "AulaA"),
    ("Colaborativo", "SalaReuniones"),
    ("TieneProyector", "AulaA"),
    ("TieneProyector", "SalaReuniones"),
    ("TieneProyector", "AuditorioMini"),
    ("CapacidadAlta", "AuditorioMini"),

    # Disponibilidad en h1
    ("Libre", "AulaA", "h1"),
    ("Libre", "AulaB", "h1"),
    ("Libre", "Biblio1", "h1"),
    ("Ocupada", "SalaReuniones", "h1"),
    ("Libre", "AuditorioMini", "h1"),

    # Disponibilidad en h2
    ("Libre", "AulaA", "h2"),
    ("Ocupada", "AulaB", "h2"),
    ("Libre", "Biblio1", "h2"),
    ("Libre", "SalaReuniones", "h2"),
    ("Ocupada", "AuditorioMini", "h2"),

    # Disponibilidad en h3
    ("Ocupada", "AulaA", "h3"),
    ("Libre", "AulaB", "h3"),
    ("Libre", "Biblio1", "h3"),
    ("Libre", "SalaReuniones", "h3"),
    ("Libre", "AuditorioMini", "h3"),

    # Disponibilidad en h4
    ("Libre", "AulaA", "h4"),
    ("Libre", "AulaB", "h4"),
    ("Ocupada", "Biblio1", "h4"),
    ("Libre", "SalaReuniones", "h4"),
    ("Libre", "AuditorioMini", "h4"),
}


RULES = [
    Rule(
        name="R1_estudio_individual_requiere_silencio",
        antecedents=(("EstudioIndividual", "?g"),),
        consequent=("RequiereSilencio", "?g"),
        description="Si la solicitud es de estudio individual, entonces requiere silencio.",
    ),
    Rule(
        name="R2_reunion_requiere_colaboracion",
        antecedents=(("ReunionEquipo", "?g"),),
        consequent=("RequiereColaboracion", "?g"),
        description="Si la solicitud es una reunión de equipo, entonces requiere un espacio colaborativo.",
    ),
    Rule(
        name="R3_asignar_estudio",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("RequiereSilencio", "?g"),
            ("Silenciosa", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Un espacio silencioso y libre se puede asignar a estudio individual.",
    ),
    Rule(
        name="R4_asignar_reunion",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("RequiereColaboracion", "?g"),
            ("Colaborativo", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Un espacio colaborativo y libre se puede asignar a una reunión.",
    ),
    Rule(
        name="R5_asignar_presentacion",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("Presentacion", "?g"),
            ("TieneProyector", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Una presentación requiere un espacio libre con proyector.",
    ),
    Rule(
        name="R6_asignar_presentacion_grande",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("PresentacionGrande", "?g"),
            ("TieneProyector", "?s"),
            ("CapacidadAlta", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Una presentación grande requiere un espacio libre con proyector y capacidad alta.",
    ),
    Rule(
        name="R7_recomendar_silencioso",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("Silenciosa", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Si un espacio asignable es silencioso, también es recomendable.",
    ),
    Rule(
        name="R8_recomendar_colaborativo",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("Colaborativo", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Si un espacio asignable es colaborativo, también es recomendable.",
    ),
]


def build_kb() -> dict:
    return {
        "title": TITLE,
        "facts": set(BASE_FACTS),
        "rules": list(RULES),
        "spaces": list(SPACES),
        "slots": list(SLOTS),
        "request_types": list(REQUEST_TYPES),
    }
