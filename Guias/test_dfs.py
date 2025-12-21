# test_dfs_series.py
# Suite de verificación general para la serie de DFS (pytest).
# Requiere que implementes las funciones en un módulo: dfs_exercises.py
# Si usás otros nombres/firmas, adaptá los imports y llamados.

import math
import itertools as it
import pytest

from dfs_exercises import (
    dfs_times,
    connected_components,
    find_undirected_cycle,
    classify_edges_directed,
    bipartite_or_odd_cycle,
    bridges,
    articulation_points,
    topo_or_cycle,
    #scc_kosaraju,
    #dfs_iter_leaves,
    #path_dfs,
    #euler_orders_tree,
)

# ---------- Utils ----------

def undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def directed(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    return adj

def normalize_edge(u, v=None):
    if v is None:
        u, v = u  # u es la tupla (u,v)
    return (u, v) if u <= v else (v, u)

def is_path(adj, path):
    if not path: return False
    for u, v in zip(path, path[1:]):
        if v not in adj[u]:  # dirigido: usar directed()
            return False
    return True

def cycle_edges(cyc):
    return set(map(normalize_edge, zip(cyc, cyc[1:] + cyc[:1])))

def same_undirected_cycle(c1, c2):
    """Chequea igualdad de ciclos no dirigidos con rotación/inversión."""
    if len(c1) != len(c2): return False
    k = len(c1)
    for shift in range(k):
        if all(c1[i] == c2[(i + shift) % k] for i in range(k)):
            return True
        if all(c1[i] == c2[(shift - i) % k] for i in range(k)):
            return True
    return False

# ---------- 1) dfs_times ----------

def test_dfs_times_basic():
    # Grafo: 0-1-2, 1-3
    adj = undirected(4, [(0,1),(1,2),(1,3)])
    tin, tout, parent = dfs_times(adj, start=0)
    # Alcanzables desde 0
    for v in [0,1,2,3]:
        assert tin[v] > 0 and tout[v] > 0
        assert tin[v] < tout[v]
    # Padre-consistencia: padre de 0 es -1
    assert parent[0] == -1
    for v in [1,2,3]:
        assert parent[v] in adj[v]

# ---------- 2) connected_components ----------

def test_connected_components_multiple():
    # Componentes: {0,1,2}, {3,4}, {5}
    adj = undirected(6, [(0,1),(1,2),(3,4)])
    comps = connected_components(adj)
    comps_sorted = [sorted(c) for c in comps]
    assert sorted(comps_sorted) == [[0,1,2],[3,4],[5]]

# ---------- 3) find_undirected_cycle ----------

def test_find_cycle_triangle_and_square():
    # Triángulo 0-1-2-0 y cola 2-3-4
    adj = undirected(5, [(0,1),(1,2),(2,0),(2,3),(3,4)])
    cyc = find_undirected_cycle(adj)
    assert cyc, "Debe encontrar algún ciclo"
    # Debe ser un conjunto de aristas cerradas y sin repeticiones
    assert len(set(cyc)) == len(cyc)
    edges_in_graph = set(map(normalize_edge, it.chain.from_iterable(
        [ [(u,v)] for u,v in [(0,1),(1,2),(2,0),(2,3),(3,4)] ]
    )))
    assert cycle_edges(cyc).issubset(edges_in_graph)
    # Validar que tenga longitud >= 3
    assert len(cyc) >= 3

def test_find_cycle_none_when_acyclic():
    # Arbol: 0-1, 1-2, 1-3
    adj = undirected(4, [(0,1),(1,2),(1,3)])
    cyc = find_undirected_cycle(adj)
    assert cyc == [], "No debe haber ciclo en un árbol"

# ---------- 4) classify_edges_directed ----------

def test_classify_edges_directed_basic():
    # Grafo dirigido:
    # 0 -> 1 -> 2
    # 0 -> 2
    # 2 -> 3
    # 3 -> 1 (back-edge que forma ciclo)
    adj = directed(4, [(0,1),(1,2),(0,2),(2,3),(3,1)])
    tree, back, forward, cross = classify_edges_directed(adj)
    # Debe haber al menos una back-edge (3->1)
    assert (3,1) in back
    # (0,2) puede ser forward (si 2 es descendiente por 1) o tree según DFS
    # Aceptamos cualquiera, pero su clasificación debe pertenecer a alguna lista:
    all_classified = set(map(tuple, tree + back + forward + cross))
    for e in [(0,1),(1,2),(0,2),(2,3),(3,1)]:
        assert e in all_classified

# ---------- 5) bipartite_or_odd_cycle ----------

def test_bipartite_graph():
    # Bipartito: cuadrado 0-1-2-3-0
    adj = undirected(4, [(0,1),(1,2),(2,3),(3,0)])
    ok, data = bipartite_or_odd_cycle(adj)
    assert ok is True
    color = data
    assert set(color).issuperset({0,1})
    # Cada arista debe conectar colores distintos
    for (u,v) in [(0,1),(1,2),(2,3),(3,0)]:
        assert color[u] != color[v]

def test_non_bipartite_triangle():
    # No bipartito: triángulo
    adj = undirected(3, [(0,1),(1,2),(2,0)])
    ok, data = bipartite_or_odd_cycle(adj)
    assert ok is False
    cyc = data
    assert len(cyc) % 2 == 1  # ciclo impar
    assert len(cyc) >= 3

# ---------- 6) bridges ----------

def test_bridges_basic():
    # 0-1-2-3 con puente (2,3); y 1-4-5 con ciclo 1-4-5-1
    adj = undirected(7, [(0,1),(1,2),(2,3),(1,4),(4,5),(5,1),(2,5)])
    out = set(map(normalize_edge, bridges(adj)))
    # Puentes: (0,1) y (2,3) (porque 1-2 está cubierto por ciclo 1-4-5-1)
    assert set(map(normalize_edge, [(0,1),(2,3)])).issubset(out)
    # (1,2) no es puente
    assert normalize_edge(1,2) not in out

# ---------- 7) articulation_points ----------

def test_articulation_points():
    # Grafo: 0-1-2-3 con ciclo 1-2-4-1, y un extremo 3
    # Articulaciones esperadas: 0 (si 0-1), 2 (corta 3) y 1 (según estructura).
    adj = undirected(5, [(0,1),(1,2),(2,3),(1,4),(2,4)])
    arts = set(articulation_points(adj))
    # Chequeos robustos (puede depender del root elegido)
    assert 2 in arts  # 2 separa 3 del resto
    assert 1 in arts or 0 in arts

# ---------- 8) topo_or_cycle ----------

def test_topo_or_cycle_dag_and_cycle():
    # DAG: 0->1->2, 0->2
    adj_dag = directed(3, [(0,1),(1,2),(0,2)])
    is_dag, data = topo_or_cycle(adj_dag)
    assert is_dag is True
    order = data
    # Orden topológico válido
    pos = {v:i for i,v in enumerate(order)}
    assert pos[0] < pos[1] < pos[2]

    # Con ciclo: 0->1->2->0
    adj_cyc = directed(3, [(0,1),(1,2),(2,0)])
    is_dag, data = topo_or_cycle(adj_cyc)
    assert is_dag is False
    cyc = data
    # Debe ser ciclo dirigido no vacío
    assert len(cyc) >= 3
    # Verificar edges
    for u, v in zip(cyc, cyc[1:]+cyc[:1]):
        assert v in adj_cyc[u]

# ---------- 9) scc_kosaraju ----------

def test_scc_kosaraju_basic():
    # Dos CFCs: {0,1,2} ciclo; {3,4} ciclo; arista 2->3
    adj = directed(5, [(0,1),(1,2),(2,0),(2,3),(3,4),(4,3)])
    comps = scc_kosaraju(adj)
    comps_sorted = [tuple(sorted(c)) for c in comps]
    assert set(comps_sorted) == { (0,1,2), (3,4) }

# ---------- 10) dfs_iter_leaves ----------

def test_dfs_iter_leaves_tree():
    # Árbol raíz 0: 0-1-2, 0-3, 1-4
    adj = undirected(5, [(0,1),(1,2),(0,3),(1,4)])
    count, leaves = dfs_iter_leaves(adj, start=0)
    # Hojas del árbol DFS (dependen del orden/pila), pero deben ser vértices de grado 1 en el árbol:
    # Posibles hojas: {2,3,4}
    assert count == len(leaves)
    assert set(leaves).issubset({2,3,4})
    assert count >= 2

# ---------- 11) path_dfs ----------

def test_path_dfs_found_and_not_found():
    # 0-1-2-3 y 1-4
    adj = undirected(5, [(0,1),(1,2),(2,3),(1,4)])
    p = path_dfs(adj, 0, 3)
    assert p[0] == 0 and p[-1] == 3
    # Camino inexistente entre componentes distintas
    adj2 = undirected(4, [(0,1),(2,3)])
    p2 = path_dfs(adj2, 0, 3)
    assert p2 == []

# ---------- 12) euler_orders_tree ----------

def test_euler_orders_tree_properties():
    # Árbol: 0-1-2, 0-3, 1-4
    adj = undirected(5, [(0,1),(1,2),(0,3),(1,4)])
    pre, post, tin, tout = euler_orders_tree(adj, root=0)

    n = len(adj)
    # Longitudes correctas
    assert len(pre) == n and len(post) == n
    assert len(tin) == n and len(tout) == n
    # tin < tout y todos únicos
    assert all(tin[v] < tout[v] for v in range(n))
    assert len(set(tin)) == n and len(set(tout)) == n
    # Propiedad de intervalos: u es ancestro de v <=> tin[u] <= tin[v] < tout[u]
    # (Chequeo parcial sobre algunas parejas)
    def is_ancestor(u, v):
        return tin[u] <= tin[v] < tout[u]
    # En el árbol: 0 es ancestro de todos; 1 ancestro de {2,4}
    for v in [1,2,3,4]:
        assert is_ancestor(0, v)
    for v in [2,4]:
        assert is_ancestor(1, v)
    assert not is_ancestor(2, 4) and not is_ancestor(4, 2)

if __name__ == "__main__":
    import pytest, sys
    # ejecuta solo dfs_times por ahora; cambiá por [] para correr todos
    sys.exit(pytest.main([__file__, "-k", "dfs_times " +
                                          "or connected_components " +
                                          "or find_cycle " +
                                          "or classify_edges_directed " +
                                          "or bipartite " + 
                                          "or bridges " + 
                                          "or articulation_points " + 
                                          "or topo_or_cycle ", "-q"]))
