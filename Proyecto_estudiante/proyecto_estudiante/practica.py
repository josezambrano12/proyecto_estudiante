# practica.py - ejercicios de colecciones

# ---------- Ejercicio 1: quitar repetidos sin perder el orden ----------
ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()   # aquí guardo las que ya salieron
unicas = []      # aquí guardo el resultado en orden

for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print("Ejercicio 1:", unicas)


# ---------- Ejercicio 2: contar con un diccionario ----------
conteo = {}

for ciudad in ciudades:
    if ciudad in conteo:
        conteo[ciudad] += 1
    else:
        conteo[ciudad] = 1

print("Ejercicio 2:", conteo)

# la ciudad que más se repite
mas_repetida = ""
maximo = 0
for ciudad in conteo:
    if conteo[ciudad] > maximo:
        maximo = conteo[ciudad]
        mas_repetida = ciudad

print("La más repetida:", mas_repetida)


# ---------- Ejercicio 3: conjuntos ----------
matematica = {"Ana", "Luis", "Sol", "Marco"}
ingles = {"Luis", "Marco", "Ruth"}

print("Ejercicio 3")
print("En las dos:", matematica & ingles)
print("Solo en matemática:", matematica - ingles)
print("Total de estudiantes distintos:", len(matematica | ingles))


# ---------- Ejercicio 4: lista de diccionarios a índice ----------
clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]

indice = {}
for c in clientes:
    indice[c["id"]] = c     # la clave es el id

print("Ejercicio 4:", indice[2]["nombre"])


# ---------- Ejercicio 5: tuplas ----------
ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]

total = 0
mejor_mes = ""
mejor_venta = 0

for mes, valor in ventas:   # saco el mes y el valor de cada tupla
    total += valor
    if valor > mejor_venta:
        mejor_venta = valor
        mejor_mes = mes

print("Ejercicio 5: el mejor mes fue", mejor_mes, "con", mejor_venta)
print("Total de ventas:", total)