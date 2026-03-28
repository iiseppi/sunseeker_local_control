import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_DEVICE_ID

# The schema defines what fields the user sees in the setup dialog.
# We make it a required string field.
DATA_SCHEMA = vol.Schema({
    vol.Required(
        CONF_DEVICE_ID, 
        default="", 
        description={"suggested_value": "e.g., 20-character Serial Number"}
    ): str,
})

class SunseekerLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sunseeker Local MQTT."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters the Device ID."""
        errors = {}
        
        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID].strip()
            
            # Basic validation: ensure the ID is not completely empty
            if not device_id:
                errors["base"] = "empty_id"
            else:
                # If valid, create the entry. The title is what shows up in the HA integrations list.
                return self.async_create_entry(
                    title=f"Sunseeker ({device_id})", 
                    data={CONF_DEVICE_ID: device_id}
                )

        # Show the form to the user.
        # The translations for the description should ideally be in a strings.json file,
        # but this provides the structure.
        return self.async_show_form(
            step_id="user", 
            data_schema=DATA_SCHEMA, 
            errors=errors,
            description_placeholders={
                "hint": "Find your Device ID (often a 20-character serial number) on the mower's sticker, in the official app, or by listening to your MQTT broker traffic (topic: device/YOUR_ID/update)."
            }
        )