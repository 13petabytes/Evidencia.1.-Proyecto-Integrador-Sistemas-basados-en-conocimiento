from __future__ import annotations

from engine import Rule
from kb_v1 import BASE_FACTS as V1_BASE_FACTS
from kb_v1 import REQUEST_TYPES as V1_REQUEST_TYPES
from kb_v1 import RULES as V1_RULES
from kb_v1 import SLOTS, SPACES


TITLE = "KB V2 - plantilla para extender V1"

# Esta lista ya incluye el nuevo tipo de solicitud para que la app lo muestre.
REQUEST_TYPES = list(V1_REQUEST_TYPES) + ["ReunionAccesible",  "ReunionLarga"]


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
    # Hechos para reuniones largas
    ("Consecutivo", "h1", "h2"),
    ("Consecutivo", "h2", "h3"),
    ("Consecutivo", "h3", "h4"),
    ("EsDirector", "Director1"),
    ("Solicita", "Director1", "h1"),
    ("Requiere2Horas", "req2"),
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

    # Jerarquía de capacidad (MI MON) 
        # ∀s  CapacidadAlta(s) ⇒ CapacidadMedia(s)
    Rule(
        name="R13_capacidad_alta_implica_media",
        antecedents=(("CapacidadAlta", "?s"),),
        consequent=("CapacidadMedia", "?s"),
        description="Todo espacio de capacidad alta también tiene capacidad media, haciéndolo elegible para solicitudes medianas.",
    ),

    # Recomendación por prioridad de presentación grande 
    # ∀g (PresentacionGrande(g) ⇒ AltaPrioridad(g))
    Rule(
        name="R14_prioridad_presentacion",
        antecedents=(("PresentacionGrande", "?g"),),
        consequent=("AltaPrioridad", "?g"),
        description=(
            "Las presentaciones grandes tienen alta prioridad."
        ),
    ),

