def cadenas_binarias(n: int):
    def backtrack(pref):
        nonlocal n
        if len(pref) == n:
            print(pref)
        else:
            backtrack(pref + "0")
            backtrack(pref + "1")
            # Otra Opcion:
            # for bit in range(2):
            #     backtrack(pref + str(bit))

    backtrack("")
#cadenas_binarias(3)

def permutaciones(c):
    def backtrack(permutacion: list, candidatos: list):
        if len(permutacion) == len(c):
            print(permutacion)
        else:
            for candidato in candidatos:
                nueva_permutacion = permutacion + [candidato]
                nuevos_candidatos = candidatos.copy()
                nuevos_candidatos.remove(candidato)
                backtrack(nueva_permutacion, nuevos_candidatos)

    backtrack([], c)
#permutaciones([1,2,3,4])

def subset_sum(c, k):
    def backtrack(candidatos: list, k: int):
        if candidatos == [] and k == 0:
            return True
        
        if k < 0 or candidatos == []:
            return False

        else:
            for candidato in candidatos:
                nuevos_candidatos = candidatos.copy()
                nuevos_candidatos.remove(candidato)
                nuevo_k = k - candidato
                res_sin = backtrack(nuevos_candidatos, k)
                res_con = backtrack(nuevos_candidatos, nuevo_k)
                return res_sin or res_con
    
    return backtrack(c, k)
#print(subset_sum([6,0,5], 12))

