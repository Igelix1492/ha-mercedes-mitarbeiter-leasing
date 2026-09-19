"""Regression tests of the actual blueprint Jinja templates."""
import math
from pathlib import Path
import unittest
import yaml
from jinja2 import Environment

ROOT = Path(__file__).resolve().parents[1]
class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor("!input", lambda loader, node: loader.construct_scalar(node))
ENV = Environment()
def is_number(value):
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False

class Templates(unittest.TestCase):
    def render(self, key, value, start=0):
        doc = yaml.load((ROOT / "blueprints" / (key + ".yaml")).read_text(), Loader=Loader)
        context = dict(states=lambda entity: str(value), is_number=is_number,
                       odometer="sensor.test", start_km=start)
        sensor = doc["sensor"]
        available = ENV.from_string(sensor["availability"]).render(**context).strip()
        if available != "True":
            return "unavailable"
        return ENV.from_string(sensor["state"]).render(**context).strip()

    def test_every_band_edge(self):
        bands = [
            (0,9099,0),(9100,13099,240),(13100,17099,450),(17100,21099,630),
            (21100,22099,720),(22100,23099,810),(23100,24099,900),
            (24100,25099,990),(25100,26099,1140),(26100,27099,1290),
            (27100,28099,1440),(28100,29099,1590),(29100,30099,1740),
            (30100,31099,1890),(31100,32099,2040),(32100,33099,2190),
            (33100,34099,2340),(34100,35099,2490),(35100,36099,2640),
            (36100,37099,2790),(37100,38099,2940),
        ]
        for lower, upper, amount in bands:
            for km in (lower, upper):
                with self.subTest(km=km):
                    self.assertEqual(self.render("bandbreite", km), f"{lower} - {upper}")
                    self.assertEqual(self.render("nachzahlung", km), str(amount))
                    expected = str(upper + 1 - km) if upper < 38099 else "None"
                    self.assertEqual(self.render("restkilometer", km), expected)

    def test_offset_and_fraction(self):
        self.assertEqual(self.render("restkilometer", 9199.9, 100), "1")
        self.assertEqual(self.render("nachzahlung", 9200, 100), "240")

    def test_invalid(self):
        for value in ("unknown", "unavailable", "", "abc", "nan", "inf", -1):
            for key in ("restkilometer", "bandbreite", "nachzahlung"):
                with self.subTest(value=value, key=key):
                    self.assertEqual(self.render(key, value), "unavailable")
        self.assertEqual(self.render("bandbreite", 99, 100), "unavailable")
        self.assertEqual(self.render("bandbreite", 100, -1), "unavailable")

    def test_outside_table(self):
        for km in (38100, 99999):
            self.assertEqual(self.render("bandbreite", km), "Außerhalb der Tariftabelle")
            self.assertEqual(self.render("nachzahlung", km), "None")
            self.assertEqual(self.render("restkilometer", km), "None")

if __name__ == "__main__":
    unittest.main()
