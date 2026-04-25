from __future__ import annotations

from engine import Rule
from kb_v1 import BASE_FACTS as V1_BASE_FACTS
from kb_v1 import REQUEST_TYPES as V1_REQUEST_TYPES
from kb_v1 import RULES as V1_RULES
from kb_v1 import SLOTS, SPACES


TITLE = "KB V2 - plantilla para extender V1"

# Se agrega un nuevo tipo de solicitud para que la aplicación pueda reconocerlo
# y mostrarlo como opción al usuario.
REQUEST_TYPES = list(V1_REQUEST_TYPES) + ["ReunionAccesible"]


# =========================
# HECHOS NUEVOS AGREGADOS
# =========================
# Se añaden propiedades adicionales a ciertos espacios:
# - Accesible: espacios aptos para personas con movilidad reducida.
# - Centrico: espacios ubicados en una zona conveniente o principal.
EXTRA_FACTS = {
    ("Accesible", "AulaA"),
    ("Accesible", "SalaReuniones"),
    ("Centrico", "AulaA"),
    ("Centrico", "SalaReuniones"),
}


# =========================
# REGLAS NUEVAS KB V2
# =========================
EXTRA_RULES = [

    # ==========================================================
    # R9. HERENCIA DEL NUEVO TIPO DE SOLICITUD
    # ∀g (ReunionAccesible(g) ⇒ ReunionEquipo(g))
    # ----------------------------------------------------------
    # Lógica:
    # Toda solicitud clasificada como ReunionAccesible también
    # debe ser tratada como una ReunionEquipo, heredando así
    # todas las reglas de asignación que ya existían para ese tipo.
    # ==========================================================
    Rule(
        name="R9_reunion_accesible_es_reunion",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("ReunionEquipo", "?g"),
        description=(
            "Toda solicitud de tipo ReunionAccesible hereda las "
            "características y reglas de ReunionEquipo."
        ),
    ),

    # ==========================================================
    # R10. UNA REUNIÓN ACCESIBLE NECESITA ACCESIBILIDAD
    # ∀g (ReunionAccesible(g) ⇒ NecesitaAccesibilidad(g))
    # ----------------------------------------------------------
    # Lógica:
    # Si la reunión fue solicitada como accesible, entonces el
    # motor debe marcarla con el requisito adicional de buscar
    # un espacio con infraestructura accesible.
    # ==========================================================
    Rule(
        name="R10_reunion_accesible_necesita_accesibilidad",
        antecedents=(("ReunionAccesible", "?g"),),
        consequent=("NecesitaAccesibilidad", "?g"),
        description=(
            "Toda reunión accesible requiere que el espacio asignado "
            "cuente con condiciones de accesibilidad."
        ),
    ),

    # ==========================================================
    # R11. RECOMENDACIÓN DE ESPACIOS ACCESIBLES
    # ∀s∀g∀t (Asignable(s,g,t) ∧ NecesitaAccesibilidad(g) ∧ Accesible(s)
    #         ⇒ Recomendable(s,g,t))
    # ----------------------------------------------------------
    # Lógica:
    # Si un espacio ya puede asignarse normalmente y además cumple
    # con la propiedad de ser accesible, entonces pasa a ser una
    # opción recomendada para ese tipo de solicitud.
    # ==========================================================
    Rule(
        name="R11_recomendar_accesible",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("NecesitaAccesibilidad", "?g"),
            ("Accesible", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description=(
            "Un espacio asignable y accesible es recomendable para "
            "solicitudes que requieren accesibilidad."
        ),
    ),

    # ==========================================================
    # R12. RECOMENDACIÓN DE ESPACIOS CÉNTRICOS PARA PRESENTACIONES
    # ∀s∀g∀t (Asignable(s,g,t) ∧ Presentacion(g) ∧ Centrico(s)
    #         ⇒ Recomendable(s,g,t))
    # ----------------------------------------------------------
    # Lógica:
    # Las presentaciones suelen beneficiarse de espacios mejor
    # ubicados o más visibles, por ello si el espacio es céntrico
    # se marca como recomendable.
    # ==========================================================
    Rule(
        name="R12_recomendar_centrico_presentacion",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("Presentacion", "?g"),
            ("Centrico", "?s"),
        ),
        consequent=("Recomendable", "?s", "?g", "?t"),
        description=(
            "Un espacio asignable y céntrico es recomendable para "
            "solicitudes de tipo Presentacion."
        ),
    ),

    # ==========================================================
    # R13. JERARQUÍA DE CAPACIDAD
    # ∀s (CapacidadAlta(s) ⇒ CapacidadMedia(s))
    # ----------------------------------------------------------
    # Lógica:
    # Un espacio con capacidad alta naturalmente puede cubrir
    # también solicitudes de tamaño medio, ampliando sus posibles
    # usos dentro del sistema experto.
    # ==========================================================
    Rule(
        name="R13_capacidad_alta_implica_media",
        antecedents=(("CapacidadAlta", "?s"),),
        consequent=("CapacidadMedia", "?s"),
        description=(
            "Todo espacio de capacidad alta también satisface "
            "requerimientos de capacidad media."
        ),
    ),

    # ==========================================================
    # R14. PRESENTACIONES GRANDES SON DE ALTA PRIORIDAD
    # ∀g (PresentacionGrande(g) ⇒ AltaPrioridad(g))
    # ----------------------------------------------------------
    # Lógica:
    # Se define que una presentación grande debe ser tratada como
    # una solicitud importante, para que el motor le dé preferencia
    # en la recomendación de mejores espacios.
    # ==========================================================
    Rule(
        name="R14_prioridad_presentacion",
        antecedents=(("PresentacionGrande", "?g"),),
        consequent=("AltaPrioridad", "?g"),
        description=(
            "Las presentaciones grandes se consideran solicitudes "
            "de alta prioridad."
        ),
    ),

    # ==========================================================
    # R15. ESPACIOS ALTAMENTE RECOMENDABLES PARA ALTA PRIORIDAD
    # ∀s∀g∀t (Asignable(s,g,t) ∧ AltaPrioridad(g)
    #         ⇒ AltamenteRecomendable(s,g,t))
    # ----------------------------------------------------------
    # Lógica:
    # Cuando una solicitud tiene alta prioridad, cualquier espacio
    # que cumpla con asignabilidad se eleva de recomendable normal
    # a altamente recomendable para ser mostrado primero.
    # ==========================================================
    Rule(
        name="R15_preferir_prioridad",
        antecedents=(
            ("Asignable", "?s", "?g", "?t"),
            ("AltaPrioridad", "?g"),
        ),
        consequent=("AltamenteRecomendable", "?s", "?g", "?t"),
        description=(
            "Los espacios asignables para solicitudes de alta prioridad "
            "se clasifican como altamente recomendables."
        ),
    ),

    # ==========================================================
    # R16. PRIORIDAD ESPECIAL PARA EL DIRECTOR
    # ∀s∀t (Solicita(Director1,t) ∧ Libre(s,t)
    #       ⇒ AsignablePrioritario(s,Director1,t))
    # ----------------------------------------------------------
    # Lógica:
    # Si quien realiza la solicitud es el Director1, cualquier espacio
    # libre pasa a considerarse prioritariamente asignable para él,
    # reflejando una política institucional de preferencia.
    # ==========================================================
    Rule(
        name="R16_prioridad_director",
        antecedents=(
            ("Solicita", "Director1", "?t"),
            ("Libre", "?s", "?t"),
        ),
        consequent=("AsignablePrioritario", "?s", "Director1", "?t"),
        description=(
            "El usuario Director1 tiene prioridad institucional "
            "sobre cualquier espacio libre."
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