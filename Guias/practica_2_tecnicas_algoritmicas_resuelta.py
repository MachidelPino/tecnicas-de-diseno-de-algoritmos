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
print(king_army(5))