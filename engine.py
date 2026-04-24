from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple


Fact = Tuple[str, ...]
Substitution = Dict[str, str]


@dataclass(frozen=True)
class Rule:
    name: str
    antecedents: Tuple[Fact, ...]
    consequent: Fact
    description: str = ""


def is_variable(token: str) -> bool:
    return isinstance(token, str) and token.startswith("?")


def fact_to_string(fact: Fact) -> str:
    predicate, *args = fact
    return f"{predicate}({', '.join(args)})"


def theta_to_string(theta: Substitution) -> str:
    if not theta:
        return "{}"
    parts = [f"{var} -> {value}" for var, value in sorted(theta.items())]
    return "{ " + ", ".join(parts) + " }"


def substitute_token(token: str, theta: Substitution) -> str:
    if is_variable(token):
        return theta.get(token, token)
    return token


def substitute_fact(pattern: Fact, theta: Substitution) -> Fact:
    return tuple(substitute_token(token, theta) for token in pattern)


def match_fact(pattern: Fact, fact: Fact, theta: Optional[Substitution] = None) -> Optional[Substitution]:
    if len(pattern) != len(fact):
        return None

    theta = dict(theta or {})

    for pattern_token, fact_token in zip(pattern, fact):
        if is_variable(pattern_token):
            current = theta.get(pattern_token)
            if current is None:
                theta[pattern_token] = fact_token
            elif current != fact_token:
                return None
        else:
            if pattern_token != fact_token:
                return None

    return theta


def _find_substitutions(
    antecedents: Sequence[Fact],
    facts: Sequence[Fact],
    theta: Optional[Substitution] = None,
) -> Iterator[Substitution]:

    theta = dict(theta or {})

    if not antecedents:
        yield theta
        return

    first_antecedent = substitute_fact(antecedents[0], theta)

    for fact in facts:
        new_theta = match_fact(first_antecedent, fact, theta)
        if new_theta is not None:
            yield from _find_substitutions(antecedents[1:], facts, new_theta)


def find_substitutions(antecedents: Sequence[Fact], facts: Iterable[Fact]) -> List[Substitution]:
    ordered_facts = sorted(set(facts))
    return list(_find_substitutions(list(antecedents), ordered_facts, {}))


def forward_chain(
    base_facts: Iterable[Fact],
    rules: Sequence[Rule],
    max_rounds: int = 50,
) -> Tuple[Set[Fact], List[dict]]:

    known_facts: Set[Fact] = set(base_facts)
    trace: List[dict] = []

    rounds = 0
    added_something = True

    while added_something and rounds < max_rounds:
        added_something = False
        ordered_facts = sorted(known_facts)

        for rule in rules:
            substitutions = find_substitutions(rule.antecedents, ordered_facts)
            for theta in substitutions:
                new_fact = substitute_fact(rule.consequent, theta)
                if new_fact not in known_facts:
                    known_facts.add(new_fact)
                    added_something = True
                    trace.append(
                        {
                            "round": rounds + 1,
                            "rule": rule.name,
                            "description": rule.description,
                            "theta": theta_to_string(theta),
                            "derived_fact": fact_to_string(new_fact),
                        }
                    )
        rounds += 1

    return known_facts, trace


def query_facts(facts: Iterable[Fact], predicate: str) -> List[Fact]:
    return sorted(f for f in set(facts) if f[0] == predicate)


def filter_facts(facts: Iterable[Fact], predicate: str, *args: Optional[str]) -> List[Fact]:
    results: List[Fact] = []
    for fact in set(facts):
        if fact[0] != predicate:
            continue
        if len(fact) != len(args) + 1:
            continue
        ok = True
        for value, expected in zip(fact[1:], args):
            if expected is not None and value != expected:
                ok = False
                break
        if ok:
            results.append(fact)
    return sorted(results)


def add_request_facts(base_facts: Iterable[Fact], request_id: str, slot: str, request_type: str) -> Set[Fact]:
    updated = set(base_facts)
    updated.add(("Solicita", request_id, slot))
    updated.add((request_type, request_id))
    return updated


# 🔥 NUEVA FUNCIÓN MEJORADA
def reserve_space(
    base_facts: Iterable[Fact],
    space: str,
    request_id: str,
    slot: str,
    duration: int = 1,
    slots: Optional[List[str]] = None,
) -> Set[Fact]:

    updated = set(base_facts)

    # Si no hay slots definidos, comportamiento original
    if not slots:
        updated.discard(("Libre", space, slot))
        updated.add(("Ocupada", space, slot))
        updated.add(("Reservada", space, request_id, slot))
        return updated

    try:
        start_index = slots.index(slot)
    except ValueError:
        return updated

    selected_slots = slots[start_index:start_index + duration]

    for s in selected_slots:
        updated.discard(("Libre", space, s))
        updated.add(("Ocupada", space, s))
        updated.add(("Reservada", space, request_id, s))

    return updated


def run_request(
    base_facts: Iterable[Fact],
    rules: Sequence[Rule],
    request_id: str,
    slot: str,
    request_type: str,
) -> dict:

    facts_with_request = add_request_facts(base_facts, request_id, slot, request_type)
    closure, trace = forward_chain(facts_with_request, rules)

    assignable = filter_facts(closure, "Asignable", None, request_id, slot)
    recommendable = filter_facts(closure, "Recomendable", None, request_id, slot)

    return {
        "facts_with_request": facts_with_request,
        "closure": closure,
        "trace": trace,
        "assignable": assignable,
        "recommendable": recommendable,
    }