import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_HOST, CONF_API_KEY, CONF_VERIFY_SSL, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class UnifiBandwidthConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow für die UniFi Bandwidth Integration."""

    async def async_step_user(self, user_input=None):
        """Erster Schritt der Benutzerkonfiguration."""
        errors = {}

        if user_input is not None:
            # Teste die API-Verbindung mit den eingegebenen Daten
            valid = await self.test_connection(user_input[CONF_HOST], user_input[CONF_API_KEY])

            if valid:
                return self.async_create_entry(title="UniFi Bandwidth", data=user_input)
            else:
                errors["base"] = "connection_error"

        # Erstelle die Eingabemaske
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="192.168.1.1"): cv.string,
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_VERIFY_SSL, default=False): cv.boolean,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): cv.positive_int,
            }),
            errors=errors,
        )

    async def test_connection(self, host: str, api_key: str) -> bool:
        """Testet die Verbindung zur UniFi API."""
        import requests
        url = f"https://{host}/proxy/network/api/s/default/stat/sta"
        headers = {"X-API-KEY": api_key, "Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, verify=False, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
