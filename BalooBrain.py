def generar_acta(texto):
    # ... parseo de nombre/fecha/puesto

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(BASE_DIR, "acta_template_pro.docx")
    output = os.path.join(
        BASE_DIR,
        f"Acta_{nombre_limpio}_{fecha_limpia}.docx"
    )

    resultado = subprocess.run(
        [
            "python",
            "llena_actas.py",  # 👈 sin espacios
            "--template", template,
            "--output", output,
            "--empleado", nombre,
            "--puesto", puesto,
            "--fecha", fecha
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return output  # 🔥 ruta del archivo
    else:
        return f"❌ Error:\n{resultado.stderr}"
