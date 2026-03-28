# Sunseeker Local MQTT for Home Assistant
A custom Home Assistant integration for Sunseeker and whitelabeled robotic lawnmowers. Enables fast, secure, and cloud-free local control via MQTT.

[Tästä suomenkielisiin ohjeisiin (Finnish instructions below)](#suomeksi-finnish)

---

## 🇬🇧 English

### What is this?
By default, Sunseeker mowers (and whitelabeled brands like Scheppach, Brucke, Orbex, and Meec Tools) communicate with a proprietary cloud server over an unencrypted MQTT connection. This poses a security risk, as your WiFi credentials and other data are sent in plain text.

This integration leverages local MQTT traffic interception to cut off the cloud entirely. It provides a secure, instantaneous, and private way to manage your lawnmower directly from Home Assistant.

### Key Features
* **100% Local Control (Local Push):** No cloud dependency.
* **Instantaneous Response:** Commands execute with zero cloud latency.
* **Comprehensive Monitoring:** Track battery, mower status, rain delay countdowns, and current session statistics.

### Prerequisites
1. **Home Assistant** with a working MQTT broker (e.g., Mosquitto add-on).
2. **Network Redirection (Crucial!):** You MUST configure your local router to intercept the mower's MQTT traffic (Port 1883) and redirect it to your Home Assistant's IP address.
   * *Example (MikroTik RouterOS):*
     `/ip firewall nat add chain=dstnat src-address=[MOWER_IP] protocol=tcp dst-port=1883 action=dst-nat to-addresses=[HOME_ASSISTANT_IP] to-ports=1883 comment="Redirect Sunseeker MQTT"`
   * *Other routers:* Look for features like "Custom NAT", "Port Forwarding (Internal)", or "DNS Hijacking".

### Installation
**Method 1: HACS (Recommended)**
1. Open Home Assistant -> HACS -> Integrations.
2. Click the three dots (top right) -> **Custom repositories**.
3. Add this repository URL (`https://github.com/your_username/sunseeker_local_control`) and select **Integration** as the category.
4. Click **Download** and restart Home Assistant.

**Method 2: Manual**
1. Copy the `custom_components/sunseeker_local` folder into your Home Assistant's `config/custom_components/` directory.
2. Restart Home Assistant.

### Configuration
1. Go to **Settings** -> **Devices & Services** -> **Add Integration**.
2. Search for **Sunseeker Local (MQTT)**.
3. Enter your mower's 20-character **Device ID**. 
   * *Where to find it?* On the mower's sticker (S/N), in the official app, or by sniffing your MQTT broker traffic for `device/YOUR_ID/update`.

### Acknowledgments
Special thanks to [OlliKantola](https://github.com/OlliKantola/Sunseeker_LawnMower_Control) for reverse-engineering the MQTT commands and documenting the local API.

---

## 🇫🇮 Suomeksi (Finnish)

### Mikä tämä on?
Oletuksena Sunseeker-ruohonleikkurit (ja sisarmerkit kuten Scheppach, Brücke, Orbex ja Meec Tools) kommunikoivat valmistajan pilvipalvelimen kanssa salaamattoman MQTT-yhteyden yli. Tämä on tietoturvariski, sillä mm. langattoman verkkosi salasana lähetetään selkokielisenä.

Tämä integraatio hyödyntää paikallisen verkkoliikenteen uudelleenohjausta, jolloin pilviyhteys katkaistaan kokonaan. Saat turvallisen, viiveettömän ja yksityisen tavan hallita leikkuriasi suoraan Home Assistantista.

### Tärkeimmät ominaisuudet
* **100% Paikallinen hallinta (Local Push):** Ei riippuvuutta pilvipalveluista.
* **Välitön vaste:** Komennot menevät perille ilman viivettä.
* **Kattava seuranta:** Seuraa akkua, leikkurin tilaa, sateen viiveitä ja leikkuutilastoja.

### Vaatimukset
1. **Home Assistant**, jossa on toimiva MQTT-välityspalvelin (esim. Mosquitto add-on).
2. **Verkon uudelleenohjaus (Kriittinen!):** Sinun ON pakotettava reitittimesi (router) kaappaamaan leikkurin ulospäin suuntautuva MQTT-liikenne (portti 1883) ja ohjattava se Home Assistantin IP-osoitteeseen.
   * *Esimerkki (MikroTik RouterOS):*
     `/ip firewall nat add chain=dstnat src-address=[LEIKKURIN_IP] protocol=tcp dst-port=1883 action=dst-nat to-addresses=[HOME_ASSISTANT_IP] to-ports=1883 comment="Redirect Sunseeker MQTT"`
   * *Muut reitittimet:* Etsi ominaisuuksia kuten "Custom NAT", "Port Forwarding (Internal)" tai "DNS Hijacking".



### Asennus
**Tapa 1: HACS (Suositeltu)**
1. Avaa Home Assistant -> HACS -> Integrations.
2. Klikkaa kolmea pistettä (oikea yläkulma) -> **Custom repositories**.
3. Lisää tämän repon URL (`https://github.com/iiseppi/sunseeker_local_control`) ja valitse tyypiksi **Integration**.
4. Lataa integraatio ja käynnistä Home Assistant uudelleen.

**Tapa 2: Manuaalinen**
1. Kopioi `custom_components/sunseeker_local` -kansio Home Assistantin `config/custom_components/` -hakemistoon.
2. Käynnistä Home Assistant uudelleen.

### Käyttöönotto
1. Mene **Asetukset** -> **Laitteet ja palvelut** -> **Lisää integraatio**.
2. Etsi **Sunseeker Local (MQTT)**.
3. Syötä leikkurisi 20-merkkinen **Laite-ID (Device ID)**. 
   * *Mistä löydän sen?* Leikkurin tarrasta (S/N), virallisesta sovelluksesta tai seuraamalla MQTT-liikennettä (etsi aihetta `device/SINUN_ID/update`).

### Kiitokset
Erityiskiitokset [OlliKantolalle](https://github.com/OlliKantola/Sunseeker_LawnMower_Control) MQTT-komentojen selvittämisestä ja paikallisen APIn dokumentoinnista.
