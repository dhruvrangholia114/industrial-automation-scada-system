from flask import Flask, jsonify, render_template, request
from plc_simulator import PLCSimulator

app = Flask(__name__)
plc = PLCSimulator()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/status")
def status():
    return jsonify(plc.status())

@app.post("/api/control")
def control():
    try:
        return jsonify(plc.set_control(request.get_json(silent=True) or {}))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.post("/api/simulate")
def simulate():
    try:
        return jsonify(plc.simulate(request.get_json(silent=True) or {}))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": "Simulation values must be numbers or booleans"}), 400

@app.post("/api/acknowledge")
def acknowledge():
    return jsonify(plc.acknowledge())

if __name__ == "__main__":
    app.run(debug=True)
