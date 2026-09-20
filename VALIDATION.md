# Prüfstatus

Am 19.09.2026 im Home-Assistant-Template-Editor geprüft:
- 126 Prüfungen der Bandberechnung an den unteren und oberen Grenzen aller 21 Bänder: keine Fehler.
- Abzug des Startwerts und Abrunden eines Dezimalwerts: erfolgreich.
- Erkennung von unknown, unavailable, nan und inf: erfolgreich.

Die Prüfung im Editor verwendete die Berechnungslogik mit synthetischen Werten. Die Blueprints wurden noch nicht als Entitäten installiert oder per HA-Konfigurationsprüfung validiert.
Die Python-Regressionstests rendern die Templates aus den YAML-Dateien. Der erste GitHub-Actions-Lauf am 19.09.2026 war erfolgreich: https://github.com/Igelix1492/ha-mercedes-mitarbeiter-leasing/actions/runs/35438478708

Erweiterung vom 20.09.2026: Tests für UUIDv4-IDs, gemeinsame MQTT-Geräte-ID, Topics, Zustandsübertragung und Verfügbarkeit hinzugefügt. Der Workflow prüft sie nach Veröffentlichung. Das MQTT-Package wurde nicht mit einem realen Broker installiert; die Tests ersetzen keine HA-Konfigurationsprüfung oder einen Integrationstest.
