from __future__ import annotations

from engine import Rule, fact_to_string, forward_chain


# Ejemplo diminuto para que los estudiantes vean la mecánica
# antes de meterse en la app completa.

facts = {
    ("Libre", "Sala1", "h1"),
    ("TieneProyector", "Sala1"),
    ("Solicita", "req_demo", "h1"),
    ("Presentacion", "req_demo"),
}

rules = [
    Rule(
        name="toy_presentacion",
        antecedents=(
            ("Libre", "?s", "?t"),
            ("Solicita", "?g", "?t"),
            ("Presentacion", "?g"),
            ("TieneProyector", "?s"),
        ),
        consequent=("Asignable", "?s", "?g", "?t"),
        description="Una presentación necesita un espacio libre con proyector.",
    )
]

if __name__ == "__main__":
    closure, trace = forward_chain(facts, rules)

    print("Hechos derivados:")
    for fact in sorted(closure):
        print("-", fact_to_string(fact))

    print("\nTraza:")
    for step in trace:
        print(step)
