# v2 - added description

import logging
import requests
from datetime import timedelta, datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


INTERVAL_TIME = 15
SCAN_INTERVAL = timedelta(seconds=INTERVAL_TIME)
_LOGGER = logging.getLogger(__name__)

def normalize_time(time_str: str) -> str:
    hour, minute = map(int, time_str.split(":"))
    base_time = datetime.strptime("00:00", "%H:%M")
    normalized = base_time + timedelta(hours=hour, minutes=minute)
    return normalized.strftime("%H:%M")

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up MMPK sensors from config."""
    sensors = []
    stops = config.get("stops", [])
    for stop in stops:
        stop_id = stop.get("id")
        lines = stop.get("lines", None)
        description = stop.get("description", f"MPK stop {stop_id}")
        if stop_id:
            name = f"MPK Stop {stop_id}"
            sensors.append(MMPKSensor(name, stop_id, lines, description))
    add_entities(sensors, True)

class MMPKSensor(SensorEntity):
    """Sensor for MPK Kraków stop schedule."""

    def __init__(self, name: str, stop_id: int, lines: list[str] | None = None, description: str | None = None) -> None:
        self._stop_id = stop_id
        self._lines = lines
        self._description = description
        self._attr_name = name
        self._attr_native_value = None
        self._attr_should_poll = True
        self._attr_scan_interval = timedelta(seconds=INTERVAL_TIME)
        self._departures_by_line = {}
        self._attr_unique_id = f"mpk_stop_{self._stop_id}"
        _LOGGER.debug(f"MMPK lines: {self._lines}")

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "stop_id": self._stop_id,
            "stop_name": getattr(self, "_stop_name", None),
            "description": self._description,
            "lines": self._lines,
            "departures_by_line": self._departures_by_line,
            "last_update": getattr(self, "_last_update", None)
        }

    def update(self) -> None:
        try:             
            now = datetime.now()
            next_departure_dt = datetime.combine(now.date(), datetime.strptime(self._attr_native_value, "%H:%M").time()) if self._attr_native_value else None

            _LOGGER.debug("Current time: %s, Next departure time: %s for stop %s", now, next_departure_dt, self._stop_id)

            if next_departure_dt is not None and now < next_departure_dt:
                _LOGGER.debug("Next departure %s for stop %s is still in the future, skipping update.", self._attr_native_value, self._stop_id)
                return
        
        except Exception as e:
            _LOGGER.warning("Failed to compare times for stop %s: %s", self._stop_id, e)
            self._attr_native_value = None
        
        """Fetch and organize all departures per line and variant."""
        now = datetime.now().isoformat()
        _LOGGER.debug("MMPK update triggered at %s for stop %s", now, self._stop_id)
        url = f"https://services.mpk.amistad.pl/mpk/schedule/stop/{self._stop_id}"
        _LOGGER.debug("Fetching MPK data from URL: %s", url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            lines_data = payload.get("lines", [])

            if self._lines is None:
                self._lines = [str(line_entry.get("line", {}).get("id")) for line_entry in lines_data if line_entry.get("line", {}).get("id")]
                _LOGGER.debug("Discovered lines for stop %s: %s", self._stop_id, self._lines)

            self._stop_name = payload.get("stop", {}).get("name", f"Stop {self._stop_id}")
            self._departures_by_line = {}

            for line_entry in lines_data:
                line_id = str(line_entry.get("line", {}).get("id"))
                if self._lines is not None and line_id not in self._lines:
                    continue

                variants = []
                seen_keys = set()

                for variant in line_entry.get("variants", []):
                    full_name = variant.get("header", {}).get("name", "Unnamed variant")
                    direction = full_name.split(" - ", 1)[1].strip() if " - " in full_name else None

                    departures = []
                    for dep in variant.get("departures", []):
                        hour = dep.get("hour")
                        minute = dep.get("minute")
                        if hour is not None and minute is not None:
                            try:
                                clean_minute = ''.join(filter(str.isdigit, str(minute)))
                                if clean_minute:
                                    time_str = f"{int(hour):02d}:{int(clean_minute):02d}"
                                    time_str = normalize_time(time_str)
                                    departures.append(time_str)
                            except Exception:
                                _LOGGER.warning("Failed to format time: %s", dep)

                    if departures:
                        key = (
                            line_id,
                            direction.strip().lower() if direction else "",
                            tuple(sorted(set(departures)))
                        )
                        if key in seen_keys:
                            _LOGGER.debug("Skipping duplicate variant: line %s → %s", line_id, direction)
                            continue
                        seen_keys.add(key)

                        variants.append({
                            "name": full_name,
                            "direction": direction,
                            "departures": departures
                        })

                if variants:
                    self._departures_by_line[line_id] = variants

            next_departure = None
            for line_variants in self._departures_by_line.values():
                for variant in line_variants:
                    if variant["departures"]:
                        candidate = variant["departures"][0]
                        if not next_departure or candidate < next_departure:
                            next_departure = candidate

            self._attr_native_value = next_departure if next_departure else None
            self._last_update = datetime.now().isoformat()
            _LOGGER.debug("Departures by line for stop %s: %s", self._stop_id, self._departures_by_line)

        except Exception as e:
            _LOGGER.error("Failed to fetch MPK data for stop %s: %s", self._stop_id, e)
            self._attr_native_value = "Error"
            self._departures_by_line = {}

