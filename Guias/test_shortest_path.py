import math
import pytest

# All functions must be implemented by you in shortest_path.py
from shortest_path_exercises import (
    shortest_avoiding_efficient_edges,      # 1
    max_edge_under_path_budget,             # 2
    min_path_with_at_most_one_negative,     # 3
    improving_edges_joint,                  # 4
    critical_edges,                         # 5
    min_multiplicative_path,                # 6
    has_profit_cycle,                       # 7
    count_paths_dag,                        # 8
    solve_srd,                              # 9
    assign_queues_linear,                   # 10
    is_geodesic,                            # 11
    #dag_shortest_paths,                     # 12
    #min_coins_change,                       # 13
    #critical_tasks,                         # 14
    #earliest_arrival_with_openings,         # 15
    #earliest_arrival_bf_openings            # 16
)

INF = float('inf')
EPS = 1e-9

# -----------------------------
# Helpers
# -----------------------------

def path_cost(path, edges):
    """Utility to compute cost of a path list [v0,...,vk] under directed edges list (u,v,w)."""
    cost = 0.0
    ed = {}
    for u, v, w in edges:
        ed.setdefault(u, {})[v] = w
    for u, v in zip(path[:-1], path[1:]):
        assert v in ed.get(u, {}), f"edge ({u},{v}) not found"
        cost += ed[u][v]
    return cost


# ---------------------------------------------------------------------------
# 1) shortest_avoiding_efficient_edges
# ---------------------------------------------------------------------------

def test_1_avoid_efficient_edges_basic():
    # Graph:
    # 0->1(1), 1->3(1)  => optimal cost 2 (efficient edges)
    # 0->2(2), 2->3(2)  => alternative cost 4 (should be returned)
    n = 4
    edges = [(0,1,1),(1,3,1),(0,2,2),(2,3,2)]
    s, t = 0, 3
    path, cost = shortest_avoiding_efficient_edges(n, edges, s, t)
    assert path == [0,2,3]
    assert abs(cost - 4.0) < EPS
    # sanity: original shortest cost is 2
    assert path_cost([0,1,3], edges) == 2

def test_1_avoid_efficient_edges_none():
    # All s-t paths are optimal -> removing efficient edges leaves no path
    n = 3
    edges = [(0,1,1),(1,2,1)]
    res = shortest_avoiding_efficient_edges(n, edges, 0, 2)
    assert res is None


# ---------------------------------------------------------------------------
# 2) max_edge_under_path_budget
# ---------------------------------------------------------------------------

def test_2_max_edge_under_budget_exists():
    # Paths s=0 -> 3, budget C=6
    # 0->1(2),1->3(2) (max edge 2)  total 4
    # 0->2(3),2->3(3) (max edge 3)  total 6  -> should pick (2,3,3)
    n=4
    edges=[(0,1,2),(1,3,2),(0,2,3),(2,3,3)]
    s,t,C=0,3,6
    ans = max_edge_under_path_budget(n, edges, s, t, C)
    assert ans == (2,3,3)

def test_2_max_edge_under_budget_none():
    n=3
    edges=[(0,1,5),(1,2,6)]
    C=10  # but shortest is 11
    assert max_edge_under_path_budget(n, edges, 0, 2, C) is None


# ---------------------------------------------------------------------------
# 3) min_path_with_at_most_one_negative
# ---------------------------------------------------------------------------

def test_3_one_negative_improves():
    # 0->1(5),1->3(5)  cost 10
    # 0->2(8),2->1(-6),1->3(5) uses one negative: cost 7  -> should be 7
    n=4
    edges=[(0,1,5),(1,3,5),(0,2,8),(2,1,-6)]
    assert abs(min_path_with_at_most_one_negative(n, edges, 0, 3) - 7.0) < EPS

def test_3_one_negative_none():
    # no path at all from 0 to 2
    n=3
    edges=[(0,1,1)]
    assert min_path_with_at_most_one_negative(n, edges, 0, 2) is None


# ---------------------------------------------------------------------------
# 4) improving_edges_joint
# ---------------------------------------------------------------------------

def test_4_improving_edges_joint_example():
    # Given by the discussion: base dist 0->3 is 6 via 0->2->3
    # Adding (2,4,2) and (4,3,1) yields path 0->2->4->3 of cost 5 -> both should be returned
    n = 5
    G  = [(0,1,10),(0,2,2),(1,2,0),(2,3,4),(3,1,0),(3,4,9)]
    E2 = [(4,3,1),(2,4,2)]
    s, t = 0, 3
    ans = set(improving_edges_joint(n, G, s, t, E2))
    assert ans == set(E2)

