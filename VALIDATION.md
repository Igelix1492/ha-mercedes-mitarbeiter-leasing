# Prüfstatus

Am 19.09.2026 im Home-Assistant-Template-Editor geprüft:
- 126 Prüfungen der Bandberechnung an den unteren und oberen Grenzen aller 21 Bänder: keine Fehler.
- Abzug des Startwerts und Abrunden eines Dezimalwerts: erfolgreich.
- Erkennung von unknown, unavailable, nan und inf: erfolgreich.

Die Prüfung im Editor verwendete die Berechnungslogik mit synthetischen Werten. Die Blueprints wurden noch nicht als Entitäten installiert oder per HA-Konfigurationsprüfung validiert.
Die beiliegenden Python-Regressionstests rendern die Templates aus den YAML-Dateien. Sie konnten lokal mangels Python-Laufzeit nicht ausgeführt werden; der GitHub-Actions-Workflow führt sie nach Veröffentlichung aus.
