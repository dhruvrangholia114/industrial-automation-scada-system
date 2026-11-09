"""A small, educational PLC scan-cycle simulator for a tank/pump process."""
from dataclasses import dataclass, asdict
from time import time

@dataclass
class PLCState:
    level: float = 55.0
    mode: str = "AUTO"
    pump_on: bool = False
    manual_command: bool = False
    sensor_fault: bool = False
    acknowledged: bool = False
    last_scan: float = 0.0

class PLCSimulator:
    """Simulates inputs, PLC logic, outputs, and alarm bits."""
    START_LEVEL = 30.0
    STOP_LEVEL = 80.0
    HIGH_HIGH = 95.0
    LOW_ALARM = 20.0
    HIGH_ALARM = 90.0

    def __init__(self):
        self.state = PLCState()
        self._last_tick = time()

    def scan(self, elapsed=1.0):
        s = self.state
        # Simulated process: pump fills; an external drain slowly removes water.
        if s.pump_on:
            s.level = min(100.0, s.level + 2.0 * elapsed)
        else:
            s.level = max(0.0, s.level - 0.15 * elapsed)

        # PLC control logic (the scan-cycle "program").
        if s.sensor_fault or s.level >= self.HIGH_HIGH:
            s.pump_on = False
        elif s.mode == "AUTO":
            if s.level <= self.START_LEVEL:
                s.pump_on = True
            elif s.level >= self.STOP_LEVEL:
                s.pump_on = False
            # Between start/stop setpoints, retain prior output (hysteresis).
        else:
            s.pump_on = bool(s.manual_command)

        s.last_scan = time()
        return self.status()

    def set_control(self, payload):
        s = self.state
        if "mode" in payload:
            mode = str(payload["mode"]).upper()
            if mode not in ("AUTO", "MANUAL"):
                raise ValueError("Mode must be AUTO or MANUAL")
            s.mode = mode
        if "pump" in payload:
            s.manual_command = bool(payload["pump"])
        if s.mode == "MANUAL":
            s.pump_on = s.manual_command and not s.sensor_fault and s.level < self.HIGH_HIGH
        return self.status()

    def simulate(self, payload):
        s = self.state
        if "drain" in payload:
            s.level = max(0.0, s.level - float(payload["drain"]))
        if "fill" in payload:
            s.level = min(100.0, s.level + float(payload["fill"]))
        if "sensor_fault" in payload:
            s.sensor_fault = bool(payload["sensor_fault"])
            if s.sensor_fault:
                s.pump_on = False
        return self.status()

    def acknowledge(self):
        self.state.acknowledged = True
        return self.status()

    def status(self):
        s = self.state
        alarms = []
        if s.sensor_fault:
            alarms.append({"id": "sensor_fault", "severity": "HIGH", "message": "Level sensor fault — pump inhibited"})
        if s.level < self.LOW_ALARM:
            alarms.append({"id": "low_level", "severity": "MEDIUM", "message": "Low tank level"})
        if s.level >= self.HIGH_ALARM:
            alarms.append({"id": "high_level", "severity": "HIGH", "message": "High tank level"})
        return {
            **asdict(s),
            "level": round(s.level, 1),
            "pump_on": s.pump_on,
            "alarms": alarms,
            "alarm_acknowledged": s.acknowledged,
            "plc_status": "FAULT" if s.sensor_fault else "RUNNING",
        }
