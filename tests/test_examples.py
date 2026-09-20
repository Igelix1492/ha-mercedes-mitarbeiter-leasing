"""Checks for UUIDs, MQTT grouping and state forwarding."""
import json
from pathlib import Path
import unittest
from uuid import UUID
import yaml
from jinja2 import Environment
from test_templates import is_number

ROOT = Path(__file__).resolve().parents[1]
class Examples(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load((ROOT / "examples/configuration.yaml").read_text())
        self.package = yaml.safe_load((ROOT / "examples/mqtt-device.yaml").read_text())
        self.env = Environment()
        self.env.globals["is_number"] = is_number
        self.env.filters["to_json"] = json.dumps

    def test_uuids_and_shared_device(self):
        sensors = self.package["mqtt"]["sensor"]
        ids = [e["unique_id"] for e in self.config["template"]]
        ids += [e["unique_id"] for e in sensors]
        ids += [self.package["automation"][0]["id"]]
        device_id = sensors[0]["device"]["identifiers"][0]
        ids.append(device_id)
        self.assertEqual(len(ids), len(set(ids)))
        for value in ids:
            self.assertEqual(UUID(value).version, 4)
        self.assertTrue(all(s["device"] == sensors[0]["device"] for s in sensors))
        topic = self.package["automation"][0]["actions"][0]["data"]["topic"]
        for sensor in sensors:
            self.assertEqual(sensor["state_topic"], topic)
            self.assertEqual(sensor["availability_topic"], topic)
            self.assertEqual(sensor["expire_after"], 180)

    def test_forwarding_and_valid_readings(self):
        auto = self.package["automation"][0]
        values = {
            auto["variables"]["source_rest"]: "40",
            auto["variables"]["source_band"]: "21100 - 22099",
            auto["variables"]["source_payment"]: "720",
        }
        rendered = self.env.from_string(auto["actions"][0]["data"]["payload"]).render(
            **auto["variables"], states=lambda entity: values[entity])
        payload = json.loads(rendered)
        self.assertEqual(payload, dict(restkilometer="40", bandbreite="21100 - 22099", nachzahlung="720"))
        for sensor in self.package["mqtt"]["sensor"]:
            self.assertEqual(self.env.from_string(sensor["availability_template"]).render(value_json=payload), "online")
        self.assertFalse(auto["actions"][0]["data"]["retain"])

    def test_missing_and_unknown_states(self):
        for state in ("unknown", "unavailable", ""):
            payload = dict(restkilometer=state, bandbreite=state, nachzahlung=state)
            for sensor in self.package["mqtt"]["sensor"]:
                self.assertEqual(self.env.from_string(sensor["availability_template"]).render(value_json=payload), "offline")
        payload = dict(restkilometer="unknown", bandbreite="37100 - 38099", nachzahlung="2940")
        result = [self.env.from_string(s["availability_template"]).render(value_json=payload)
                  for s in self.package["mqtt"]["sensor"]]
        self.assertEqual(result, ["offline", "online", "online"])
