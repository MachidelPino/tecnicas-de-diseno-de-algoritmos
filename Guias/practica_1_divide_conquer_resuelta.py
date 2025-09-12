# Ejercicio 1 # ⋆
# 1.1 #
def merge_sort ( arr ):
    if len ( arr ) <= 1:
        return arr

    medio = len ( arr ) // 2                    # Divide
    mitad_izq = merge_sort ( arr [: medio ])    # Conquer
    mitad_der = merge_sort ( arr[ medio :])     # Conquer

    return merge ( mitad_izq , mitad_der )      # Combine (Todo merge es el combine)

def merge (izq , der ):
    mergeados = []
    i = j = 0

    while i < len ( izq ) and j < len (der ):   
        if izq [i] < der[j]:
            mergeados . append (izq[i])         
            i += 1
        else:
            mergeados . append (der[j])         
            j += 1

    mergeados . extend ( izq[i:])               
    mergeados . extend ( der[j:])               
    return mergeados
# 1.2 #
# Se divide en dos subproblemas

# 1.3 #
# El tamaño de los subproblemas es la mitad del problema original

# 1.4 #
# Costo por combinar el resultado: O(n)

# 1.5 #
# T(n) = 2T(n/2) + O(n)

# 1.6 #
# Θ(n log n)

# Ejercicio 2 # ⋆
# 2.1 #
arr=[]
def busqueda_binaria (arr , objetivo , izq = 0, der = len (arr) -1):    # type: ignore
    if izq > der :
        return False # Elemento no encontrado

    medio = (izq + der ) // 2                                           # Divide
    if arr [ medio ] == objetivo :
        return medio
    elif arr [ medio ] > objetivo :
        return busqueda_binaria (arr , objetivo , izq , medio - 1)      # Conquer
    else:
        return busqueda_binaria (arr , objetivo , medio + 1, der)       # Conquer
# No tiene combine ya que no combina resultados parciales

# 2.2 #
# Se divide en 1 subproblema, ya que decide cual mitad analizar

# 2.3 #
# n // 2

# 2.4 #
# O(1)

# 2.5 #
# T(n) = T(n/2) + O(1)

# 2.6 #
# Θ(log n)

# Ejercicio 3 # ⋆
def izquierda_dominante(arr):
    long = len(arr)
    if long <= 1:
        return True
    elif long == 2:
        return arr[0] > arr[1]
    else:
        medio = long // 2                       # Divide  
        sumai = sum(arr[:medio])                # Conquer O(n/2)
        sumad = sum(arr[medio:])                # Conquer O(n/2)
        izq = izquierda_dominante(arr[:medio])  # Conquer
        der = izquierda_dominante(arr[medio:])  # Conquer

        return sumai > sumad and izq and der    # Combine
# Complejidad: T(n) = 2T(n/2) + O(1)
# Por teorema maestro: Θ(n log n)

# Ejercicio 4 # ⋆
def indice_espejo(arr):
    def indice_espejo_aux(arr, izq, der):
        if izq > der:
            return None
        else:
            mid = (izq + der) // 2
            if arr[mid] == mid + 1:
                return mid + 1
            elif arr[mid] < mid + 1:
                return indice_espejo_aux(arr, mid + 1, der)
            else:
                return indice_espejo_aux(arr, izq, mid - 1)
    return indice_espejo_aux(arr, 0, len(arr) - 1)

# Ejercicio 5 # ⋆
def potencia_logaritmica(a, b):
    if b == 0:
        return 1
    
    res = 1
    base = a
    while b > 0:
        if b & 1 == 1: res = res * base
        base = base * base
        b = b // 2
    return res

# Ejercicio 7 # ⋆
# En hoja #

