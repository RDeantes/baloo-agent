


import argparse
from datetime import datetime
from docx import Document # type: ignore
import locale
import os
locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

parser = argparse.ArgumentParser(description='Llena actas administrativas')
parser.add_argument('--template', type=str, required=True, help='Ruta del archivo plantilla .docx')
parser.add_argument('--output', type=str, required=True, help='Ruta de salida para el acta generada')
parser.add_argument('--empleado', type=str, required=True, help='Nombre del empleado')
parser.add_argument('--puesto', type=str, required=True, help='Puesto del empleado')
parser.add_argument('--fecha', type=str, required=True, help='Fecha de la falta en formato dd/mm/yyyy')
args = parser.parse_args()

doc = Document(args.template)

# Parsear la fecha de la falta
try:
    falta_dt = datetime.strptime(args.fecha, "%d/%m/%Y")
except ValueError:
    print("La fecha debe estar en formato dd/mm/yyyy")
    exit(1)

FECHA = datetime.now().strftime("%d/%m/%Y")
HORA = datetime.now().strftime("%H:%M")
DIA = datetime.now().strftime("%d")
MES = datetime.now().strftime("%B").lower()
ANIO = datetime.now().strftime("%Y")

FALTA_DIA = falta_dt.strftime("%d")
FALTA_MES = falta_dt.strftime("%B").lower()
FALTA_ANIO = falta_dt.strftime("%Y")

datos_empleado = {
    "EMPLEADO": args.empleado,
    "PUESTO": args.puesto
}

datos = datos_empleado.copy()
datos.update({
    "FECHA": FECHA,
    "HORA": HORA,
    "DIA": DIA,
    "MES": MES,
    "ANIO": ANIO,
    "FALTA_DIA": FALTA_DIA,
    "FALTA_MES": FALTA_MES,
    "FALTA_ANIO": FALTA_ANIO
})


# Reemplazos de texto
for p in doc.paragraphs:
    texto = p.text

   # texto = texto.replace("_____/__________/_________", datos["FECHA"])
    #texto = texto.replace("______ horas", datos["HORA"] + " horas")
    #texto = texto.replace("día ____ de ______________ de ________", 
                        #  f'día {datos["DIA"]} de {datos["MES"]} de {datos["ANIO"]}')

    texto = texto.replace("Empleado(a): __________________________", 
                           f'Empleado(a): {datos["EMPLEADO"]}')
    texto = texto.replace("Puesto: _______________________________", 
                           f'Puesto: {datos["PUESTO"]}')
    texto = texto.replace("Supervisor / Gerente: ___________________", 
                          f'Supervisor / Gerente: {"Reyna Guadalupe Deantes Delgado"}')
   

    texto = texto.replace(
        "Se hace constar que el/la trabajador(a) ________________________________________, quien desempeña el puesto de ____________________________",
        f'Se hace constar que el/la trabajador(a) {datos["EMPLEADO"]} quien desempeña el puesto de {datos["PUESTO"]}'
    )
   

    
    
    
    # Reemplazos de texto
    for p in doc.paragraphs:
        texto = p.text
        texto = texto.replace("Empleado(a): __________________________", f'Empleado(a): {datos["EMPLEADO"]}')
        texto = texto.replace("Puesto: _______________________________", f'Puesto: {datos["PUESTO"]}')
        texto = texto.replace("Supervisor / Gerente: ___________________", f'Supervisor / Gerente: {"Reyna Guadalupe Deantes Delgado"}')
        texto = texto.replace(
            "Se hace constar que el/la trabajador(a) ________________________________________, quien desempeña el puesto de ____________________________",
            f'Se hace constar que el/la trabajador(a) {datos["EMPLEADO"]} quien desempeña el puesto de {datos["PUESTO"]}'
        )
        texto = texto.replace(
            "incurrió en una falta injustificada el día ____ de ______________ de ________",
            f'incurrió en una falta injustificada el día {datos["FALTA_DIA"]} de {datos["FALTA_MES"]} de {datos["FALTA_ANIO"]}'
        )
        p.text = texto

    # Guardar documento exactamente en la ruta y nombre proporcionados por --output
    doc.save(args.output)
    print(f"listo!!! Archivo guardado en: {args.output}")