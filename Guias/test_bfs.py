
# test_bfs.py
# Suite de tests (pytest) para ejercicios de BFS.
# Asume un módulo "bfs_exercises.py" con las firmas:
#   bfs_tree, shortest_path, bipartite_bfs, connected_components_bfs,
#   multisource_dist_directed, grid_shortest_path, grid_multisource_dist,
#   min_moves_modk, topo_kahn, eccentricity_layers

import itertools as it
import pytest

from bfs_exercises import (
    bfs_tree,
    shortest_path,
    bipartite_bfs,
    connected_components_bfs,
    multisource_dist_directed,
    grid_shortest_path,
    grid_multisource_dist,
    #min_moves_modk,
    #topo_kahn,
    #eccentricity_layers,
)

# -------- Helpers --------

def undirected(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)
    return g

def directed(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    return g

def is_valid_path(adj, path, directed_graph=False):
    if not path: return False
    for u, v in zip(path, path[1:]):
        if directed_graph:
            if v not in adj[u]:
                return False
        else:
            if v not in adj[u] or u not in adj[v]:
                return False
    return True

# ===============================================================
# 1) bfs_tree
# ===============================================================

def test_bfs_tree_line():
    # 0-1-2-3-4
    adj = undirected(5, [(0,1),(1,2),(2,3),(3,4)])
    dist, parent = bfs_tree(adj, 0)
    assert dist == [0,1,2,3,4]
    # Padres coherentes (en la cadena)
    assert parent[0] == -1
    for v in range(1,5):
        assert parent[v] in adj[v]

def test_bfs_tree_star_from_center():
    # Estrella centrada en 0
    edges = [(0,1),(0,2),(0,3),(0,4)]
    adj = undirected(5, edges)
    dist, parent = bfs_tree(adj, 0)
    assert dist == [0,1,1,1,1]
    assert all(parent[v] == 0 for v in [1,2,3,4])

# ===============================================================
# 2) shortest_path
# ===============================================================

def test_shortest_path_basic():
    # 0-1-2-3 ; 1-4
    adj = undirected(5, [(0,1),(1,2),(2,3),(1,4)])
    p = shortest_path(adj, 0, 3)
    assert p[0] == 0 and p[-1] == 3
    assert is_valid_path(adj, p)
    # Debe ser mínimo
    assert len(p) - 1 == 3

def test_shortest_path_none():
    # Dos componentes
    adj = undirected(4, [(0,1),(2,3)])
    p = shortest_path(adj, 0, 3)
    assert p == []

# ===============================================================
# 3) bipartite_bfs
# ===============================================================

def test_bipartite_true_square():
    # Ciclo par 0-1-2-3-0
    adj = undirected(4, [(0,1),(1,2),(2,3),(3,0)])
    ok, data = bipartite_bfs(adj)
    assert ok is True
    color = data
    for (u,v) in [(0,1),(1,2),(2,3),(3,0)]:
        assert color[u] != color[v]

def test_bipartite_false_triangle():
    # Triángulo (ciclo impar)
    adj = undirected(3, [(0,1),(1,2),(2,0)])
    ok, cyc = bipartite_bfs(adj)
    assert ok is False
    assert isinstance(cyc, list) and len(cyc) >= 3 and len(cyc) % 2 == 1
    # Verificar que todas las aristas del ciclo existen
    E = set(tuple(sorted(e)) for e in [(0,1),(1,2),(2,0)])
    cycE = set(tuple(sorted(e)) for e in zip(cyc, cyc[1:] + cyc[:1]))
    assert cycE.issubset(E)

# ===============================================================
# 4) connected_components_bfs
# ===============================================================

def test_connected_components_three():
    # Componentes: {0,1,2}, {3,4}, {5}
    adj = undirected(6, [(0,1),(1,2),(3,4)])
    comps = [sorted(c) for c in connected_components_bfs(adj)]
    assert sorted(comps) == [[0,1,2],[3,4],[5]]

def test_connected_components_single():
    adj = undirected(4, [(0,1),(1,2),(2,3),(0,3)])
    comps = [sorted(c) for c in connected_components_bfs(adj)]
    assert comps == [ [0,1,2,3] ]

# ===============================================================
# 5) multisource_dist_directed
# ===============================================================

def test_multisource_dist_directed_basic():
    # 0->2, 1->2, 2->3, 3->4
    adj = directed(5, [(0,2),(1,2),(2,3),(3,4)])
    dist = multisource_dist_directed(adj, [0,1])
    # Desde {0,1}, dist(2)=1, dist(3)=2, dist(4)=3
    assert dist[2] == 1 and dist[3] == 2 and dist[4] == 3
    # Fuentes a 0
    assert dist[0] == 0 and dist[1] == 0

def test_multisource_dist_directed_unreachable():
    # 0->1 y componente aparte 2->3
    adj = directed(4, [(0,1),(2,3)])
    dist = multisource_dist_directed(adj, [0])
    assert dist[0] == 0 and dist[1] == 1
    assert dist[2] == -1 and dist[3] == -1

# ===============================================================
# 6) grid_shortest1_path
# ===============================================================

def test_grid_shortest1_path_basic():
    # 0 libre, 1 bloqueado
    grid = [
        [0,0,0],
        [0,1,0],
        [0,0,0],
    ]
    d = grid_shortest_path(grid, (0,0), (2,2))
    # Camino mínimo bordeando el obstáculo: 4 movimientos derecha/abajo
    assert d == 4

def test_grid_shortest1_path_impossible():
    grid = [
        [0,1],
        [1,0],
    ]
    assert grid_shortest_path(grid, (0,0), (1,1)) == -1

# ===============================================================
# 7) grid_multisource_dist
# ===============================================================

def test_grid_multisource_dist_center_source():
    grid = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
    ]
    dist = grid_multisource_dist(grid, [(1,1)])
    # Distancias Manhattan desde (1,1)
    assert dist[0][0] == 2 and dist[1][1] == 0 and dist[2][2] == 2

