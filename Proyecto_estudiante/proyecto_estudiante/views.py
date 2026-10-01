import os

from models import Estudiante
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# crea la carpeta data si no existe
os.makedirs("data", exist_ok=True)

gestor = GestorJSON("data/estudiantes.json")

# tuplas con los campos (no cambian)
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# ---------- funciones de ayuda ----------

def emails_registrados(excepto_id=None):
    # set con los emails que ya existen
    emails = set()
    for r in gestor.leer():
        if r["id"] != excepto_id:
            emails.add(r["email"].lower())
    return emails


def carnets_registrados(excepto_id=None):
    # set con los carnets que ya existen
    carnets = set()
    for r in gestor.leer():
        if r["id"] != excepto_id:
            carnets.add(r["carnet"].lower())
    return carnets


def siguiente_id():
    registros = gestor.leer()
    if not registros:
        return 1
    ids = [r["id"] for r in registros]
    return max(ids) + 1


# ---------- CREAR ----------

def crear_estudiante(datos):
    try:
        # limpio los espacios de cada campo
        valores = {}
        for campo in CAMPOS_ESTUDIANTE:
            valores[campo] = str(datos.get(campo, "")).strip()

        # reviso que no falte ningún campo
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if not valores[c]]
        if faltantes:
            return False, "Faltan campos obligatorios: " + ", ".join(faltantes)

        if not es_email_valido(valores["email"]):
            return False, "El email no tiene un formato válido"

        # reviso duplicados con los sets
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # creo el objeto y lo guardo
        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        gestor.guardar(registros)

        # compruebo que se guardó
        ids = [r["id"] for r in gestor.leer()]
        if estudiante.id not in ids:
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error: {error}"


# ---------- LEER ----------

def obtener_todos():
    estudiantes = []
    for r in gestor.leer():
        estudiantes.append(Estudiante.desde_diccionario(r))
    return estudiantes


def obtener_por_id(id_estudiante):
    for e in obtener_todos():
        if e.id == id_estudiante:
            return e
    return None


# ---------- BUSCAR ----------

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for r in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(r.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(r))
                break  # ya coincidió, paso al siguiente
    return encontrados


# ---------- ACTUALIZAR ----------

def actualizar_estudiante(id_estudiante, cambios):
    try:
        if not cambios:
            return False, "No se indicó ningún cambio"

        # diferencia de sets: campos que no existen
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, "Campos no válidos: " + ", ".join(sorted(desconocidos))

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            if cambios["carnet"].lower() in carnets_registrados(id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        for r in registros:
            if r["id"] == id_estudiante:
                r.update(cambios)
                gestor.guardar(registros)
                return True, f"Estudiante {id_estudiante} actualizado"

        return False, f"No existe un estudiante con id {id_estudiante}"

    except Exception as error:
        return False, f"Error: {error}"


# ---------- ELIMINAR ----------

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()

    # lista nueva sin el estudiante a eliminar
    quedan = [r for r in registros if r["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"
# ---------- NOTAS Y MATERIAS ----------

def agregar_nota(id_estudiante, materia, nota):
    # convierto la nota a número
    try:
        nota = float(nota)
    except ValueError:
        return False, "La nota debe ser un número"

    # la nota va de 0 a 100
    if nota < 0 or nota > 100:
        return False, "La nota debe estar entre 0 y 100"

    materia = materia.strip().title()
    if materia == "":
        return False, "La materia no puede estar vacía"

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, "No existe ese estudiante"

    # si la nota ya está en esa materia, no la repito
    if materia in estudiante.notas:
        if nota in estudiante.notas[materia]:
            return False, "Esa nota ya está registrada en " + materia

    estudiante.agregar_nota(materia, nota)

    # guardo el estudiante actualizado
    registros = gestor.leer()
    for i in range(len(registros)):
        if registros[i]["id"] == id_estudiante:
            registros[i] = estudiante.a_diccionario()
    gestor.guardar(registros)

    return True, "Nota agregada en " + materia


def obtener_promedio(id_estudiante):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, "No existe ese estudiante"
    return True, estudiante.obtener_promedio()


def materias_ofertadas():
    # unión de las materias de todos (el set no repite)
    materias = set()
    for e in obtener_todos():
        materias = materias | e.materias
    return materias


def estudiantes_en_comun(id_a, id_b):
    a = obtener_por_id(id_a)
    b = obtener_por_id(id_b)
    if a is None or b is None:
        return False, "Uno de los dos estudiantes no existe"

    # intersección de sets
    return True, a.materias_en_comun(b)
