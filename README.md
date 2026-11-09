# Industrial Automation & Monitoring System (PLC + SCADA Simulation)

A beginner-friendly, portfolio-ready **simulated** industrial automation project. It models a water tank, pump, level sensor, PLC scan cycle, alarms, and a browser HMI/SCADA dashboard.

> **Hardware note:** This project uses a Python PLC simulator—not a physical PLC, motor, or sensor. Python simulates the PLC logic and exposes telemetry/control through a small Flask API. The dashboard acts as the HMI/SCADA operator screen.

## What it demonstrates
- PLC scan-cycle concept: read inputs → execute logic → update outputs
- Automatic and manual pump modes
- Tank level monitoring (0–100%)
- High-level and low-level alarms
- Fault simulation and alarm acknowledgement
- HMI status, process values, mode, pump state, alarm list, and operator controls
- Basic troubleshooting and repeatable testing

## Requirements
- Python 3.10+
- pip

## Run
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Operator walkthrough
1. Start in **AUTO**. The pump starts when level falls below 30% and stops at 80% (hysteresis).
2. Use **Drain tank** to lower the level and observe the pump start.
3. Use **Fill tank** to raise the level; the pump stops at the high setpoint.
4. Select **MANUAL**, then switch the pump output ON/OFF.
5. Enable **Simulate sensor fault**. The controller stops the pump and raises an alarm.
6. Press **Acknowledge alarms**. Acknowledgement marks the alarm seen; it does not repair the fault.
7. Disable the fault and observe recovery.

## Project structure
```text
app.py                 Flask API + web server
plc_simulator.py       Simulated PLC scan cycle and control logic
templates/index.html   HMI/SCADA operator interface
static/style.css       Dashboard styling
static/app.js          HMI polling and operator actions
tests/test_plc.py      Basic automated logic tests
requirements.txt       Python dependencies
```

## Simplified control narrative
- **Input:** tank level sensor, simulated sensor-fault flag, operator mode/commands.
- **PLC logic:** In AUTO, pump starts below 30% and stops at/above 80%. In MANUAL, operator command controls the pump.
- **Interlocks:** pump cannot run if sensor fault is active or tank is at/above 95%.
- **Output:** pump motor command (simulated).
- **Alarm:** sensor fault, low level (<20%), high level (>=90%).
- **SCADA/HMI:** browser dashboard requests live values from Flask API every second and sends operator commands.

## API endpoints
- `GET /api/status` — current process data, outputs, mode, alarms
- `POST /api/control` — update mode or operator commands
- `POST /api/simulate` — alter simulated process conditions
- `POST /api/acknowledge` — acknowledge active alarm messages

## Limitations and safety
This is an educational simulation only. It is **not** connected to real equipment and must not be used to control industrial machinery. Real systems require a safety review, hardwired safety circuits, validated PLC code, and industrial network/security practices.

## Resume wording (accurate)
**Industrial Automation and Monitoring System (Python PLC/SCADA Simulation)** — Built a simulated PLC control loop for a water tank and pump, with automatic/manual operation, level monitoring, alarm handling, and a browser-based HMI/SCADA dashboard using Flask REST endpoints. Tested control thresholds, interlocks, and sensor-fault behavior with automated unit tests.
