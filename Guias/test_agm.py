# test_agm.py
# Suite de tests (pytest) para AGM, minimax y maximin.
# Requiere un módulo "agm_exercises.py" con las funciones:
#   kruskal_mst, prim_mst, mst_sequences, bottleneck_spanning_tree,
#   maximum_spanning_tree, maximin_path_value, minimax_path_value,
#   network_bandwidth, bandwidth_after_upgrades, boruvka_mst, is_mst_unique
#
# Formato:
# - edges: lista de (u, v, w), grafo NO dirigido, sin loops.
# - adj: lista de adyacencia no dirigida con (vecino, peso).
import math
import pytest

from agm_exercises import (
    kruskal_mst,
    prim_mst,
    mst_sequences,
    #bottleneck_spanning_tree,
    #maximum_spanning_tree,
    #maximin_path_value,
    #minimax_path_value,
    #network_bandwidth,
    #bandwidth_after_upgrades,
    #boruvka_mst,
    #is_mst_unique,
)

# ---------- Helpers ----------
def make_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

# ========== 1) Kruskal ==========
def test_kruskal1_triangle_simple():
    # MST = 1 + 2 = 3
    n = 3
    edges = [(0,1,1), (1,2,2), (0,2,3)]
    w, E = kruskal_mst(n, edges)
    assert w == 3
    assert len(E) == n - 1

def test_kruskal1_disconnected_forest():
    # Dos componentes: {0,1,2} y {3} aislado
    n = 4
    edges = [(0,1,1), (1,2,2), (0,2,3)]
    w, E = kruskal_mst(n, edges)
    assert w == 3 and len(E) == 2  # 3 nodos conectados => 2 aristas

# ========== 2) Prim ==========
def test_prim_triangle():
    n = 3
    edges = [(0,1,1), (1,2,2), (0,2,3)]
    w, parent = prim_mst(n, make_adj(n, edges))
    assert w == 3
    assert sum(1 for p in parent if p != -1) == n - 1

def test_prim_square_with_diagonals():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1),(3,0,1),(0,2,10),(1,3,10)]
    w, parent = prim_mst(n, make_adj(n, edges))
    assert w == 3
    assert sum(1 for p in parent if p != -1) == n - 1

# ========== 3) MST sobre secuencias (distancia L1) ==========
def test_mst_sequences_small():
    # d01=1, d02=2, d12=1 -> MST = 2
    X = [[0,0],[1,0],[1,1]]
    w, E = mst_sequences(X)
    assert w == 2 and len(E) == 2

def test_mst_sequences_line1D():
    # puntos 0,5,9 -> dist 5,9,4 => MST = 9
    X = [[0],[5],[9]]
    w, E = mst_sequences(X)
    assert w == 9 and len(E) == 2

# ========== 4) Árbol bottleneck (MBST) ==========
def test_bottleneck_equals_mst_max_edge_case1():
    n = 3
    edges = [(0,1,5),(1,2,3),(0,2,4)]
    wk, Ek = kruskal_mst(n, edges)
    _, Eb = bottleneck_spanning_tree(n, edges)
    assert len(Eb) == n - 1
    assert max(w for _,_,w in Eb) == max(w for _,_,w in Ek)

def test_bottleneck_equals_mst_max_edge_case2():
    n = 4
    edges = [(0,1,2),(1,2,2),(2,3,5),(0,3,4),(1,3,3)]
    wk, Ek = kruskal_mst(n, edges)
    _, Eb = bottleneck_spanning_tree(n, edges)
    assert len(Eb) == n - 1
    assert max(w for _,_,w in Eb) == max(w for _,_,w in Ek)

# ========== 5) MaxST y maximin path ==========
def test_maximum_spanning_tree_weight():
    n = 4
    edges = [(0,1,5),(1,2,4),(2,3,3),(3,0,2),(0,2,1)]
    w, E = maximum_spanning_tree(n, edges)
    assert len(E) == n - 1 and w == 12  # 5+4+3

def test_maximin_path_value_simple():
    # Mejor ancho de banda 0->4 es 2
    n = 5
    edges = [(0,1,5),(1,2,4),(0,2,3),(2,3,2),(3,4,1),(0,4,2)]
    val = maximin_path_value(n, edges, 0, 4)
    assert val == 2

# ========== 6) Minimax path ==========
def test_minimax_path_value_case1():
    # 0->2->4 (3,3) minimiza el máximo a 3
    n = 5
    edges = [(0,1,5),(1,4,5),(0,2,3),(2,4,3),(0,3,2),(3,4,4)]
    val = minimax_path_value(n, edges, 0, 4)
    assert val == 3

def test_minimax_path_value_case2():
    # 0-1 (1), 1-2 (10), 0-2 (5) -> minimax(0,2) = 5
    n = 3
    edges = [(0,1,1),(1,2,10),(0,2,5)]
    val = minimax_path_value(n, edges, 0, 2)
    assert val == 5

# ========== 7) Network bandwidth ==========
def test_network_bandwidth_chain():
    n = 4
    edges = [(0,1,4),(1,2,3),(2,3,2),(0,3,1)]
    assert network_bandwidth(n, edges) == 2

def test_network_bandwidth_star():
    n = 5
    edges = [(0,1,10),(0,2,9),(0,3,8),(0,4,7)]
    assert network_bandwidth(n, edges) == 7

# ========== 8) Bandwidth after upgrades (vector a[i]) ==========
def test_bandwidth_after_upgrades_properties_case1():
    n = 4
    edges = [(0,1,4),(1,2,3),(2,3,2),(0,3,1)]
    a = bandwidth_after_upgrades(n, edges)
    assert isinstance(a, list) and len(a) == n
    assert a[0] == network_bandwidth(n, edges)
    assert all(a[i] <= a[i+1] for i in range(n-1))
    assert a[1] >= 3 and a[2] >= 4
    maxw = max(w for _,_,w in edges)
    assert math.isinf(a[-1]) or a[-1] >= maxw

def test_bandwidth_after_upgrades_properties_case2():
    # Triángulo: a0=2; con 1 upgrade llegamos a 3
    n = 3
    edges = [(0,1,1),(1,2,2),(0,2,3)]
    a = bandwidth_after_upgrades(n, edges)
    assert a[0] == 2 and a[1] >= 3
    assert all(a[i] <= a[i+1] for i in range(n-1))

# ========== 9) Borůvka ==========
def test_boruvka_matches_kruskal_case1():
    n = 4
    edges = [(0,1,1),(1,2,2),(2,3,3),(0,3,4),(1,3,5)]
    wk, Ek = kruskal_mst(n, edges)
    wb, Eb = boruvka_mst(n, edges)
    assert wb == wk and len(Eb) == n - 1

def test_boruvka_matches_kruskal_case2():
    n = 5
    edges = [(0,1,2),(0,2,3),(1,2,1),(1,3,4),(2,4,5),(3,4,6)]
    wk, Ek = kruskal_mst(n, edges)
    wb, Eb = boruvka_mst(n, edges)
    assert wb == wk and len(Eb) == n - 1

# ========== 10) Unicidad del AGM ==========
def test_is_mst_unique_true_distinct_weights():
    n = 3
    edges = [(0,1,1),(1,2,2),(0,2,3)]
    assert is_mst_unique(n, edges) is True

def test_is_mst_unique_false_square_equal_weights():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1),(3,0,1),(0,2,100)]  # diagonal grande para conexidad
    assert is_mst_unique(n, edges) is False

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-k", "kruskal1 " + 
                                          "or prim " + 
                                          "or mst_sequences", "-q"]))