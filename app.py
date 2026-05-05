from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UNITS = {
    "m":  1,
    "cm": 1e-2,
    "mm": 1e-3,
    "µm": 1e-6,
    "nm": 1e-9,
}

def convert(value_m, unit):
    return value_m / UNITS[unit]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        image_size  = float(data["image_size"])
        magnification = float(data["magnification"])
        input_unit  = data["input_unit"]
        output_unit = data["output_unit"]

        if magnification == 0:
            return jsonify({"error": "Magnification cannot be zero."}), 400
        if image_size <= 0:
            return jsonify({"error": "Image size must be a positive number."}), 400

        # Convert image size to metres, then divide by magnification
        image_size_m  = image_size * UNITS[input_unit]
        actual_size_m = image_size_m / magnification
        actual_size   = convert(actual_size_m, output_unit)

        # Build a neat human-readable result
        def fmt(v):
            if v == 0:
                return "0"
            if 0.001 <= abs(v) < 1e6:
                return f"{v:,.6g}"
            return f"{v:.4e}"

        return jsonify({
            "actual_size": fmt(actual_size),
            "output_unit": output_unit,
            "formula": f"{image_size} {input_unit} ÷ {magnification:g}× = {fmt(actual_size)} {output_unit}"
        })

    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

if __name__ == "__main__":
    print("🔬  Organism Size Calculator running at http://127.0.0.1:5000")
    app.run(debug=True)