def n_reinas(n):
    tablero = [[None for _ in range(n)] for _ in range(n)]

    def es_valido(tablero, fila, casillero):
        nonlocal n
        # Fila
        if True in tablero[fila]:
            return False
            
        # Columna
        for columna in range(n):
            if tablero[columna][casillero]:
                return False
        
        # Diagonal1
        i0 = fila - 1
        j0 = casillero - 1
        i1 = fila + 1
        j1 = casillero + 1
        while i0 in range(n) and j0 in range(n):
            if tablero[i0][j0]:
                return False
            i0 -= 1
            j0 -= 1

        while i1 in range(n) and j1 in range(n):
            if tablero[i1][j1]:
                return False
            i1 += 1
            j1 += 1
            
        # Diagonal2
        i0 = fila + 1
        j0 = casillero - 1
        i1 = fila - 1
        j1 = casillero + 1
        while i0 in range(n) and j0 in range(n):
            if tablero[i0][j0]:
                return False
            i0 += 1
            j0 -= 1

        while i1 in range(n) and j1 in range(n):
            if tablero[i1][j1]:
                return False
            i1 -= 1
            j1 += 1

        return True
    
    def agregar_falsos(tablero, fila, casillero):
        nonlocal n
        # Fila
        for i in range(n):
            if i != casillero:
                tablero[fila][i] = False
        
        # Columna
        for i in range(n):
            if i != fila:
                tablero[i][casillero] = False

        # Diagonal1
        i0 = fila - 1
        j0 = casillero - 1
        i1 = fila + 1
        j1 = casillero + 1
        while i0 in range(n) and j0 in range(n):
            tablero[i0][j0] = False
            i0 -= 1
            j0 -= 1

        while i1 in range(n) and j1 in range(n):
            tablero[i1][j1] = False
            i1 += 1
            j1 += 1
            
        # Diagonal2
        i0 = fila + 1
        j0 = casillero - 1
        i1 = fila - 1
        j1 = casillero + 1
        while i0 in range(n) and j0 in range(n):
            tablero[i0][j0] = False
            i0 += 1
            j0 -= 1

        while i1 in range(n) and j1 in range(n):
            tablero[i1][j1] = False
            i1 -= 1
            j1 += 1

        return tablero


    def backtrack(tablero: list[bool], fila_actual, reinas):
        nonlocal n
        if reinas == 0:
            res = [None for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if tablero[i][j]:
                        res[j] = i + 1
            if None not in res:
                print(res)
        elif fila_actual < n:
            for casillero in range(n):
                if tablero[fila_actual][casillero] == False:
                    continue
                if es_valido(tablero, fila_actual, casillero):
                    nuevo_tablero = [row.copy() for row in tablero]
                    nuevo_tablero[fila_actual][casillero] = True
                    tablero_terminado = agregar_falsos(nuevo_tablero, fila_actual, casillero)
                    nueva_r = reinas - 1
                    backtrack(tablero_terminado, fila_actual + 1, nueva_r)

    backtrack(tablero, 0, n)

#n_reinas(5)

def sudoku_4(sudoku):
    candidatos = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
    for fila in sudoku:
        for num in fila:
            if num != 0:
                candidatos.remove(num)
    
    def acomodar_indices(i, j):
        j += 1
        if j == 4:
            i += 1
            j = 0
        return i, j
    
    def es_valido(sudoku, i, j, candidato):
        # Esta vacio
        if sudoku[i][j] != 0:
            return False
        
        # Fila
        if candidato in sudoku[i]:
            return False
        
        # Columna
        for fila in range(4):
            if sudoku[fila][j] == candidato:
                return False
        
        # Subcuadrado
        bi = i//2 * 2
        bj = j//2 * 2
        for r in range(bi, bi+2):
            for c in range(bj, bj+2):
                if sudoku[r][c] == candidato:
                    return False
        
        return True

    def backtrack(sudoku, i, j, candidatos: list):
        if i == 4:
            for fila in sudoku:
                print(fila)
            return True
        if sudoku[i][j] != 0:
            ni, nj = acomodar_indices(i, j)
            return backtrack(sudoku, ni, nj, candidatos)
        else:
            for candidato in set(candidatos):
                if es_valido(sudoku, i, j, candidato):
                    nuevos_candidatos = candidatos.copy()
                    nuevo_sudoku = [row.copy() for row in sudoku]
                    nuevos_candidatos.remove(candidato)
                    nuevo_sudoku[i][j] = candidato
                    ni, nj = acomodar_indices(i, j)
                    if backtrack(nuevo_sudoku, ni, nj, nuevos_candidatos):
                        return True
        return None
    
    backtrack(sudoku, 0, 0, candidatos)

#sudoku_4([[0,0,0,1],
#          [0,0,0,3],
#          [0,0,0,2],
#          [0,0,0,4]])

def cuadrados_magicos(n: int):
    cuadrado = [[None for _ in range(n)] for _ in range(n)]
    candidatos = [k+1 for k in range(n**2)]
    num_mag = (n**3 + n) // 2
    k = 1

    def actualizar_indices(i, j):
        nonlocal n
        j += 1
        if j == n:
            i += 1
            j = 0
        return i, j
    
    def algo_completo(cuadrado, i, j, candidato, op):
        nonlocal num_mag, n
        suma = candidato
        if op == 0:
            for fj in range(j):
                suma += cuadrado[i][fj]
            return suma == num_mag
        elif op == 1:
            for fi in range(i):
                suma += cuadrado[fi][j]
            return suma == num_mag
        elif op == 2:
            for fi in range(n - 1):
                suma += cuadrado[fi][n - 1 - fi]
            return suma == num_mag
        elif op == 3:
            for fi in range(n - 1):
                suma += cuadrado[fi][fi]
            return suma == num_mag
    
    def es_valido(cuadrado, i, j, candidato):
        nonlocal n, num_mag
        if j == n - 1 and not algo_completo(cuadrado, i, j, candidato, 0):
            return False
        if i == n - 1 and not algo_completo(cuadrado, i, j, candidato, 1):
            return False
        if (i == n - 1 and j == 0) and not algo_completo(cuadrado, i, j, candidato, 2):
            return False
        if i == j == n - 1 and not algo_completo(cuadrado, i, j, candidato, 3):
            return False
        else:
            # Fila
            suma = candidato
            for fj in range(j):
                suma += cuadrado[i][fj]
                if suma > num_mag:
                    return False
            
            # Columna
            suma = candidato
            for fi in range(i):
                suma += cuadrado[fi][j]
                if suma > num_mag:
                    return False
            
            # Diagonal1
            if i + j == n - 1:
                suma = candidato
                for fi in range(i):
                    suma += cuadrado[fi][n - 1 - fi]
                    if suma > num_mag:
                        return False
                    
            # Diagonal2
            if i == j:
                suma = candidato
                for fi in range(i):
                    suma += cuadrado[fi][fi]
                    if suma > num_mag:
                        return False
            
        return True


    def backtrack(cuadrado: list[list[int]], i, j, candidatos: list):
        nonlocal num_mag, k
        if i == n:
            print("Solucion: " + str(k))
            for row in cuadrado:
                print(row)
            k += 1
            return
        else:
            for candidato in candidatos:
                if es_valido(cuadrado, i, j, candidato):
                    nuevo_cuadrado = [row.copy() for row in cuadrado]
                    nuevos_candidatos = candidatos.copy()
                    nuevos_candidatos.remove(candidato)
                    nuevo_cuadrado[i][j] = candidato
                    ni, nj = actualizar_indices(i, j)
                    backtrack(nuevo_cuadrado, ni, nj, nuevos_candidatos)
        return None

    backtrack(cuadrado, 0, 0, candidatos)

#cuadrados_magicos(3)

def maxi_subconjuto(matriz: list[list], k):
    n = len(matriz)
    mejor_conjunto = []
    mejor_valor = float("-inf")
    cotas = [0 for _ in range(len(matriz))]
    for i0 in range(len(matriz)):
        copia = matriz[i0].copy()
        for _ in range(k - 1):
            cotas[i0] += max(copia)
            copia.remove(max(copia))
    order = sorted(range(n), key=lambda i: cotas[i], reverse=True)

    def aporte(candidato, res):
        nonlocal matriz
        return sum(matriz[candidato][e] for e in res)
    
    def cota_superior(suma_parcial, pos, faltan):
        if faltan <= 0:
            return suma_parcial
        
        candidato = [cotas[order[t]] for t in range(pos, n)]
        candidato.sort(reverse=True)
        return suma_parcial + sum(candidato[:faltan])



    def backtrack(res: list, suma_parcial, pos):
        nonlocal n, cotas, matriz, k, mejor_valor, mejor_conjunto
        if len(res) == k:
            if suma_parcial > mejor_valor:
                mejor_valor = suma_parcial
                mejor_conjunto = res[:]
            return
        
        if pos >= n:
            return
        
        faltan = k - len(res)

        if len(res) + (n - pos) < k:
            return
        
        if cota_superior(suma_parcial, pos, faltan) <= mejor_valor:
            return

        i = order[pos]
        backtrack(res + [i], suma_parcial + aporte(i, res), pos+1)

        backtrack(res, suma_parcial, pos+1)

    backtrack([], 0, 0)
    return mejor_valor, sorted([i+1 for i in mejor_conjunto])

#print(maxi_subconjuto([[0,9,1,2],[9,0,3,4],[1,3,0,8],[2,4,8,0]], 3))

def ruta_minima(matriz: list[list]):
    # Hay que corregir la cota, pq hay una de las ciudad q tengo en cuenta q va a ser la ultima ciudad y no va a tener costo de salida
    # O habria que modificar la idea del algoritmo para que vuelva a la ciudad de origen o que vuelva a una ciudad fija
    # En general esta bien
    n = len(matriz)
    mejor_costo = float("inf")
    mejor_ruta = []
    minimos_por_ciudad = []
    for fila in matriz:
        copia = fila.copy()
        copia.remove(0)
        minimos_por_ciudad.append(min(copia))

    def determinar_cota(ruta_parcial: list[int], costo_parcial):
        suma_costos_minimos = 0
        for ciudad in range(n):
            if ciudad in ruta_parcial:
                continue
            suma_costos_minimos += minimos_por_ciudad[ciudad]
        return costo_parcial + suma_costos_minimos

    def backtrack(ruta_parcial, costo_parcial):
        nonlocal mejor_costo, mejor_ruta
        if len(ruta_parcial) == n:
            if costo_parcial < mejor_costo:
                mejor_costo = costo_parcial
                mejor_ruta = ruta_parcial
        else:
            cota = determinar_cota(ruta_parcial, costo_parcial)
            if cota >= mejor_costo:
                return
            
            for candidato in range(n):
                if candidato in ruta_parcial:
                    continue
                if len(ruta_parcial) == 0:
                    backtrack(ruta_parcial + [candidato], 0)
                else:
                    backtrack(ruta_parcial + [candidato], costo_parcial + matriz[ruta_parcial[-1]][candidato])
            
            

    backtrack([], 0)
    return mejor_ruta, mejor_costo

M = [
  [0, 4, 1],
  [2, 0, 5],
  [3, 1, 0]
]
print(ruta_minima(M))

M = [
  [0, 10, 15, 20],
  [5, 0,  9, 10],
  [6, 13, 0, 12],
  [8,  8,  9, 0]
]
print(ruta_minima(M))

M = [
  [0, 50, 1, 100],
  [2, 0, 50, 3],
  [100, 2, 0, 4],
  [1, 100, 2, 0]
]
print(ruta_minima(M))

M = [
  [0, 14, 4, 10, 20],
  [5, 0, 7, 8, 7],
  [9, 6, 0, 12, 8],
  [8, 5, 6, 0, 10],
  [7, 8, 6, 9, 0]
]
print(ruta_minima(M))