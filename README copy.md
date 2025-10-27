

sensor
```
- platform: mmpk
  stops:
    - id: 1387
      lines:
        - "50"
        - "18"
    - id: 2532
    - id: 1377
```    

```
{% set sensor = 'sensor.mpk_stop_1387' %}
{% set stop = state_attr(sensor, 'stop_name') %}
{% set updated = state_attr(sensor, 'last_update') %} 
{% set departures = state_attr(sensor, 'departures_by_line') %}
{% set next_departure = states(sensor) != "unknown" and states(sensor) or "Brak odjazdów" %}

**Przystanek: {{ stop if stop else "Nieznany" }} {% if updated %}[{{ updated[11:19] }}]{% endif %}**
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

```


## Notes

* https://services.mpk.amistad.pl/mpk/schedule/stop/1387
* https://services.mpk.amistad.pl/mpk/schedule/stop/2532
* https://services.mpk.amistad.pl/mpk/schedule/variant/50-1/1382
* https://services.mpk.amistad.pl/mpk/schedule/variant/50-1/1387
* https://services.mpk.amistad.pl/mpk/schedule/variant/50-2/1387

```
{% set sensor = 'sensor.mpk_stop_1387' %}
{% set stop = state_attr(sensor, 'stop_name') %}
{% set updated = state_attr(sensor, 'last_update') %} 
{% set departures = state_attr(sensor, 'departures_by_line') %}
{% set next_departure = states(sensor) != "unknown" and states(sensor) or "Brak odjazdów" %}


**Przystanek: {{ stop if stop else "Nieznany" }} {% if updated %}[{{ updated[11:19] }}]{% endif %}**  
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

<hr>
{% set sensor = 'sensor.mpk_stop_1377' %}
{% set stop = state_attr(sensor, 'stop_name') %}
{% set updated = state_attr(sensor, 'last_update') %} 
{% set departures = state_attr(sensor, 'departures_by_line') %}
{% set next_departure = states(sensor) != "unknown" and states(sensor) or "Brak odjazdów" %}


**Przystanek: {{ stop if stop else "Nieznany" }} {% if updated %}[{{ updated[11:19] }}]{% endif %}**  
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
<hr>
{% set sensor = 'sensor.mpk_stop_2532' %}
{% set stop = state_attr(sensor, 'stop_name') %}
{% set updated = state_attr(sensor, 'last_update') %} 
{% set departures = state_attr(sensor, 'departures_by_line') %}
{% set next_departure = states(sensor) != "unknown" and states(sensor) or "Brak odjazdów" %}

**Przystanek: {{ stop if stop else "Nieznany" }} {% if updated %}[{{ updated[11:19] }}]{% endif %}**  
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
{% endif %}

```