from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener datos del formulario
        num_familias = int(request.form["num_familias"])
        consumo_total_kwh = float(request.form["consumo_total_kwh"])
        consumos_familias = [float(request.form[f"consumo_familia_{i + 1}"]) for i in range(num_familias)]

        # Calcular facturas
        facturas_familias = calcular_factura(consumos_familias, consumo_total_kwh, num_familias)
        return render_template("index.html", facturas=facturas_familias, total=sum(facturas_familias))

    return render_template("index.html", facturas=None, total=None)

def calcular_factura(consumos_familias, consumo_total_kwh, num_familias):
    precio_kwh = 0.6524  # Precio por kWh en S/
    cargo_fijo = 2.29 / num_familias
    mant_reposicion = 1.70 / num_familias
    alumbrado_publico = 20.76 / num_familias
    interes_compensatorio = 0.80 / num_familias

    subtotal_energia = sum((consumo / sum(consumos_familias) * consumo_total_kwh) * precio_kwh for consumo in consumos_familias)
    subtotal = subtotal_energia + cargo_fijo + mant_reposicion + alumbrado_publico + interes_compensatorio

    # Aplicar descuento a la última familia
    if num_familias > 0:
        descuento = subtotal * 0.10
        subtotal -= descuento
        facturas_familias = [subtotal / num_familias] * num_familias
        facturas_familias[-1] += descuento
        return facturas_familias

    return []

if __name__ == "__main__":
    app.run(debug=True)
