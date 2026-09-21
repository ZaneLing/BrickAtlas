"""Two independent connected-component implementations; no generator imports."""
from collections import deque


def component_sets(nodes, edges, remove=None):
    vertices = set(nodes)
    if len(vertices) != len(nodes):
        raise ValueError("Repeated node")
    if remove is not None and remove not in vertices:
        raise ValueError("Target missing")
    allowed = vertices - {remove}
    adjacency = {n: set() for n in allowed}
    for edge in edges:
        if len(edge) != 2 or any(n not in vertices for n in edge):
            raise ValueError("Edge endpoint outside node list")
        a, b = edge
        if a in allowed and b in allowed:
            adjacency[a].add(b)
            adjacency[b].add(a)
    components, unseen = [], set(allowed)
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        q, reached = deque([start]), {start}
        while q:
            for other in sorted(adjacency[q.popleft()]):
                if other in unseen:
                    unseen.remove(other)
                    reached.add(other)
                    q.append(other)
        components.append(sorted(reached))
    return sorted(components)


def component_count_union_find(nodes, edges, remove=None):
    # Independently constructs and validates a disjoint-set forest.
    parent = {}
    for node in nodes:
        if node in parent:
            raise ValueError("Repeated node")
        parent[node] = node
    if remove is not None and remove not in parent:
        raise ValueError("Target missing")
    all_nodes = set(parent)
    parent.pop(remove, None)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    count = len(parent)
    for edge in edges:
        if len(edge) != 2 or edge[0] not in all_nodes or edge[1] not in all_nodes:
            raise ValueError("Invalid edge")
        a, b = edge
        if a == remove or b == remove:
            continue
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            count -= 1
    return count


def graph_stats(nodes, edges, target):
    simple = sorted({tuple(sorted(e)) for e in edges if e[0] != e[1]})
    after = [e for e in simple if target not in e]
    c = len(component_sets(nodes, edges, target))
    union = component_count_union_find(nodes, edges, target)
    if c != union:
        raise ValueError("Independent oracle disagreement")
    c_before = len(component_sets(nodes, edges))
    if c_before != component_count_union_find(nodes, edges):
        raise ValueError("Independent original oracle disagreement")
    return {"n_before": len(nodes), "m_before": len(simple),
            "n_after": len(nodes) - 1, "m_after": len(after),
            "component_count": c, "deficit": len(nodes) - 1 - c,
            "components_before": c_before,
            "target_degree": sum(target in e for e in simple),
            "surviving_degree_sequence": sorted(sum(n in e for e in after) for n in nodes if n != target)}


def matched_cycle_fixture():
    nodes = ["t", *"abcdef"]
    star = [["t", n] for n in "abcdef"]
    ring = star + [list(e) for e in ["ab", "bc", "cd", "de", "ef", "fa"]]
    triangles = star + [list(e) for e in ["ab", "bc", "ca", "de", "ef", "fd"]]
    a, b = [graph_stats(nodes, edges, "t") for edges in [ring, triangles]]
    assert a["component_count"] == 1 and b["component_count"] == 2
    for field in ["n_before", "m_before", "target_degree", "surviving_degree_sequence"]:
        assert a[field] == b[field]
    # Repetition, direction and isolated vertices do not alter semantics.
    duplicated = ring + [e[::-1] for e in ring] + [ring[0]]
    assert graph_stats(nodes, duplicated, "t") == a
    assert len(component_sets(nodes + ["isolated"], duplicated, "t")) == 2
    assert component_count_union_find(nodes + ["isolated"], duplicated, "t") == 2
    return {"purpose": "synthetic implementation fixture, not corpus data", "a": a, "b": b}
