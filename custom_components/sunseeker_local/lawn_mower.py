import json
import logging
from homeassistant.components.lawn_mower import LawnMowerEntity, LawnMowerEntityFeature, LawnMowerActivity
from homeassistant.components import mqtt
from .const import CONF_DEVICE_ID, TOPIC_COMMAND, TOPIC_UPDATE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the lawn mower platform."""
    device_id = config_entry.data[CONF_DEVICE_ID]
    async_add_entities([SunseekerMower(device_id)])

class SunseekerMower(LawnMowerEntity):
    """Representation of a Sunseeker Lawn Mower."""

    def __init__(self, device_id):
        """Initialize the mower."""
        self._device_id = device_id
        self._attr_name = f"Sunseeker {device_id}"
        self._attr_unique_id = f"sunseeker_mower_{device_id}"
        self._attr_supported_features = (
            LawnMowerEntityFeature.START | LawnMowerEntityFeature.DOCK | LawnMowerEntityFeature.STOP
        )
        self._attr_activity = LawnMowerActivity.IDLE

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        topic = TOPIC_UPDATE.format(self._device_id)
        
        async def message_received(msg):
            """Handle incoming MQTT messages."""
            try:
                data = json.loads(msg.payload)
                if data.get("cmd") == 501:
                    mode = data.get("mode")
                    if data.get("station", False):
                        self._attr_activity = LawnMowerActivity.DOCKED
                    elif mode == 1:
                        self._attr_activity = LawnMowerActivity.MOWING
                    elif mode == 2:
                        self._attr_activity = LawnMowerActivity.RETURNING
                    else:
                        self._attr_activity = LawnMowerActivity.IDLE
                    self.async_write_ha_state()
            except Exception as e:
                _LOGGER.error("Error parsing mower state: %s", e)

        await mqtt.async_subscribe(self.hass, topic, message_received)

    async def _send_command(self, mode_code):
        """Send a command to the mower."""
        topic = TOPIC_COMMAND.format(self._device_id)
        payload = json.dumps({"cmd": 101, "mode": mode_code})
        await mqtt.async_publish(self.hass, topic, payload)

    async def async_start(self):
        """Start or resume mowing."""
        await self._send_command(1)

    async def async_stop(self):
        """Stop the mower."""
        await self._send_command(0)

    async def async_dock(self):
        """Tell the mower to return to dock."""
        await self._send_command(2)