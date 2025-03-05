import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
import aiohttp
import asyncio
from datetime import timedelta

from .const import DOMAIN, CONF_HOST, CONF_API_KEY, CONF_VERIFY_SSL, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up UniFi Bandwidth sensors from a config entry."""
    host = entry.data[CONF_HOST]
    api_key = entry.data[CONF_API_KEY]
    verify_ssl = entry.data[CONF_VERIFY_SSL]
    update_interval = timedelta(seconds=entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL))

    coordinator = UniFiDataUpdateCoordinator(hass, host, api_key, verify_ssl, update_interval)
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for mac, client in coordinator.data.items():
        device_name = client.get("hostname") or client.get("name") or mac
        sensors.append(UniFiBandwidthSensor(coordinator, mac, device_name, "download"))
        sensors.append(UniFiBandwidthSensor(coordinator, mac, device_name, "upload"))

    async_add_entities(sensors, True)

class UniFiDataUpdateCoordinator(DataUpdateCoordinator):
    """Fetch data from UniFi API periodically."""
    def __init__(self, hass, host, api_key, verify_ssl, update_interval):
        """Initialize the coordinator."""
        self.host = host
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from the UniFi API."""
        url = f"https://{self.host}/proxy/network/api/s/default/stat/sta"
        headers = {"X-API-KEY": self.api_key, "Accept": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                response = await asyncio.wait_for(
                    session.get(url, headers=headers, ssl=self.verify_ssl), timeout=10
                )
                data = await response.json()
                _LOGGER.debug(f"API Daten empfangen: {data}")
                return {client["mac"]: client for client in data["data"]}
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout error while fetching data from UniFi API")
            raise UpdateFailed("Timeout while fetching data")
        except Exception as err:
            _LOGGER.error(f"Error fetching data from UniFi API: {err}")
            raise UpdateFailed from err

class UniFiBandwidthSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UniFi bandwidth sensor."""

    def __init__(self, coordinator, mac, device_name, data_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._mac = mac
        self._device_name = device_name
        self._data_type = data_type
        self._attr_name = f"UniFi {device_name} {data_type}"
        self._attr_unique_id = f"{mac}_{data_type}"
        self._attr_entity_id = f"sensor.unifi_{data_type}_{mac.replace(':', '_')}"
    
    @property
    def state(self):
        """Return the state of the sensor."""
        client_data = self.coordinator.data.get(self._mac, {})
        _LOGGER.debug(f"Sensor {self._attr_name}: {client_data}")  # Debugging

        if self._data_type == "download":
            return client_data.get("rx_bytes-r", 0)
        elif self._data_type == "upload":
            return client_data.get("tx_bytes-r", 0)
        return None
    
    @property
    def available(self):
        """Return True if sensor is available."""
        return self.coordinator.last_update_success
    
    async def async_update(self):
        """Request an update from the coordinator."""
        await self.coordinator.async_request_refresh()
