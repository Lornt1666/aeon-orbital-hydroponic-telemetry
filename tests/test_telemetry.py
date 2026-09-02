import unittest
from orbital_hydro.telemetry import NutrientReading, classify, lighting_duty_cycle


class TelemetryTests(unittest.TestCase):
    def test_in_range(self):
        r = NutrientReading("res-1", 1.8, 6.0, 21.0, 400.0)
        self.assertEqual(classify(r), {
            "ec_ms_cm": "ok",
            "ph": "ok",
            "temp_c": "ok",
            "light_ppfd": "ok",
        })

    def test_low_ph(self):
        r = NutrientReading("res-1", 1.8, 4.9, 21.0, 400.0)
        self.assertEqual(classify(r)["ph"], "low")

    def test_duty_cycle_clamp(self):
        self.assertEqual(lighting_duty_cycle(0.0), 0.0)
        self.assertEqual(lighting_duty_cycle(800.0), 1.0)
        self.assertAlmostEqual(lighting_duty_cycle(200.0), 0.5)


if __name__ == "__main__":
    unittest.main()