def test_4_improving_edges_joint_no_improve():
    n=3
    G=[(0,1,1),(1,2,1)]
    E2=[(0,2,5)]
    assert improving_edges_joint(n,G,0,2,E2) == []


# ---------------------------------------------------------------------------
# 5) critical_edges
# ---------------------------------------------------------------------------

def test_5_critical_edges_single_path():
    n=4
    edges=[(0,1,1),(1,2,1),(2,3,1)]
    crit = set((u,v,w) for (u,v,w) in critical_edges(n,edges,0,3))
    assert crit == set(edges)   # única ruta -> todas críticas

def test_5_critical_edges_multiple_paths():
    n=4
    edges=[(0,1,1),(1,3,1),(0,2,1),(2,3,1)]
    # Dos caminos mínimos disjuntos: ninguna arista es crítica
    assert critical_edges(n, edges, 0, 3) == []


# ---------------------------------------------------------------------------
# 6) min_multiplicative_path
# ---------------------------------------------------------------------------

def test_6_multiplicative_simple():
    n=3
    edges=[(0,1,2.0),(1,2,2.0),(0,2,5.0)]
    # 0->1->2 has product 4 < 5
    assert abs(min_multiplicative_path(n, edges, 0, 2) - 4.0) < EPS

def test_6_multiplicative_unreachable():
    n=2
    edges=[]
    assert min_multiplicative_path(n, edges, 0, 1) is None


# ---------------------------------------------------------------------------
# 7) has_profit_cycle (model cycle with overall negative cost after transform)
# ---------------------------------------------------------------------------

def test_7_profit_cycle_exists():
    # 0 -> 1 -> 0, con netos negativos:
    # w'(0->1) = travel(0,1)=1 + cabins[1]=-3  => -2
    # w'(1->0) = travel(1,0)=1 + cabins[0]=-3  => -2
    # suma ciclo = -4 < 0  => hay ganancia positiva
    cabins = [-3.0, -3.0]
    travel = [(0, 1, 1.0), (1, 0, 1.0)]
    assert has_profit_cycle(cabins, travel) is True

def test_7_profit_cycle_absent():
    # mismos tramos pero sin “subsidios” de cabañas: netos todos positivos
    # w'(0->1) = 1 + 0 = 1, w'(1->0) = 1 + 0 = 1  => suma ciclo = 2 > 0
    cabins = [0.0, 0.0]
    travel = [(0, 1, 1.0), (1, 0, 1.0)]
    assert has_profit_cycle(cabins, travel) is False

# ------------------------------------------------------------------
# Tests extra para has_profit_cycle
# ------------------------------------------------------------------

def test_profit_cycle_self_loop_negative():
    # Ciclo de longitud 1 (self-loop): w'(0->0) = travel(0,0)=0 + cabins[0]=-1 => -1 < 0
    cabins = [-1.0]
    travel = [(0, 0, 0.0)]
    assert has_profit_cycle(cabins, travel) is True

def test_profit_cycle_parallel_edges_pick_negative():
    # Dos aristas paralelas 0->1 (una cara, una barata).
    # Elegir la combinación que hace el ciclo negativo.
    # cabins[0]=-2, cabins[1]=-1
    # 0->1 (caro): 5 + (-1) = 4
    # 0->1 (barato): 0 + (-1) = -1
    # 1->0: 0 + (-2) = -2
    # Usando barato + regreso: (-1) + (-2) = -3 < 0
    cabins = [-2.0, -1.0]
    travel = [(0, 1, 5.0), (0, 1, 0.0), (1, 0, 0.0)]
    assert has_profit_cycle(cabins, travel) is True

def test_profit_cycle_disconnected_component_detected():
    # El ciclo negativo está en una componente distinta; debe detectarse igual.
    # Componente A: nodos 0,1 sin ciclo negativo.
    # Componente B: nodos 2,3 con ciclo negativo (viajes 0 + cabins negativos).
    cabins = [0.0, 0.0, -3.0, -3.0]
    travel = [
        (0, 1, 1.0), (1, 0, 1.0),   # ciclo positivo en A
        (2, 3, 0.0), (3, 2, 0.0)    # ciclo negativo en B: -3 + -3 = -6
    ]
    assert has_profit_cycle(cabins, travel) is True

def test_profit_cycle_absent_large_cycle_mixed_signs():
    # Hay aristas con neto negativo, pero NINGÚN ciclo suma < 0.
    # 0->1: 3 + (-2) = 1
    # 1->2: 2 + 0    = 2
    # 2->0: 1 + 0    = 1
    # Suma ciclo 0-1-2-0 = 4 > 0
    cabins = [-2.0, 0.0, 0.0]
    travel = [(0,1,3.0),(1,2,2.0),(2,0,1.0)]
    assert has_profit_cycle(cabins, travel) is False

