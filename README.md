# Home Assistant custom component mMPK

MPK Kraków public transport timetable

## Sensor configuration
```yaml
sensor:
  - platform: mmpk
    stops:
      - id: 1
        description: Bronowice Małe
      - id: 2
        description: Giełda Balicka
        lines:
          - "126"

```

* A sensor configured with id: `1` will retrieve data for all available buses and trams at the specified stop.
* A sensor configured with id: `2` will retrieve data exclusively for line `126` at the specified stop.
* `description` is optional

## Stop list

[CSV](doc/MPK_stops.csv)

## Instalation
### Manual


### 📦 Manual Installation

To install this integration manually, you need to download [**mmpk.zip**](https://github.com/mysiar/ha-custom-component-mmpk/releases/latest/download/mmpk.zip) and extract its contents to the `config/custom_components/mmpk` directory.


```bash
mkdir -p custom_components/mmpk
cd custom_components/mmpk
wget https://github.com/mysiar/ha-custom-component-mmpk/releases/latest/download/mmpk.zip
unzip mmpk.zip
rm mmpk.zip
```

## Display data 

* Markdown card
```
{% set sensor = 'sensor.mpk_stop_1' %}
{% set state = states(sensor) %}
{% set disabled = state_attr(sensor, 'entity_disabled') %}
{% set available = state not in ['unknown', 'unavailable', none] %}

{% if disabled or not available %}
_Sensor {{ sensor }} jest niedostępny lub wyłączony._
{% else %}
  {% set stop = state_attr(sensor, 'stop_name') %}
  {% set updated = state_attr(sensor, 'last_update') %}
  {% set departures = state_attr(sensor, 'departures_by_line') %}
  {% set next_departure = state if state != "unknown" else "Brak odjazdów" %}

**Przystanek: {{ stop if stop else "Nieznany" }}{% if updated %} [{{ updated[11:19] }}]{% endif %}**  
Następny odjazd: {{ next_departure }}  
{% if departures %}
  {% for line, variants in departures.items() -%}
    {% for variant in variants -%}
**{{ line }} → {{ variant.direction }}**  
{% if variant.departures -%}
{{ variant.departures | join(', ') }}
{% endif -%}
    {% endfor -%}
  {% endfor -%}
{% else -%}
Brak danych o odjazdach
{% endif -%}
{% endif %}

```

**Sensor 1 card**

![Sensor 1 card](doc/sensor_1_card.png)

**Sensor 2 card**

![Sensor 2 card](doc/sensor_2_card.png)