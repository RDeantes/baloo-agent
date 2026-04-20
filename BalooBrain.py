import os
import subprocess

import openpyxl


# 🐻 Personalidad Baloo (solo para texto)
def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


# 🎯 FUNCIÓN PRINCIPAL (IMPORTANTE: ESTA ES LA QUE SE IMPORTA)
def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        return generar_acta(texto)  # 🔥 REGRESA RUTA DEL ARCHIVO

    elif "asistencia" in texto_lower:
        return personalidad_baloo(agregar_asistencia(texto))

    else:
        return personalidad_baloo(
            "No entendí 🤔 intenta así:\nacta Juan Pérez 10/04/2026 mesero"
        )


# 📄 GENERAR ACTA EN WORD
def generar_acta(texto):
    try:
        partes = texto.split()

        # 🔍 Buscar fecha
        fecha = None
        for p in partes:
            if "/" in p:
                fecha = p
                break

        if not fecha:
            return "No encontré la fecha ❌ usa formato dd/mm/yyyy"

        fecha_index = partes.index(fecha)

        # 👤 Nombre completo
        nombre = " ".join(partes[1:fecha_index])

        # 💼 Puesto
        puesto = " ".join(partes[fecha_index + 1:])

        if not nombre or not puesto:
            return "Formato incorrecto ❌ usa:\nacta Juan Pérez 10/04/2026 mesero"

        # 🔥 LIMPIEZA
        nombre_limpio = nombre.replace(" ", "_")
        fecha_limpia = fecha.replace("/", "-")

        # 📁 RUTA SEGURA (clave en Railway)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        template = os.path.join(BASE_DIR, "Acta_Administrativa_Falta_Injustificada_Membretada(1).docx")
        output = os.path.join(
            BASE_DIR,
            f"Acta_{nombre_limpio}_{fecha_limpia}.docx"
        )

        # 🚀 Ejecutar script que llena el Word
        resultado = subprocess.run(
    [
        "python",
        os.path.join(BASE_DIR, "llena actas.py"),
        "--template", template,
        "--output", output,
        "--empleado", nombre,
        "--puesto", puesto,
        "--fecha", fecha
    ],
        capture_output=True,
        text=True
    )

        print("STDOUT:", resultado.stdout)
        print("STDERR:", resultado.stderr)

        if resultado.returncode == 0:
            return output  # 🔥 CLAVE: ruta del archivo

        elif resultado.stderr:
            return f"❌ Error al generar acta:\n{resultado.stderr}"

        else:
            return "❌ No se generó el acta correctamente"

    except Exception as e:
        return f"❌ Error al generar acta: {str(e)}"


# 📊 AGREGAR ASISTENCIA
def agregar_asistencia(texto):
    partes = texto.split()

    if partes[0].lower() == "asistencia":
        partes.pop(0)

    if len(partes) < 2:
        return "Formato incorrecto ❌ usa:\nasistencia Juan Perez administrativos"

    nombre_completo = " ".join(partes[:-1])
    area = partes[-1]

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo_excel = os.path.join(BASE_DIR, "LISTA DE ASISTENCIA.xlsx")

        libro = openpyxl.load_workbook(archivo_excel)
        hoja = libro[area]

        ultima_fila = hoja.max_row + 1

        hoja[f"A{ultima_fila}"] = nombre_completo

        libro.save(archivo_excel)

        return f"✅ {nombre_completo} agregado correctamente a la lista de asistencia."

    except Exception as e:
        return f"❌ Error al agregar asistencia: {str(e)}"