# Ejercicio 8 # ⋆
def maxima_subsecuencia(A):
    def max_subfijo_izq(arr):
        
        i = len(arr) - 1
        suma = arr[i]

        while i > 0 and suma < suma + arr[i - 1]:
            suma += arr[i - 1]
            i += -1

        return suma
    
    def max_prefijo_der(arr):
        
        i = 0
        suma = arr[i]

        while i < len(arr) - 1 and suma < suma + arr[i + 1]:
            suma += arr[i + 1]
            i += 1

        return suma

    if len(A) == 1:
        return A[0]
    
    mid = len(A) // 2
    mejor_izq = maxima_subsecuencia(A[:mid])
    mejor_der = maxima_subsecuencia(A[mid:])
    mejor_medio = max_subfijo_izq(A[:mid]) + max_prefijo_der(A[mid:])

    mejor = max(mejor_izq, mejor_der, mejor_medio)
    return mejor

# Ejercicio 9 # ⋆
def potencia_sum(A, n, potencia, prod_matriz, suma_matriz):
    if n == 1:
        return A
    
    m = n // 2
    Sm = potencia_sum(A, m, potencia, prod_matriz, suma_matriz)
    Am = potencia(A, m)

    return suma_matriz(Sm, prod_matriz(Am, Sm))

# Ejercicio 10 # ⋆
class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der
    
def distancia_maxima(abb: Nodo):
    if abb is None:
        return -1, 0
    
    h_izq, d_izq = distancia_maxima(abb.izq)
    h_der, d_der = distancia_maxima(abb.der)

    altura = 1 + max(h_izq, h_der)
    diametro = max(d_izq, d_der, h_izq + h_der + 2)
    
    return altura, diametro

# Ejercicio 11 # ⋆
def desorden_sort(arr):
    if len ( arr ) <= 1:
        return arr, 0
    
    medio = len ( arr ) // 2                    # Divide
    mitad_izq, res_izq = desorden_sort( arr [: medio ])    # Conquer
    mitad_der, res_der = desorden_sort( arr[ medio :])     # Conquer
    merged, res_merged = merge_desorden(mitad_izq, mitad_der)     # Combine (Todo merge es el combine)
    
    return merged, res_izq + res_der + res_merged

def merge_desorden (izq , der ):
    mergeados = []
    i = j = 0
    res = 0

    while i < len ( izq ) and j < len (der ):   
        if izq [i] <= der[j]:
            mergeados . append (izq[i])         
            i += 1
        else:
            mergeados . append (der[j])         
            j += 1
            res += len(izq) - i

    mergeados . extend ( izq[i:])               
    mergeados . extend ( der[j:])               
    return mergeados, res

# Ejercicio 12 # ⋆
# 12.1 #
def pos_false(matriz):
    n = len(matriz)
    if n == 0 or len(matriz[0]) == 0:
        return None

    def pos_false_aux(i0, i1, j0, j1):
        if conjuncion_submatriz(matriz, i0, i1, j0, j1):
            return None

        if (i1 - i0 == 1) and (j1 - j0 == 1):
            return (i0, j0)

        mi = (i0 + i1) // 2
        mj = (j0 + j1) // 2

        res = pos_false_aux(i0, mi, j0, mj)
        if res is not None:
            return res

        res = pos_false_aux(i0, mi, mj, j1)
        if res is not None:
            return res

        res = pos_false_aux(mi, i1, j0, mj)
        if res is not None:
            return res

        return pos_false_aux(mi, i1, mj, j1)

    return pos_false_aux(0, n, 0, len(matriz[0]))

def conjuncion_submatriz(matriz, i0, i1, j0, j1):
    for i in range(i0, i1):
        for j in range(j0, j1):
            if not matriz[i][j]:
                return False
    return True

# 12.2 #
def contar_falsos(m):
    def contar_falsos_aux(m, i0, i1, j0, j1):
        if conjuncion_submatriz(m, i0, i1, j0, j1):
            return 0
        
        if (i1 - i0 == 1) and (j1 - j0 == 1):
            return 1

        mi = (i0 + i1) // 2
        mj = (j0 + j1) // 2
        return  contar_falsos_aux(m, i0, mi, j0, mj) + contar_falsos_aux(m, i0, mi, mj, j1) + contar_falsos_aux(m, mi, i1, j0, mj) + contar_falsos_aux(m, mi, i1, mj, j1)

    return contar_falsos_aux(m, 0, len(m), 0, len(m))