import os
import subprocess

# 🐻 Personalidad Baloo
def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


# 🎯 FUNCIÓN PRINCIPAL
def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        return personalidad_baloo(generar_acta(texto))

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

        # 🔥 LIMPIEZA DE DATOS (AQUÍ ESTÁ EL FIX)
        nombre_limpio = nombre.replace(" ", "_")
        fecha_limpia = fecha.replace("/", "-")

        template = "Acta_Administrativa_Falta_Injustificada_Membretada(1).docx"
        output = f"Acta_{nombre_limpio}_{fecha_limpia}.docx"

        resultado = subprocess.run(
            [
                "python",
                "llena actas.py",
                "--template", template,
                "--output", output,
                "--empleado", nombre,
                "--puesto", puesto,
                "--fecha", fecha
            ],
            capture_output=True,
            text=True
        )

        # Debug (puedes borrar luego)
        print("STDOUT:", resultado.stdout)
        print("STDERR:", resultado.stderr)

        if resultado.returncode == 0:
            return f"🎉 ¡Listo, pequeño amigo!\nTu acta ya quedó lista 🐻📄\nArchivo: {output}"

        elif resultado.stderr:
            return f"❌ Error al generar acta:\n{resultado.stderr}"

        else:
            return "❌ No se generó el acta correctamente"

    except Exception as e:
        return f"Error al generar acta: {str(e)}"
    
    
#AHORA QUIERO AGREGAR A UNA PERSONA A LA LISTA DE ASSITENCIA EN EL LIBRO DE EXCEL QUE SE LLAMA LISTA DE ASISTENCIA.XLSX EN LA HOJA QUE SE LLAMA ADMINISTRATIVOS Y LA COLUMNA A ES PARA LOS NOMBRES Y LA COLUMNA B PARA LAS FECHAS, LA PERSONA SE LLAMA JUAN PEREZ Y LA FECHA ES 10/04/2026
import openpyxl 

#con que palabra el agente reconoce que quiero usar esta funcion ?Puedes usar la palabra clave "asistencia" para que el agente reconozca que quieres usar la función de agregar asistencia. Por ejemplo, podrías enviar un mensaje como:
# "asistencia Juan Pérez" y el agente entenderá que deseas agregar la asistencia de Juan Pérez para esa fecha.



def agregar_asistencia(texto):          
    
    #como separo los argumentos del mensaje para que el agente sepa que el nombre es Juan Pérez y el area es administrativos ? Puedes enviar el mensaje con un formato específico para que el agente pueda separar los argumentos correctamente. Por ejemplo, podrías usar un formato como:
# "asistencia Juan Pérez administrativos" y el agente entenderá que "Juan Pérez" es el nombre y "administrativos" es el área. Luego, en tu función `agregar_asistencia`, puedes separar los argumentos de la siguiente manera:  
    partes = texto.split()
    nombre_completo = " ".join(partes[:-1])  # Esto toma todo excepto el último elemento como el nombre completo
    #si quiero quitarle la palabra asistencia antes del nombre como lo hago ? Puedes modificar la función `agregar_asistencia` para que elimine la palabra clave "asistencia" antes de procesar el nombre y el área. Aquí tienes un ejemplo de cómo hacerlo:
    if partes[0].lower() == "asistencia":
        partes.pop(0)  # Esto elimina la primera palabra "asistencia"
        nombre_completo = " ".join(partes[:-1])  # Esto toma todo excepto el último elemento como el nombre completo        
        area = partes[-1]  # Esto toma el último elemento como el área          



    
    try:
    
        # Cargar el libro de Excel
        libro = openpyxl.load_workbook("LISTA DE ASISTENCIA.xlsx")
        hoja = libro[area]

        # Encontrar la última fila con datos
        ultima_fila = hoja.max_row + 1

        # Agregar el nombre y la fecha en las columnas A y B respectivamente
        hoja[f"A{ultima_fila}"] = nombre_completo
        # Guardar los cambios en el libro de Excel
        libro.save("LISTA DE ASISTENCIA.xlsx")

        return f"✅ {nombre_completo} agregado correctamente a la lista de asistencia."

    except Exception as e:
        return f"❌ Error al agregar asistencia: {str(e)}"
    