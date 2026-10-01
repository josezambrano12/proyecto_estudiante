from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    obtener_promedio, materias_ofertadas, estudiantes_en_comun
)

# campos que se piden al crear y actualizar
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_id(texto="Id del estudiante: "):
    # devuelve el id como número, o None si escribió otra cosa
    try:
        return int(input(texto))
    except ValueError:
        imprimir_error("El id debe ser un número")
        return None


def mostrar_estudiantes(lista):
    print(f"{'ID':<5}{'NOMBRE':<25}{'CARNET':<15}{'PROMEDIO':<10}")
    print("-" * 55)
    for e in lista:
        print(f"{e.id:<5}{e.obtener_nombre_completo():<25}{e.carnet:<15}{e.obtener_promedio():<10}")
    print("-" * 55)
    imprimir_info(f"Total: {len(lista)} estudiante(s)")


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def opcion_crear():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if estudiantes:
        mostrar_estudiantes(estudiantes)
    else:
        imprimir_info("No hay estudiantes registrados.")
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)
    if encontrados:
        mostrar_estudiantes(encontrados)
    else:
        imprimir_info("No se encontraron estudiantes.")
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return pausa()

    e = obtener_por_id(id_estudiante)
    if e is None:
        imprimir_error("No existe ese estudiante")
    else:
        print(f"Id:       {e.id}")
        print(f"Nombre:   {e.obtener_nombre_completo()}")
        print(f"Email:    {e.email}")
        print(f"Carnet:   {e.carnet}")
        print(f"Materias: {', '.join(sorted(e.materias))}")
        print(f"Promedio: {e.obtener_promedio()}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return pausa()

    e = obtener_por_id(id_estudiante)
    if e is None:
        imprimir_error("No existe ese estudiante")
        return pausa()

    print("Deje en blanco lo que no quiera cambiar")
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(e, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return pausa()

    e = obtener_por_id(id_estudiante)
    if e is None:
        imprimir_error("No existe ese estudiante")
        return pausa()

    print(e)
    if confirmar("¿Desea eliminarlo?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return pausa()

    materia = input("Materia: ")
    nota = input("Nota (0 - 100): ")
      # views valida que sea número entre 0 y 100

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    mostrar_resultado(exito, mensaje)
    pausa()


def opcion_promedio():
    imprimir_titulo("VER PROMEDIO")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return pausa()

    exito, resultado = obtener_promedio(id_estudiante)
    if exito:
        imprimir_info(f"Promedio: {resultado}")
    else:
        imprimir_error(resultado)
    pausa()


def opcion_materias_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    id_a = pedir_id("Id del primer estudiante: ")
    if id_a is None:
        return pausa()
    id_b = pedir_id("Id del segundo estudiante: ")
    if id_b is None:
        return pausa()

    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif resultado:
        for materia in sorted(resultado):
            print(f"- {materia}")
    else:
        imprimir_info("No tienen materias en común.")
    pausa()


def opcion_materias():
    imprimir_titulo("MATERIAS REGISTRADAS")
    materias = materias_ofertadas()
    if materias:
        for materia in sorted(materias):
            print(f"- {materia}")
    else:
        imprimir_info("Todavía no hay materias.")
    pausa()


def salir():
    imprimir_info("Programa finalizado.")
    return "salir"


# diccionario del menú: número -> (texto, función)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_promedio),
    "9": ("Materias en común", opcion_materias_comun),
    "10": ("Materias registradas", opcion_materias),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE ESTUDIANTES")
    for numero, (texto, funcion) in OPCIONES.items():
        print(f"{numero}. {texto}")


def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        texto, funcion = OPCIONES[opcion]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma cerrado.")