import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up UniFi Bandwidth from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.info("UniFi Bandwidth Integration erfolgreich eingerichtet")

    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    _LOGGER.info("UniFi Bandwidth Integration wird entfernt")

    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok
