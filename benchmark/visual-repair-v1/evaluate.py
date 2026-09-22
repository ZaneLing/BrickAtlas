#!/usr/bin/env python3
"""Independent union-find semantic evaluator for arbitrary submitted repairs."""
import itertools
import json


def components(graph, missing, restored):
    active = set(graph["nodes"]) - (set(missing) - set(restored))
    parent, sizes = {v: v for v in active}, {v: 1 for v in active}

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in graph["edges"]:
        if a in active and b in active:
            ra, rb = root(a), root(b)
            if ra != rb:
                if sizes[ra] < sizes[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                sizes[ra] += sizes[rb]
    labels = {v: root(v) for v in active}
    return labels, sorted((sizes[v] for v in active if parent[v] == v), reverse=True)


def solve(task_input, binding):
    """Uses only public graph/fault input and a supplied binding, never gold."""
    terminals = [*task_input["fixed_terminals"], binding]
    missing = task_input["missing"]
    for cost in range(len(missing) + 1):
        solutions = []
        for restored in itertools.combinations(missing, cost):
            labels, sizes = components(task_input["graph"], missing, restored)
            if all(v in labels for v in terminals) and len({labels[v] for v in terminals}) == 1:
                solutions.append({"restored": sorted(restored), "component_sizes": sizes})
        if solutions:
            return {"bound_terminal": binding, "minimum_cost": cost,
                    "budget_sufficient": cost <= task_input["budget"],
                    "solutions": sorted(solutions, key=lambda s: s["restored"])}
    raise ValueError("No feasible repair in input")


def no_duplicate_keys(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError("duplicate_json_key")
        result[k] = v
    return result


def parse(raw):
    if isinstance(raw, str):
        return json.loads(raw, object_pairs_hook=no_duplicate_keys,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite")))
    if isinstance(raw, dict):
        return raw
    raise ValueError("not_json_object")


def evaluate(task_input, expected_binding, raw, atomic=False):
    result = {"valid": False, "binding_correct": False, "repair_exact": False,
              "feasible": False, "minimal": False, "complete": False,
              "component_results_correct": False, "errors": []}
    try:
        answer = parse(raw)
        if not isinstance(answer, dict):
            raise ValueError("not_json_object")
        required = {"bound_terminal"} if atomic else {
            "bound_terminal", "minimum_cost", "budget_sufficient", "solutions"}
        if set(answer) != required:
            raise ValueError("wrong_fields")
        bound = answer["bound_terminal"]
        if not isinstance(bound, str) or bound not in task_input["candidate_ids"]:
            raise ValueError("unknown_binding")
        result["binding_correct"] = bound == expected_binding
        if atomic:
            result["valid"] = True
            return result
        if type(answer["minimum_cost"]) is not int or answer["minimum_cost"] < 0:
            raise ValueError("invalid_cost")
        if type(answer["budget_sufficient"]) is not bool:
            raise ValueError("invalid_budget_type")
        if not isinstance(answer["solutions"], list) or not answer["solutions"]:
            raise ValueError("missing_solutions")
        restored_sets, sizes_by_set = set(), {}
        for solution in answer["solutions"]:
            if not isinstance(solution, dict) or set(solution) != {"restored", "component_sizes"}:
                raise ValueError("invalid_solution_fields")
            restored, sizes = solution["restored"], solution["component_sizes"]
            if not isinstance(restored, list) or any(not isinstance(v, str) for v in restored):
                raise ValueError("invalid_restored")
            if len(set(restored)) != len(restored):
                raise ValueError("duplicate_vertex")
            if not set(restored) <= set(task_input["missing"]):
                raise ValueError("restore_not_missing")
            key = frozenset(restored)
            if key in restored_sets:
                raise ValueError("duplicate_solution")
            if not isinstance(sizes, list) or any(type(n) is not int or n <= 0 for n in sizes):
                raise ValueError("invalid_component_sizes")
            restored_sets.add(key)
            sizes_by_set[key] = sorted(sizes, reverse=True)
        result["valid"] = True
        truth = solve(task_input, bound)
        expected = {frozenset(s["restored"]): s["component_sizes"] for s in truth["solutions"]}
        terminals = [*task_input["fixed_terminals"], bound]
        feasible, components_ok = True, True
        for restored in restored_sets:
            labels, sizes = components(task_input["graph"], task_input["missing"], restored)
            feasible &= all(v in labels for v in terminals) and len({labels.get(v) for v in terminals}) == 1
            components_ok &= sizes == sizes_by_set[restored]
        result.update({
            "feasible": feasible,
            "minimal": feasible and all(len(s) == truth["minimum_cost"] for s in restored_sets),
            "complete": restored_sets == set(expected),
            "component_results_correct": components_ok,
        })
        checks = {
            "infeasible": result["feasible"],
            "nonminimal": result["minimal"],
            "incomplete_optimum_set": result["complete"],
            "wrong_components": components_ok,
            "wrong_cost": answer["minimum_cost"] == truth["minimum_cost"],
            "wrong_budget": answer["budget_sufficient"] == truth["budget_sufficient"],
            "wrong_binding": result["binding_correct"],
        }
        result["errors"] = [error for error, passed in checks.items() if not passed]
        result["repair_exact"] = not result["errors"]
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        result["errors"] = [str(exc)]
    return result
