from __future__ import annotations

from engine import Rule
from kb_v1 import BASE_FACTS as V1_BASE_FACTS
from kb_v1 import REQUEST_TYPES as V1_REQUEST_TYPES
from kb_v1 import RULES as V1_RULES
from kb_v1 import SLOTS, SPACES


TITLE = "KB V2 - plantilla para extender V1"

# Esta lista ya incluye el nuevo tipo de solicitud para que la app lo muestre.
REQUEST_TYPES = list(V1_REQUEST_TYPES) + ["ReunionAccesible"]

EXTRA_FACTS = {
    ("Accesible", "AulaA"),
    ("Accesible", "SalaReuniones"),
    ("Centrico", "AulaA"),
    ("Centrico", "SalaReuniones"),
}



EXTRA_RULES = [
    Rule(
        name="R13_prioridad_presentacion",
        antecedents=(("PresentacionGrande", "?g"),),
        consequent=("AltaPrioridad", "?g"),
    ),

    Rule(
        name="R14_preferir_prioridad",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("AltaPrioridad", "?g"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
    ),

    Rule(
        name="R15_prioridad_director",
        antecedents=(
            ("Solicita", "Director1", "?t"),
            ("Libre", "?s", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "Director1", "?t"),
        description="El usuario Director1 tiene prioridad sobre espacios libres.",
    ),

    Rule(
        name="R16_requiere_continuidad",
        antecedents=(("Requiere2Horas", "?g"),),
        consequent=("NecesitaSlotsConsecutivos", "?g"),
    ),

    ##### Herencia de Reunión Accesible #####
    # ∀𝑔(𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑙𝑒(𝑔)⇒𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐸𝑞𝑢𝑖𝑝𝑜(𝑔))
    Rule(
        name="R9_reunion_accesible_es_reunion",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("ReunionEquipo", "?g"),
        description=(
            "Toda reunión accesible hereda el tipo ReunionEquipo, "
        ),
    ),

    ##### Requisito de Accesibilidad #####
    # ∀𝑔(𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑙𝑒(𝑔) ⇒ 𝑁𝑒𝑐𝑒𝑠𝑖𝑡𝑎𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑖𝑙𝑖𝑑𝑎𝑑(𝑔))
    Rule(
        name="R10_reunion_accesible_necesita_accesibilidad",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("NecesitaAccesibilidad", "?g"),
        description=(
            "Toda reunión accesible requiere que el espacio asignado "
            "cuente con el predicado Accesible."
        ),
    ),

    ##### Recomendación por Accesibilidad #####
    # ∀𝑠∀𝑔∀𝑡(𝐴𝑠𝑖𝑔𝑛𝑎𝑏𝑙𝑒(𝑠,𝑔,𝑡)∧𝑁𝑒𝑐𝑒𝑠𝑖𝑡𝑎𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑖𝑙𝑖𝑑𝑎𝑑(𝑔)∧𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑙𝑒(𝑠)⇒𝑅𝑒𝑐𝑜𝑚𝑒𝑛𝑑𝑎𝑏𝑙𝑒(𝑠,𝑔,𝑡))
    Rule(
        name="R11_recomendar_accesible",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("NecesitaAccesibilidad", "?g"),
            ("Accesible", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description=(
            "Un espacio asignable y accesible es recomendable para solicitudes que necesitan accesibilidad."
        ), 
    ),

    ##### Recomendación por Centralidad en Presentaciones #####
    #∀𝑠∀𝑔∀𝑡(𝐴𝑠𝑖𝑔𝑛𝑎𝑏𝑙𝑒(𝑠,𝑔,𝑡)∧𝑃𝑟𝑒𝑠𝑒𝑛𝑡𝑎𝑐𝑖𝑜𝑛(𝑔)∧𝐶𝑒𝑛𝑡𝑟𝑖𝑐𝑜(𝑠)⇒𝑅𝑒𝑐𝑜𝑚𝑒𝑛𝑑𝑎𝑏𝑙𝑒(𝑠,𝑔,𝑡))
    Rule(
        name="R12_recomendar_centrico_presentacion",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("Presentacion", "?g"),
            ("Centrico", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description=(
            "Un espacio asignable y céntrico es recomendable para solicitudes de tipo Presentacion."
        ),
    ),

    ##### Jerarquia de capacidad (MI MON) #####
        # ∀s  CapacidadAlta(s) ⇒ CapacidadMedia(s)
    Rule(
        name="R13_capacidad_alta_implica_media",
        antecedents=(("CapacidadAlta", "?s"),),
        consequent=("CapacidadMedia", "?s"),
        description=(
            "Todo espacio de capacidad alta también tiene capacidad media, haciéndolo elegible para solicitudes medianas."
        ),
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