def test_profit_cycle_zero_travel_zero_cabins_no_cycle():
    # Sin costos y sin aristas que cierren ciclo: debe dar False.
    cabins = [0.0, 0.0, 0.0]
    travel = [(0,1,0.0), (1,2,0.0)]  # DAG sin ciclos
    assert has_profit_cycle(cabins, travel) is False

def test_profit_cycle_undirected_requires_both_directions():
    # Si el grafo es “no dirigido”, hay que pasar ambas direcciones.
    # Solo 0->1 con neto negativo NO alcanza si falta 1->0.
    cabins = [-5.0, -5.0]
    travel = [(0,1,0.0)]  # falta (1,0,0.0) => no hay ciclo
    assert has_profit_cycle(cabins, travel) is False

def test_profit_cycle_precision_true_when_below_eps():
    # Suma del ciclo = -1e-9 < 0 (más negativa que -EPS=1e-12) => True.
    # 0->1: 0 + (-5) = -5
    # 1->0: 5 - 1e-9 + 0 = 5 - 1e-9
    # total = -1e-9
    cabins = [-5.0, 0.0]
    travel = [(0,1,0.0), (1,0,5.0 - 1e-9)]
    assert has_profit_cycle(cabins, travel) is True

def test_profit_cycle_precision_false_when_within_eps():
    # Suma del ciclo ≈ -1e-13 (en magnitud MENOR que EPS=1e-12) => se considera 0 => False.
    cabins = [-5.0, 0.0]
    travel = [(0,1,0.0), (1,0,5.0 - 1e-13)]
    assert has_profit_cycle(cabins, travel) is False

def test_profit_cycle_no_edges():
    # Sin aristas no puede haber ciclo.
    cabins = [0.0, -10.0]
    travel = []
    assert has_profit_cycle(cabins, travel) is False

def test_profit_cycle_three_node_negative_2_cycle_inside():
    # Hay un 2-ciclo negativo embebido en un grafo más grande.
    cabins = [0.0, -4.0, 10.0]
    travel = [
        (0, 1, 0.0), (1, 0, 0.0),   # ciclo 0-1-0 con suma -4 < 0
        (1, 2, 1.0), (2, 1, 1.0)    # otro 2-ciclo positivo
    ]
    assert has_profit_cycle(cabins, travel) is True


# ---------------------------------------------------------------------------
# 8) count_paths_dag
# ---------------------------------------------------------------------------

def test_8_count_paths_small_dag():
    # 0->1, 0->2, 1->3, 2->3 => paths 0->1->3 and 0->2->3 => 2
    n=4
    edges=[(0,1),(0,2),(1,3),(2,3)]
    assert count_paths_dag(n, edges) == 6  # total non-empty: (0->1),(0->2),(1->3),(2->3),(0->1->3),(0->2->3) = 6?
    # Wait: the function from the exercise counts ALL non-empty paths in the whole DAG
    # For this tiny DAG: paths are [0->1], [0->2], [1->3], [2->3], [0->1->3], [0->2->3] = 6
    # But our exercise version (section) counted all non-empty -> 6.
    # So we assert 6 instead of 4.
    assert count_paths_dag(n, edges) == 6

def test_8_count_paths_dag_chain():
    # Chain of 3 edges: number of non-empty paths = 3 (single edges) + 2 (length 2) + 1 (length3) = 6
    n=4
    edges=[(0,1),(1,2),(2,3)]
    assert count_paths_dag(n, edges) == 6


# ---------------------------------------------------------------------------
# 9) solve_srd (SRD solver with cycle extraction)
# ---------------------------------------------------------------------------

def test_9_srd_sat_and_values():
    # System: x1 - x2 <= 1, x2 - x1 <= 2  => feasible.
    n = 2
    ineqs = [(1,2,1),(2,1,2)]
    status, vals = solve_srd(n, ineqs)
    assert status == "SAT"
    assert len(vals) == n

def test_9_srd_unsat_cycle():
    # x1 - x2 <= -5, x2 - x1 <= -1  => sum => 0 <= -6 -> negative cycle
    n=2
    ineqs=[(1,2,-5),(2,1,-1)]
    status, cert = solve_srd(n, ineqs)
    assert status == "UNSAT"
    assert isinstance(cert, list) and len(cert) > 0


# ---------------------------------------------------------------------------
# 10) assign_queues_linear (supermarket)
# ---------------------------------------------------------------------------

