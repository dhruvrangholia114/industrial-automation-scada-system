import unittest
from plc_simulator import PLCSimulator

class TestPLCSimulator(unittest.TestCase):
    def test_auto_starts_below_start_setpoint(self):
        plc=PLCSimulator()
        plc.state.level=25
        plc.scan(elapsed=0)
        self.assertTrue(plc.state.pump_on)

    def test_auto_stops_at_stop_setpoint(self):
        plc=PLCSimulator()
        plc.state.level=81
        plc.state.pump_on=True
        plc.scan(elapsed=0)
        self.assertFalse(plc.state.pump_on)

    def test_sensor_fault_inhibits_pump(self):
        plc=PLCSimulator()
        plc.state.pump_on=True
        plc.state.sensor_fault=True
        plc.scan(elapsed=0)
        self.assertFalse(plc.state.pump_on)
        self.assertEqual(plc.status()["plc_status"],"FAULT")

    def test_manual_command(self):
        plc=PLCSimulator()
        plc.set_control({"mode":"MANUAL","pump":True})
        self.assertTrue(plc.state.pump_on)

if __name__=="__main__":
    unittest.main()
