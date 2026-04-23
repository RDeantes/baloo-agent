import os
import subprocess
import openpyxl


def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        return generar_acta(texto)

    elif "asistencia" in texto_lower:
        return personalidad_baloo(agregar_asistencia(texto))

    else:
        return personalidad_baloo(
            "No entendí 🤔 intenta así:\nacta Juan Pérez 10/04/2026 mesero"
        )


def generar_acta(texto):
    try:
        partes = texto.split()

        fecha = next((p for p in partes if "/" in p), None)
        if not fecha:
            return "No encontré la fecha ❌ usa formato dd/mm/yyyy"

        fecha_index = partes.index(fecha)

        nombre = " ".join(partes[1:fecha_index])
        puesto = " ".join(partes[fecha_index + 1:])

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        template = os.path.join(
            BASE_DIR,
            "Acta_Administrativa_Falta_Injustificada_Membretada(1).docx"
        )

        output = os.path.join(
            BASE_DIR,
            f"Acta_{nombre.replace(' ', '_')}_{fecha.replace('/', '-')}.docx"
        )

        resultado = subprocess.run(
            [
                "python",
                os.path.join(BASE_DIR, "llena_actas.py"),
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

    pdf_output = output.replace(".docx", ".pdf")

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", BASE_DIR,
        output
    ])

    return os.path.abspath(pdf_output)

        return f"❌ Error:\n{resultado.stderr}"

    except Exception as e:
        return f"❌ Error: {str(e)}"


def agregar_asistencia(texto):
    partes = texto.split()

    if partes[0].lower() == "asistencia":
        partes.pop(0)

    nombre = " ".join(partes[:-1])
    area = partes[-1]

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "LISTA DE ASISTENCIA.xlsx")

        libro = openpyxl.load_workbook(archivo)
        hoja = libro[area]

        fila = hoja.max_row + 1
        hoja[f"A{fila}"] = nombre

        libro.save(archivo)

        return f"✅ {nombre} agregado correctamente."

    except Exception as e:
        return f"❌ Error: {str(e)}"
