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
    ("CapacidadMedia", "AulaA"),
    ("CapacidadMedia", "SalaReuniones"),
    ("CapacidadBaja", "AulaB"),
    ("CapacidadBaja", "Biblio1"),
    ("CapacidadAlta", "SalaReuniones"),
    ("CapacidadAlta", "AuditorioMini"),
}

EXTRA_RULES = [

    ##### Herencia de Reunión Accesible #####
    # ∀𝑔(𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑙𝑒(𝑔)⇒𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐸𝑞𝑢𝑖𝑝𝑜(𝑔))
    Rule(
        name="R9_reunion_accesible_es_reunion",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("ReunionEquipo", "?g"),
        description=(
            "Para toda reunión, si es accesible, entonces es una Reunión en Equipo."
        ),
    ),

    ##### Requisito de Accesibilidad #####
    # ∀𝑔(𝑅𝑒𝑢𝑛𝑖𝑜𝑛𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑙𝑒(𝑔) ⇒ 𝑁𝑒𝑐𝑒𝑠𝑖𝑡𝑎𝐴𝑐𝑐𝑒𝑠𝑖𝑏𝑖𝑙𝑖𝑑𝑎𝑑(𝑔))
    Rule(
        name="R10_reunion_accesible_necesita_accesibilidad",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("NecesitaAccesibilidad", "?g"),
        description=(
            "Toda reunión accesible requiere que el espacio asignado sea Accesible."
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
            "Un espacio asignable y céntrico es recomendable para solicitudes de tipo Presentación."
        ),
    ),

    ##### Jerarquía de capacidad (MI MON) #####
        # ∀s  CapacidadAlta(s) ⇒ CapacidadMedia(s)
    Rule(
        name="R13_capacidad_alta_implica_media",
        antecedents=(("CapacidadAlta", "?s"),),
        consequent=("CapacidadMedia", "?s"),
        description="Todo espacio de capacidad alta también tiene capacidad media, haciéndolo elegible para solicitudes medianas.",
    ),

    ### Recomendación por prioridad de presentación grande ###
    # ∀g (PresentacionGrande(g) ⇒ AltaPrioridad(g))
    Rule(
        name="R14_prioridad_presentacion",
        antecedents=(("PresentacionGrande", "?g"),),
        consequent=("AltaPrioridad", "?g"),
        description=(
            "Las presentaciones grandes tienen alta prioridad."
        ),
    ),

    ### Recomendación por prioridad de presentación de alta prioridad ###
    # ∀s∀g∀t(Asignable(s,g,t)∧AltaPrioridad(g)⇒AltamenteRecomendable(s,g,t))
    Rule(
        name="R15_preferir_prioridad",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("AltaPrioridad", "?g"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
        description=("Si una solicitud tiene alta prioridad, es altamente recomendable."),
    ),

    ### Recomendación por prioridad de director ###
    # ∀s∀t(Solicita(Director1,t)∧ Libre(s, t)⇒ AsignablePrioritario(s,Director1,t))
    Rule(
        name="R16_prioridad_director",
        antecedents=(
            ("Solicita", "Director1", "?t"),
            ("Libre", "?s", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "Director1", "?t"),
        description="El usuario Director1 tiene prioridad sobre espacios libres.",
    ),

    ### Recomendación por continuidad ###
    # ∀g (Requiere2Horas(g) ⇒ NecesitaSlotsConsecutivos(g))
    Rule(
        name="R17_requiere_continuidad",
        antecedents=(("Requiere2Horas", "?g"),),
        consequent=("NecesitaSlotsConsecutivos", "?g"),
        description=("Para toda solicitud que requiere 2 horas, necesita slots consecutivos."),
    ),

    # Abigail

    ### Las reuniones individuales son de capacidad baja ###
    # ∀g  EstudioIndividual(g) ⇒ CapacidadBaja(g)
    Rule(
    name="R18_capacidad_alta_implica_media",
    antecedents=(("EstudioIndividual", "?g"),),
    consequent=("CapacidadBaja", "?g"),
    description=(
        "Todo estudio individual es de capacidad baja."
    ),
    ),

    ### Capacidad Media implica capacidad Baja ###
    # ∀s  CapacidadMedia(s) ⇒ CapacidadBaja(s)
    Rule(
        name="R19_capacidad_media_implica_baja",
        antecedents=(("CapacidadMedia", "?s"),),
        consequent=("CapacidadBaja", "?s"),
        description=(
            "Todo espacio con capacidad media también cumple con capacidad baja."
        ),
    ),

    ### Reunion en equipo requiere capacidad Media ###
    # ∀g  ReunionEquipo(g) ⇒ RequiereCapacidadMedia(g)
    Rule(
        name="R20_reunion_equipo_requiere_media",
        antecedents=(("ReunionEquipo", "?g"),),
        consequent=("RequiereCapacidadMedia", "?g"),
        description=(
            "Toda reunión en equipo requiere al menos un espacio con capacidad media."
        ),
    ),

    ### Toda presentación es de capacidad Media ###
    # ∀g  Presentacion(g) ⇒ CapacidadMedia(g)
    Rule(
        name="R21_presentacion_capacidad_media",
        antecedents=(("Presentacion", "?g"),),
        consequent=("CapacidadMedia", "?g"),
        description=(
            "Toda presentación es de capacidad media."
        ),
    ),

    ### Si una solicitud requiere silencio, el espacio debe ser silenciosa ###
    # ∀s∀g∀t (Libre(s,t) ∧ Solicita(g,t) ∧ RequiereSilencio(g) ∧ Silenciosa(s) ⇒ Asignable(s,g,t))
    Rule(
        name="R22_asignable_si_requiere_silencio",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("RequiereSilencio", "?g"),
            ("Silenciosa", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description=(
            "Si una solicitud requiere silencio, solo espacios silenciosos pueden ser asignables."
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

