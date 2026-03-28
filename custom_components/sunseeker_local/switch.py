import json
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.components import mqtt
from .const import CONF_DEVICE_ID, TOPIC_COMMAND, TOPIC_UPDATE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the switch platform."""
    device_id = config_entry.data[CONF_DEVICE_ID]
    async_add_entities([SunseekerRainSwitch(device_id)])

class SunseekerRainSwitch(SwitchEntity):
    """Representation of the mower's rain sensor switch."""

    def __init__(self, device_id):
        """Initialize the switch."""
        self._device_id = device_id
        self._attr_name = "Sunseeker Rain Sensor"
        self._attr_unique_id = f"sunseeker_rain_{device_id}"
        self._attr_is_on = False

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        topic = TOPIC_UPDATE.format(self._device_id)
        
        async def message_received(msg):
            """Handle incoming MQTT messages."""
            try:
                data = json.loads(msg.payload)
                if data.get("cmd") == 505 and "rain_en" in data:
                    self._attr_is_on = data["rain_en"]
                    self.async_write_ha_state()
            except Exception as e:
                _LOGGER.debug("Error parsing rain switch state: %s", e)

        await mqtt.async_subscribe(self.hass, topic, message_received)

    async def async_turn_on(self, **kwargs):
        """Turn the rain sensor on."""
        topic = TOPIC_COMMAND.format(self._device_id)
        payload = json.dumps({"cmd": 105, "rain_en": True, "rain_delay_set": 180})
        await mqtt.async_publish(self.hass, topic, payload)

    async def async_turn_off(self, **kwargs):
        """Turn the rain sensor off."""
        topic = TOPIC_COMMAND.format(self._device_id)
        payload = json.dumps({"cmd": 105, "rain_en": False, "rain_delay_set": 180})
        await mqtt.async_publish(self.hass, topic, payload)