def test_grid_multisource_dist_with_walls():
    grid = [
        [0,1,0,0],
        [0,1,0,0],
        [0,0,0,1],
        [0,0,0,0],
    ]
    # Fuentes arriba izq y abajo der
    dist = grid_multisource_dist(grid, [(0,0),(3,3)])
    # Celdas bloqueadas deben quedar -1 o no actualizadas; chequeamos algunas libres
    assert dist[0][0] == 0 and dist[3][3] == 0
    # Celda (2,2) es alcanzable por ambos; la mínima debería ser 2
    assert dist[2][2] == 2

# ===============================================================
# 8) min_moves_modk
# ===============================================================

def test_min_moves_modk_example():
    # Ejemplo inspirado en la guía (k=10)
    grid = [
        [1,3,6],
        [6,7,4],
        [4,9,3],
    ]
    k = 10
    # start (0,0) valor inicial v1=1, objetivo w=0 -> 1->3->6 (2 movs)
    assert min_moves_modk(grid, k, (0,0), v1=1, w=0) == 2

def test_min_moves_modk_impossible_small():
    grid = [
        [0,0],
        [0,0],
    ]
    k = 2
    # Si v1=1, w=0, moverse siempre suma 0 -> imposible
    assert min_moves_modk(grid, k, (0,0), v1=1, w=0) == -1

# ===============================================================
# 9) topo_kahn
# ===============================================================

def test_topo_kahn_dag():
    # DAG con orden único 0<1<2
    adj = directed(3, [(0,1),(1,2),(0,2)])
    ok, order = topo_kahn(adj)
    assert ok is True
    pos = {v:i for i,v in enumerate(order)}
    assert pos[0] < pos[1] < pos[2]

def test_topo_kahn_cycle():
    # Ciclo 0->1->2->0
    adj = directed(3, [(0,1),(1,2),(2,0)])
    ok, order = topo_kahn(adj)
    assert ok is False and order == []

# ===============================================================
# 10) eccentricity_layers
# ===============================================================

def test_eccentricity_layers_line():
    # 0-1-2-3
    adj = undirected(4, [(0,1),(1,2),(2,3)])
    ecc, layers = eccentricity_layers(adj, 1)
    # Desde 1: capas {1}, {0,2}, {3}; excentricidad = 2
    assert ecc == 2
    assert layers[0] == [1]
    assert set(layers[1]) == {0,2} and layers[2] == [3]

def test_eccentricity_layers_in_component_only():
    # Dos componentes: {0,1,2} y {3,4}
    adj = undirected(5, [(0,1),(1,2),(3,4)])
    ecc, layers = eccentricity_layers(adj, 0)
    # En la componente de 0, la excentricidad es 2 (hasta el 2)
    assert ecc == 2
    # 3 y 4 no deben aparecer en las capas
    assert all(3 not in layer and 4 not in layer for layer in layers)

if __name__ == "__main__":
    import pytest, sys
    # ejecuta solo dfs_times por ahora; cambiá por [] para correr todos
    sys.exit(pytest.main([__file__, "-k", "bfs_tree " + 
                                          "or shortest_path " + 
                                          "or bipartite " + 
                                          "or connected_components " + 
                                          "or multisource_dist_directed " + 
                                          "or grid_shortest1_path " + 
                                          "or grid_multisource_dist ", "-q"]))