def test_10_supermarket_feasible():
    # M=5, 3 clients: 0 left of 1 with K=2; 1 and 2 friends within L=1
    M=5
    fights=[(0,1,2,True)]
    friends=[(1,2,1)]
    status, sol = assign_queues_linear(M, fights, friends)
    assert status == "SAT"
    x = sol
    assert 1 <= x[0] <= M and 1 <= x[1] <= M and 1 <= x[2] <= M
    assert x[1] - x[0] >= 2 and abs(x[1] - x[2]) <= 1

def test_10_supermarket_infeasible():
    # Conflict: friends L=0 but fight requires K=2 -> impossible
    M=3
    fights=[(0,1,2,True)]
    friends=[(0,1,0)]
    status, _ = assign_queues_linear(M, fights, friends)
    assert status == "UNSAT"


# ---------------------------------------------------------------------------
# 11) is_geodesic
# ---------------------------------------------------------------------------

def test_11_is_geodesic_true():
    # Triangle 0-1-2 with unit weights; D={0,2} covers all via intervals
    n=3
    edges=[(0,1,1),(1,2,1),(0,2,2)]  # directed or undirected as your implementation defines
    D={0,2}
    assert is_geodesic(n, edges, D) is True

def test_11_is_geodesic_single_vertex_true():
    n = 1
    edges = []
    D = {0}
    assert is_geodesic(n, edges, D) is True

def test_12_is_geodesic_two_vertices_true():
    n = 2
    edges = [(0,1,1)]
    D = {0,1}
    assert is_geodesic(n, edges, D) is True

def test_13_is_geodesic_two_vertices_false_D_one():
    n = 2
    edges = [(0,1,1)]
    D = {0}
    assert is_geodesic(n, edges, D) is False

def test_14_is_geodesic_path_endpoints_true():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1)]
    D = {0,3}
    assert is_geodesic(n, edges, D) is True

def test_15_is_geodesic_path_middle_false():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1)]
    D = {1,2}
    assert is_geodesic(n, edges, D) is False

def test_16_is_geodesic_star_false_two_leaves():
    n = 5
    edges = [(0,1,1),(0,2,1),(0,3,1),(0,4,1)]
    D = {1,2}
    assert is_geodesic(n, edges, D) is False

def test_17_is_geodesic_star_true_all_leaves():
    n = 5
    edges = [(0,1,1),(0,2,1),(0,3,1),(0,4,1)]
    D = {1,2,3,4}
    assert is_geodesic(n, edges, D) is True

def test_18_is_geodesic_diamond_true_endpoints():
    n = 4
    edges = [(0,1,1),(1,3,1),(0,2,1),(2,3,1)]
    D = {0,3}
    assert is_geodesic(n, edges, D) is True

def test_19_is_geodesic_cycle4_true_opposite():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1),(3,0,1)]
    D = {0,2}
    assert is_geodesic(n, edges, D) is True

def test_20_is_geodesic_cycle5_false_sparse_D():
    n = 5
    edges = [(0,1,1),(1,2,1),(2,3,1),(3,4,1),(4,0,1)]
    D = {0,2}
    assert is_geodesic(n, edges, D) is False

def test_21_is_geodesic_cycle5_true_three_spread():
    n = 5
    edges = [(0,1,1),(1,2,1),(2,3,1),(3,4,1),(4,0,1)]
    D = {0,2,4}
    assert is_geodesic(n, edges, D) is True

def test_22_is_geodesic_triangle_false_varied_weights():
    n = 3
    edges = [(0,1,2),(1,2,2),(0,2,1)]
    D = {0,1}
    assert is_geodesic(n, edges, D) is False

def test_23_is_geodesic_T_tree_true_leaves():
    n = 4
    edges = [(0,1,1),(1,2,1),(1,3,1)]
    D = {0,2,3}
    assert is_geodesic(n, edges, D) is True

def test_24_is_geodesic_T_tree_false_two_leaves_only():
    n = 4
    edges = [(0,1,1),(1,2,1),(1,3,1)]
    D = {0,2}
    assert is_geodesic(n, edges, D) is False

def test_25_is_geodesic_complete_false_pair():
    n = 4
    edges = [(0,1,1),(0,2,1),(0,3,1),(1,2,1),(1,3,1),(2,3,1)]
    D = {0,1}
    assert is_geodesic(n, edges, D) is False

def test_26_is_geodesic_complete_true_all_D():
    n = 4
    edges = [(0,1,1),(0,2,1),(0,3,1),(1,2,1),(1,3,1),(2,3,1)]
    D = {0,1,2,3}
    assert is_geodesic(n, edges, D) is True

