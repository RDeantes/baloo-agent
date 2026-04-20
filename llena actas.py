from docx import Document
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--template")
parser.add_argument("--output")
parser.add_argument("--empleado")
parser.add_argument("--puesto")
parser.add_argument("--fecha")
args = parser.parse_args()

doc = Document(args.template)

# 📅 FECHAS
fecha_dt = datetime.strptime(args.fecha, "%d/%m/%Y")

datos = {
    "{{EMPLEADO}}": args.empleado,
    "{{PUESTO}}": args.puesto,
    "{{GERENTE}}": "Reyna Guadalupe Deantes Delgado",
    "{{FECHA}}": datetime.now().strftime("%d/%m/%Y"),
    "{{DIA}}": fecha_dt.strftime("%d"),
    "{{MES}}": fecha_dt.strftime("%B"),
    "{{ANIO}}": fecha_dt.strftime("%Y"),
}

# 🔥 REEMPLAZO PROFESIONAL (NO rompe formato)
for p in doc.paragraphs:
    for key, value in datos.items():
        if key in p.text:
            for run in p.runs:
                if key in run.text:
                    run.text = run.text.replace(key, value)

# 🔥 TAMBIÉN EN TABLAS
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for key, value in datos.items():
                if key in cell.text:
                    cell.text = cell.text.replace(key, value)

doc.save(args.output)
