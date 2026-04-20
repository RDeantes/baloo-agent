import os
import subprocess
import openpyxl 

# 🐻 Personalidad Baloo (solo para mensajes de texto)
def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


# 🎯 FUNCIÓN PRINCIPAL
def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        # 🔥 IMPORTANTE: regresar SOLO la ruta del archivo
        return generar_acta(texto)

    elif "asistencia" in texto_lower:
        return personalidad_baloo(agregar_asistencia(texto))

    else:
        return personalidad_baloo(
            "No entendí 🤔 intenta así:\nacta Juan Pérez 10/04/2026 mesero"
        )


# 📄 FUNCIÓN QUE GENERA ACTA
def generar_acta(texto):
    try:
        partes = texto.split()

        # 🔍 Buscar la fecha
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

        # 📁 RUTA SEGURA (IMPORTANTE EN RAILWAY)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        template = os.path.join(BASE_DIR, "Acta_Administrativa_Falta_Injustificada_Membretada(1).docx")
        output = os.path.join(BASE_DIR, f"Acta_{nombre_limpio}_{fecha_limpia}.docx")

        resultado = subprocess.run(
            [
                "python",
                "llena actas.py",  # si falla, renómbralo a llena_actas.py
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
            return output  # 🔥 CLAVE

        elif resultado.stderr:
            return f"❌ Error al generar acta:\n{resultado.stderr}"

        else:
            return "❌ No se generó el acta correctamente"

    except Exception as e:
        return f"Error al generar acta: {str(e)}"


# 📊 AGREGAR ASISTENCIA
def agregar_asistencia(texto):          
    partes = texto.split()

    if partes[0].lower() == "asistencia":
        partes.pop(0)

    nombre_completo = " ".join(partes[:-1])
    area = partes[-1]

    try:
        libro = openpyxl.load_workbook("LISTA DE ASISTENCIA.xlsx")
        hoja = libro[area]

        ultima_fila = hoja.max_row + 1

        hoja[f"A{ultima_fila}"] = nombre_completo

        libro.save("LISTA DE ASISTENCIA.xlsx")

        return f"✅ {nombre_completo} agregado correctamente a la lista de asistencia."

    except Exception as e:
        return f"❌ Error al agregar asistencia: {str(e)}"
