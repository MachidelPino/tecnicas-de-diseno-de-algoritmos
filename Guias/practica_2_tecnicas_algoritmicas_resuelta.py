# Ejercicio 2 #
def magi_cuadrados(n: int):
    M = (n**3 + n) // 2
    res = [[None for _ in range(n)] for _ in range(n)]
    candidatos = [k+1 for k in range(n**2)]
    
    def backtrack_mc(res, n, i, j, candidatos: list, M):
        if i == n:
            # Se llenó el cuadrado, devolver copia de la solución
            return [row[:] for row in res]
        for idx, candidato in enumerate(candidatos):
            if es_valida(res, i, j, candidato, M):
                res[i][j] = candidato
                ni, nj = acomodar_indices(res, i, j)
                nuevos_candidatos = candidatos[:idx] + candidatos[idx+1:]
                solucion = backtrack_mc(res, n, ni, nj, nuevos_candidatos, M)
                if solucion:
                    return solucion
                res[i][j] = None  # Backtrack
        return None

    return backtrack_mc(res, n, 0, 0, candidatos, M)

def acomodar_indices(res, i, j):
    if j == len(res) - 1:
        i += 1
        j = 0
        return i, j

    j += 1
    return i, j 

def es_valida(res, i, j, candidato, M):
    res[i][j] = candidato
    n = len(res)

    # Filas
    for fila in res:
        if None not in fila and sum(fila) != M:
            res[i][j] = None
            return False
        if sumas(fila) > M:
            res[i][j] = None
            return False

    # Columnas    
    for j0 in range(n):
        columna = [res[i0][j0] for i0 in range(n)]
        if None not in columna and sum(columna) != M:
            res[i][j] = None
            return False
        if sumas(columna) > M:
            res[i][j] = None
            return False

    # Diagonales
    diagonal1 = [res[d][d] for d in range(n)]
    diagonal2 = [res[n-1-d][d] for d in range(n)]
    if None not in diagonal1 and sum(diagonal1) != M:
        res[i][j] = None
        return False
    if sumas(diagonal1) > M:
        res[i][j] = None
        return False
    if None not in diagonal2 and sum(diagonal2) != M:
        res[i][j] = None
        return False
    if sumas(diagonal2) > M:
        res[i][j] = None
        return False

    res[i][j] = None
    return True

def sumas(l):
    suma = 0
    for n in l:
        if n == None:
            suma += 0
        else:
            suma += n
    
    return suma

# Varios ejercicios de backtracking resueltos en otro archivo #

# Ejercicio 9 #
def king_army(n: int):
    memo: dict = {}                     # Inicializo memo
    def f(i):
        if i <= 1:                      # Casos Base    O(1)
            return 1                                    
        if i in memo:                   # Si ya calcule el valor anteriormente,
            return memo[i]              # lo devuelvo
        else:
            memo[i] = f(i-1) + f(i-2)   # Guardo nuevo valor en memo
            return memo[i]
    
    return f(n)
#print(king_army(5))

# Ejercicio 10 #
def vacations(dias: int, gym: dict, comp: dict):
    memo: dict = {}
    INF = 10**9

    def f(i, last):
        if i > dias - 1:
            return 0
        
        key = (i, last)
        if key in memo:
            return memo[key]
        
        mejor = INF

        cand = 1 + f(i+1, 0)
        if cand < mejor:
            mejor = cand
        
        if gym[i] == 1 and last != 1:
            cand = f(i+1, 1)
            if cand < mejor:
                mejor = cand
            
        if comp[i] == 1 and last != 2:
            cand = f(i+1, 2)
            if cand < mejor:
                mejor = cand

        memo[key] = mejor
        return memo[key]

    
    return f(1, 0)

#print(vacations(6, {1:1,2:1,3:0,4:1,5:1,6:1}, {1:1,2:1,3:1,4:0,5:1,6:1}))

def suma_dinamica(c, k):
    memo: dict = {}
    n = len(c)

    def top_down(i, j):
        if j < 0:
            return False
        if i == n:
            return j == 0
        
        key = i, j
        if key not in memo:
            memo[key] = top_down(i+1, j) or top_down(i+1, j - c[i])
        
        return memo[key]
        
    return top_down(0,k)

#print(suma_dinamica([6,12,6], 12))

def optipago_bt(billetes: list[int], costo: int):
    n = len(billetes)
    mejor_minimo = (float("inf"), float("inf"))

    def backtrack(cant_billetes: int, costo_parcial: int, i):
        nonlocal mejor_minimo
        if i == n:
            if costo_parcial >= costo:
                mejor_minimo = min(mejor_minimo, (costo_parcial, cant_billetes))
        else:
            backtrack(cant_billetes, costo_parcial, i+1)
            backtrack(cant_billetes + 1, costo_parcial + billetes[i], i+1)
    
    backtrack(0, 0, 0)
    return mejor_minimo

#print(optipago_bt([2,3,5,10,20,20], 14))