# Recomendación por prioridad de presentación de alta prioridad 
    Rule(
        name="R15_preferir_prioridad",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("AltaPrioridad", "?g"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
        description="Si una solicitud tiene alta prioridad, es altamente recomendable.",
    ),

# Director SIEMPRE es alta prioridad 
    Rule(
        name="R16a_director_es_alta_prioridad",
        antecedents=(
            ("EsDirector", "?g"),
        ),
        consequent=("AltaPrioridad", "?g"),
        description="Los directores siempre tienen alta prioridad.",
    ),

# Prioridad sobre espacios libres 
    Rule(
        name="R16_prioridad_director",
        antecedents=(
            ("Solicita", "?g", "?t"),
            ("EsDirector", "?g"),
            ("Libre", "?s", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "?g", "?t"),
        description="El director tiene prioridad sobre espacios libres.",
    ),

# Prioridad sobre espacios reservados (puede 'robar') 
    Rule(
        name="R17_director_prioridad_reserva",
        antecedents=(
            ("Solicita", "?g", "?t"),
            ("EsDirector", "?g"),
            ("Reservada", "?s", "?otro", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "?g", "?t"),
        description="El director puede tomar espacios reservados por otros.",
    ),

# Todo asignable prioritario cuenta como asignable 
    Rule(
        name="R17a_asignable_prioritario_es_asignable",
        antecedents=(
            ("AsignablePrioritario", "?s", "?g", "?t"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Todo espacio prioritario es asignable.",
    ),

# También es recomendable 
    Rule(
        name="R17b_asignable_prioritario_es_recomendable",
        antecedents=(
            ("AsignablePrioritario", "?s", "?g", "?t"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Todo espacio prioritario es recomendable.",
    ),

# Y altamente recomendable
    Rule(
        name="R17c_prioridad_director_fuerte",
        antecedents=(
            ("AsignablePrioritario", "?s", "?g", "?t"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
        description="Los espacios prioritarios para director son altamente recomendables.",
    ),

    ### Recomendación por continuidad ###
    # ∀g (Requiere2Horas(g) ⇒ NecesitaSlotsConsecutivos(g))
    Rule(
        name="R18_requiere_continuidad",
        antecedents=(("Requiere2Horas", "?g"),),
        consequent=("NecesitaSlotsConsecutivos", "?g"),
        description=("Para toda solicitud que requiere 2 horas, necesita slots consecutivos."),
    ),

    # Abigail

    ### Las reuniones individuales son de capacidad baja ###
    # ∀g  EstudioIndividual(g) ⇒ CapacidadBaja(g)
    Rule(
        name="R19_estudio_requiere_baja",
        antecedents=(("EstudioIndividual", "?g"),),
        consequent=("RequiereCapacidadBaja", "?g"),
    ),

    ### Capacidad Media implica capacidad Baja ###
    # ∀s  CapacidadMedia(s) ⇒ CapacidadBaja(s)
    Rule(
        name="R20_capacidad_media_implica_baja",
        antecedents=(("CapacidadMedia", "?s"),),
        consequent=("CapacidadBaja", "?s"),
        description=(
            "Todo espacio con capacidad media también cumple con capacidad baja."
        ),
    ),

    ### Reunion en equipo requiere capacidad Media ###
    # ∀g  ReunionEquipo(g) ⇒ RequiereCapacidadMedia(g)
    Rule(
        name="R21_reunion_equipo_requiere_media",
        antecedents=(("ReunionEquipo", "?g"),),
        consequent=("RequiereCapacidadMedia", "?g"),
        description=(
            "Toda reunión en equipo requiere al menos un espacio con capacidad media."
        ),
    ),

    ### Toda presentación es de capacidad Media ###
    # ∀g  Presentacion(g) ⇒ CapacidadMedia(g)
    Rule(
        name="R22_presentacion_requiere_media",
        antecedents=(("Presentacion", "?g"),),
        consequent=("RequiereCapacidadMedia", "?g"),
        description=("Toda solicitud de tipo presentación requiere capacidad media."),
    ),

    ### Un espacio con proyector es recomendable ###
    # ∀s∀g∀t (Asignable(s,g, t) ∧ TieneProyector(s) ) ⇒ Recomendable(s,g,t))
    Rule(
        name="R22_recomendar_tiene_proyector",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("TieneProyector", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description="Si un espacio tiene proyector, también es recomendable.",
    ),

    ### Reglas de compatibilidad ###
    ### Compatibilidad capacidad media
    Rule(
        name="R24_compatible_capacidad_media",
        antecedents=(
            ("RequiereCapacidadMedia", "?g"),
            ("CapacidadMedia", "?s"),
        ),
        consequent=("CompatibleCapacidad", "?s", "?g"),
        description=(
            "Un espacio es compatible si cumple la capacidad media requerida."
        ),
    ),

    ### Compatibilidad capacidad baja
    Rule(
        name="R25_compatible_capacidad_baja",
        antecedents=(
            ("RequiereCapacidadBaja", "?g"),
            ("CapacidadBaja", "?s"),
        ),
        consequent=("CompatibleCapacidad", "?s", "?g"),
        description=(
            "Un espacio es compatible si cumple la capacidad baja requerida."),
    ),

    ## Asignación para toda capacidad
    Rule(
        name="R26_asignar_por_capacidad",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("CompatibleCapacidad", "?s", "?g"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description=(
            "Un espacio compatible en capacidad y libre puede asignarse."
        ),
    ),

    # Recomendación por capacidad
    Rule(
        name="R27_recomendar_capacidad_justa",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("CompatibleCapacidad", "?s", "?g"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
    ),

    ### Reglas para la asignación por tiempo
    # Si dos slots consecutivos están libres, se genera un slot largo
    Rule(
        name="R28_generar_slot_largo",
        antecedents=(
            ("Libre", "?s", "?t1"),
            ("Libre", "?s", "?t2"),
            ("Consecutivo", "?t1", "?t2"),
        ),
        consequent=("LibreLargo", "?s", "?t1"),
        description=(
            "Si dos franjas consecutivas están libres, se genera un slot largo."
        ),
    ),
    # Reuniones largas requieren slots largos
    Rule(
        name="R29_reunion_larga_usa_slot_largo",
        antecedents=(
            ("ReunionLarga", "?g"),
            ("Solicita", "?g", "?t"),
        ),
        consequent=("NecesitaSlotLargo", "?g"),
    ),
    # Reuniones largas sólo pueden ser asignadas a slots largos
    Rule(
        name="R30_asignar_reunion_larga",
        antecedents=(
            ("NecesitaSlotLargo", "?g"),
            ("Solicita", "?g", "?t"),
            ("LibreLargo", "?s", "?t"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description=(
            "Reuniones largas solo se asignan en slots largos disponibles."
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