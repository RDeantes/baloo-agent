import os
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 🐻 Personalidad Baloo
def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


# 🎯 FUNCIÓN PRINCIPAL
def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        return generar_acta_pdf(texto)  # 🔥 ahora PDF directo

    elif "asistencia" in texto_lower:
        return personalidad_baloo(agregar_asistencia(texto))

    else:
        return personalidad_baloo(
            "No entendí 🤔 intenta así:\nacta Juan Pérez 10/04/2026 mesero"
        )


# 📄 GENERAR ACTA EN PDF
def generar_acta_pdf(texto):
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

        # 👤 Nombre
        nombre = " ".join(partes[1:fecha_index])

        # 💼 Puesto
        puesto = " ".join(partes[fecha_index + 1:])

        if not nombre or not puesto:
            return "Formato incorrecto ❌ usa:\nacta Juan Pérez 10/04/2026 mesero"

        # 📁 Ruta segura
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(
            BASE_DIR,
            f"Acta_{nombre.replace(' ', '_')}_{fecha.replace('/', '-')}.pdf"
        )

        # 🧾 Crear PDF
        c = canvas.Canvas(archivo, pagesize=letter)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, 750, "ACTA ADMINISTRATIVA")

        c.setFont("Helvetica", 11)
        c.drawString(100, 700, f"Empleado: {nombre}")
        c.drawString(100, 680, f"Puesto: {puesto}")
        c.drawString(100, 660, f"Fecha de falta: {fecha}")

        c.drawString(100, 620, "Se hace constar que el empleado incurrió en una falta injustificada.")

        c.drawString(100, 580, "Firma del empleado: ______________________")
        c.drawString(100, 550, "Firma del gerente: _______________________")

        c.save()

        return archivo  # 🔥 CLAVE: regresar ruta

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
