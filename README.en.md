# Mercedes Members Employee Leasing Information

[Deutsch](README.md)

Unofficial Home Assistant template blueprints for kilometres until the next mileage-band change, the current mileage band, and the corresponding additional payment.

## Dashboard example

<img src="example-dashboard.png" alt="Mercedes leasing dashboard with the licence plate redacted" width="420">

Edited, anonymised capture of the original dashboard. The licence plate is covered in all three places. Additional vehicle readings and controls are not supplied by these blueprints. The original display shows 39 km to the band's upper limit; the corrected blueprint shows **40 km until the next band starts at 22,100 km**, given an odometer reading of 22,060 km and a zero starting value.

## Installation

Requires Home Assistant 2026.9 or later and an existing odometer sensor in **km**. This project does not connect to the vehicle or to Mercedes Members.

1. Download all three YAML files from [blueprints](blueprints).
2. Save them in `/config/blueprints/template/mercedes_leasing/`.
3. Merge [examples/configuration.yaml](examples/configuration.yaml) into your configuration. If `template:` already exists, append the three list items instead of adding another top-level key.
4. Set `odometer` to your own sensor in all three entries. Set `start_km` to the odometer reading at the beginning of the lease, or zero if your source already reports distance driven under this contract.
5. Check the configuration, then reload template entities or restart Home Assistant.

Each sensor uses its own template blueprint. Configuration is through YAML; this is not a HACS integration. For another vehicle, use different names and unique IDs. Verify new values before replacing old sensors and update dashboard references where necessary.

## Unique IDs

The example uses randomly generated UUIDv4 values for `unique_id`. Generate a fresh UUID for each additional sensor instance, for example with `uuidgen` or Python's `uuid.uuid4()`, and keep it stable. Copying the same UUID within a HA instance does not make it unique again. Unique text IDs are valid too; UUIDs reduce accidental naming collisions.

**Existing installations:** keep your current `unique_id` values. Replacing an ID creates a new entity identity and can affect dashboard references and history association.

## Optional: one device for all three readings

YAML template sensors do not support a `device:` block. [examples/mqtt-device.yaml](examples/mqtt-device.yaml) therefore provides three MQTT sensors sharing a single `device.identifiers` value, plus an automation forwarding the blueprint states. The **three MQTT sensors belong to one device**. The original three template sensors remain as calculation sources.

Requires a configured MQTT integration and broker, plus the three installed blueprint sensors. Adjust the three source entity IDs in the package to the actual IDs in your HA instance.

1. Save the file as `/config/packages/mercedes_leasing_mqtt.yaml`.
2. Enable packages in your existing configuration:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
   Merge existing `homeassistant:` and `packages:` entries instead of duplicating them.
3. Check configuration and restart HA.
4. Open the “Mercedes Mitarbeiter-Leasing” device under Settings → Devices & services → MQTT.

The automation publishes on state changes, HA startup, and every minute. MQTT readings expire after 180 seconds without a message. Invalid or unknown numerical source values become unavailable in the MQTT copies. After a broker restart, publication resumes within a minute. For another vehicle, replace **all UUIDs, the topic, and the three source entities**. All three sensors of the same vehicle must share its device ID; YAML anchors ensure this.

To remove the optional device configuration, remove its package and restart HA. The blueprint calculations remain. No discovery configurations or state messages are retained on the broker.

References: [Template blueprints](https://www.home-assistant.io/integrations/template/#using-blueprints), [MQTT devices](https://www.home-assistant.io/integrations/sensor.mqtt/#device), [HA packages](https://www.home-assistant.io/docs/configuration/packages/).

## Calculations and edge cases

Contract distance = odometer minus starting reading, rounded down to whole kilometres.
Band limits are inclusive: at 9,099 km, 1 km remains until 9,100 km, where the payment changes to EUR 240.
Remaining distance refers to the next **known** band change. In the final band (37,100–38,099 km), no subsequent tariff is known: remaining distance is `unknown`, while the payment remains EUR 2,940.
At 38,100 km and above, the band reads “Außerhalb der Tariftabelle” (outside the tariff table), and both numerical readings are `unknown`.
Missing or invalid odometer values, or readings below the starting value, make all three blueprint sensors `unavailable`.

## Included example tariff

**Contract basis: 9,000 km.** My original configuration is based on a lease agreement for 9,000 km. The agreed mileage allowance can vary between individual contracts. The mileage bands and additional payments provided here are therefore not universal rates: check them against your own agreement and adjust them where necessary. `start_km` refers only to the odometer reading at the beginning of the lease, not the agreed mileage allowance; changing it does not adjust the tariff table.

The amounts were supplied with the project's initial configuration. **The tariff date and contractual validity have not been verified.** Check your own contract before use. Amounts correspond to current distance, not a forecast for the end of the lease.

| Contract distance (km) | Additional payment (EUR) |
| --- | ---: |
| 0–9099 | 0 |
| 9100–13099 | 240 |
| 13100–17099 | 450 |
| 17100–21099 | 630 |
| 21100–22099 | 720 |
| 22100–23099 | 810 |
| 23100–24099 | 900 |
| 24100–25099 | 990 |
| 25100–26099 | 1140 |
| 26100–27099 | 1290 |
| 27100–28099 | 1440 |
| 28100–29099 | 1590 |
| 29100–30099 | 1740 |
| 30100–31099 | 1890 |
| 31100–32099 | 2040 |
| 32100–33099 | 2190 |
| 33100–34099 | 2340 |
| 34100–35099 | 2490 |
| 35100–36099 | 2640 |
| 36100–37099 | 2790 |
| 37100–38099 | 2940 |

To change the tariff, update `limits` identically in all three blueprints and `payments` in `nachzahlung.yaml`. Use one amount per band and strictly increasing limits.

## Validation

Regression tests render the actual YAML templates with Jinja and check band boundaries, starting-value subtraction, fractional readings, invalid states, and the end of the tariff table. Additional tests check example UUIDs, MQTT device grouping, and forwarding templates. These tests do not replace a full Home Assistant installation and broker test.

```sh
python3 -m pip install -r requirements-test.txt
python3 -m unittest discover -s tests -v
```

## About and licence

Independent community project, not an official Mercedes-Benz offering. No credentials, licence plates, or personal vehicle identifiers are needed in the published configuration.
MIT licence; see [LICENSE](LICENSE).