def test_27_is_geodesic_heavy_shortcut_still_path_true():
    n = 4
    edges = [(0,1,1),(1,2,1),(2,3,1),(0,3,100)]
    D = {0,3}
    assert is_geodesic(n, edges, D) is True

# Esta mal el test
"""def test_11_is_geodesic_false():
    n=4
    edges=[(0,1,1),(1,2,1),(2,3,1)]
    D={0,3}
    assert is_geodesic(n, edges, D) is False"""


# ---------------------------------------------------------------------------
# 12) dag_shortest_paths
# ---------------------------------------------------------------------------

def test_12_dag_shortest_paths_basic():
    n=5
    edges=[(0,1,1),(0,2,5),(1,3,2),(2,3,1),(3,4,1)]
    dist, parent = dag_shortest_paths(n, edges, 0)
    assert dist[4] == 1+2+1  # 0->1->3->4
    # parents reconstruct 4->3->1->0
    assert parent[4] == 3 and parent[3] in (1,2) and parent[0] is None

def test_12_dag_shortest_paths_with_negative_edge():
    n=3
    edges=[(0,1,2),(1,2,-1)]
    dist, parent = dag_shortest_paths(n, edges, 0)
    assert dist[2] == 1


# ---------------------------------------------------------------------------
# 13) min_coins_change
# ---------------------------------------------------------------------------

def test_13_min_coins_change_simple():
    vals=[1,3,4]
    assert min_coins_change(vals, 6) == 2  # 3+3 (or 2 coins)

def test_13_min_coins_change_unreachable():
    vals=[3,5]
    # If unreachable under this model, return INF or -1. We accept -1.
    res = min_coins_change(vals, 1)
    assert res in (-1, math.inf, float('inf'))


# ---------------------------------------------------------------------------
# 14) critical_tasks (project scheduling)
# ---------------------------------------------------------------------------

def test_14_critical_tasks_basic():
    # DAG of tasks: 0->2, 1->2; times=[2,1,3].  Critical tasks are all (0,1,2) for a tight project.
    n=3
    prereq=[(0,2),(1,2)]
    times=[2,1,3]
    crit = set(critical_tasks(n, prereq, times))
    assert crit == {0,1,2}

def test_14_critical_tasks_noncritical():
    # Add slack on task 1
    n=3
    prereq=[(0,2),(1,2)]
    times=[2,1,10]
    crit = set(critical_tasks(n, prereq, times))
    assert 2 in crit and 0 in crit and 1 not in crit


# ---------------------------------------------------------------------------
# 15) earliest_arrival_with_openings (Dijkstra with openings)
# ---------------------------------------------------------------------------

def test_15_earliest_arrival_waiting():
    # 0->1 opens at 5, travel 2. Start at 0 at time 0: wait 5, arrive 7.
    n=2
    edges=[((0,1),5,2)]
    d = earliest_arrival_with_openings(n, edges, 0)
    assert d[1] == 7

def test_15_earliest_arrival_chain():
    # 0->1 open0/1, 1->2 open0/3 => arrive 4
    n=3
    edges=[((0,1),0,1),((1,2),0,3)]
    d = earliest_arrival_with_openings(n, edges, 0)
    assert d[2] == 4


# ---------------------------------------------------------------------------
# 16) earliest_arrival_bf_openings (Bellman–Ford with possible negative travel)
# ---------------------------------------------------------------------------

def test_16_bf_openings_with_negative_travel():
    # 0->1 open0/5, 1->2 open0/-2 (time gain), 0->2 open0/10 -> best is 0->1->2: 5 + (-2) = 3
    n=3
    edges=[((0,1),0,5),((1,2),0,-2),((0,2),0,10)]
    d = earliest_arrival_bf_openings(n, edges, 0)
    assert d[2] == 3

def test_16_bf_openings_respects_opening():
    # 0->1 open5/1, 1->2 open10/1. Best arrival:
    # 0->1 at 6, then wait until 10, arrive 11; direct 0->2 open0/20 => 20 -> choose 11.
    n=3
    edges=[((0,1),5,1),((1,2),10,1),((0,2),0,20)]
    d = earliest_arrival_bf_openings(n, edges, 0)
    assert d[2] == 11

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-k", "avoid_efficient_edges " + 
                                          "or max_edge_under_budget " + 
                                          "or one_negative " + 
                                          "or improving_edges_joint " +
                                          "or critical_edges " + 
                                          "or multiplicative " + 
                                          "or profit_cycle " + 
                                          "or count_paths " + 
                                          "or srd " + 
                                          "or supermarket " + 
                                          "or is_geodesic", "-q"]))