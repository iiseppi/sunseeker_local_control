import json
import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.components import mqtt
from homeassistant.const import PERCENTAGE
from .const import CONF_DEVICE_ID, TOPIC_UPDATE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    device_id = config_entry.data[CONF_DEVICE_ID]
    async_add_entities([SunseekerBatterySensor(device_id)])

class SunseekerBatterySensor(SensorEntity):
    """Representation of the mower's battery sensor."""

    def __init__(self, device_id):
        """Initialize the sensor."""
        self._device_id = device_id
        self._attr_name = "Sunseeker Battery"
        self._attr_unique_id = f"sunseeker_batt_{device_id}"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_value = None

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        topic = TOPIC_UPDATE.format(self._device_id)
        
        async def message_received(msg):
            """Handle incoming MQTT messages."""
            try:
                data = json.loads(msg.payload)
                if data.get("cmd") == 501 and "power" in data:
                    self._attr_native_value = data["power"]
                    self.async_write_ha_state()
            except Exception as e:
                _LOGGER.debug("Error parsing battery state: %s", e)

        await mqtt.async_subscribe(self.hass, topic, message_received)