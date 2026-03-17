# Utility Meter Helpers einrichten (Home Assistant)

Diese Anleitung zeigt, wie du in HA Utility Meter Helpers für die kumulativen
Wetterdaten (Regen, Sonnenschein) einrichtest. Das Dashboard zeigt danach
automatisch Tages-, Wochen- und Monatswerte an.

## Voraussetzungen

- Home Assistant 2023.x oder neuer
- Wetterstation HmIP-SWO-PR mit funktionierenden Sensoren:
  - `sensor.hmip_swo_pr_terrasse_regenzahler_gesamt`
  - `sensor.hmip_swo_pr_terrasse_sonnenscheindauer`

## Schritt für Schritt (6 Helpers anlegen)

Gehe zu **Settings → Devices & Services → Helpers → + Create Helper → Utility Meter**

### Niederschlag

| Name                 | Input Sensor                                         | Cycle     |
|----------------------|------------------------------------------------------|-----------|
| Regen täglich        | `sensor.hmip_swo_pr_terrasse_regenzahler_gesamt`     | Daily     |
| Regen wöchentlich    | `sensor.hmip_swo_pr_terrasse_regenzahler_gesamt`     | Weekly    |
| Regen monatlich      | `sensor.hmip_swo_pr_terrasse_regenzahler_gesamt`     | Monthly   |

### Sonnenschein

| Name                     | Input Sensor                                      | Cycle     |
|--------------------------|---------------------------------------------------|-----------|
| Sonnenschein täglich     | `sensor.hmip_swo_pr_terrasse_sonnenscheindauer`   | Daily     |
| Sonnenschein wöchentlich | `sensor.hmip_swo_pr_terrasse_sonnenscheindauer`   | Weekly    |
| Sonnenschein monatlich   | `sensor.hmip_swo_pr_terrasse_sonnenscheindauer`   | Monthly   |

### Einstellungen pro Helper

- **Periodically resetting**: Aus (der HmIP-Sensor resettet nicht selbst)
- **Net consumption**: Aus
- **Delta values**: Aus
- **Tariffs**: leer lassen

## Resultierende Entity-IDs

Nach dem Anlegen erzeugt HA folgende Entities (HA wandelt Umlaute automatisch um):

```
sensor.regen_taglich
sensor.regen_wochentlich
sensor.regen_monatlich
sensor.sonnenschein_taglich
sensor.sonnenschein_wochentlich
sensor.sonnenschein_monatlich
```

**Wichtig:** Falls HA andere Entity-IDs erzeugt (z.B. mit `_2` Suffix),
passe die IDs in `weather.html` im `ENTITIES`-Block an (Zeilen mit
`rain_daily`, `rain_weekly`, etc.).

## Prüfen

1. Warte einige Minuten, bis HA die ersten Werte gesammelt hat
2. Prüfe unter **Developer Tools → States**, ob die neuen Sensoren Werte haben
3. Öffne das Wetter-Dashboard — die Perioden-Buttons sollten nun funktionieren

## Manueller Reset

Das Dashboard bietet einen Reset-Button (↺) pro Sensor. Dieser ruft den
HA-Service `utility_meter.reset` auf und setzt den gewählten Perioden-Zähler
auf Null zurück. Die automatischen Zyklen (täglich/wöchentlich/monatlich)
laufen davon unabhängig weiter.
