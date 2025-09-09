# Ejercicio 1 #
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

# Ejercicio 2 #
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

# Ejercicio 3 #
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

# Ejercicio 4 #
