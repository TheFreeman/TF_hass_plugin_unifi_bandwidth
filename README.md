# TF_hass_plugin_unifi_bandwidth

# UniFi Bandwidth Integration for Home Assistant

Monitor real-time **upload & download** speeds of all UniFi devices and clients directly in **Home Assistant**!  
This integration connects to your **UniFi Network Console (UDM, UDM Pro, UCK, etc.)**, retrieves bandwidth usage data, and provides it as **sensors**.

## 🚀 Features
- 📊 **Live monitoring** of upload & download speeds for every UniFi client
- 🔗 **Direct integration** with UniFi Network API (no cloud required)
- 🔧 **Easy setup** via Home Assistant UI (no manual YAML needed)
- 🏷️ **Human-readable names** (uses device names from UniFi, falls back to MAC addresses)
- 🔍 **Works with wildcards**: Sensor IDs follow `sensor.unifi_upload_MAC` / `sensor.unifi_download_MAC`

---

## 📥 **Installation**
### 🔹 **Method 1: Manual Installation**
1. Download the latest release from [GitHub](https://github.com/TheFreeman/TF_hass_plugin_unifi_bandwidth).
2. Extract the contents to:
3. Restart Home Assistant.
4. Add the **"UniFi Bandwidth"** integration via **Settings → Devices & Services → Add Integration**.

### 🔹 **Method 2: HACS (Recommended)**
🚧 *This method requires the integration to be added to HACS (not yet available!)*  
Once available in HACS:
1. Open **HACS** in Home Assistant.
2. Navigate to **Integrations** → **+ Explore & Download**.
3. Search for **UniFi Bandwidth** and install it.
4. Restart Home Assistant.
5. Add the integration via **Settings → Devices & Services**.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=TheFreeman&repository=https%3A%2F%2Fgithub.com%2FTheFreeman%2FTF_hass_plugin_unifi_bandwidth)

---

## 🔑 **How to Get Your UniFi API Credentials**
To retrieve bandwidth data, this integration requires **API access to your UniFi Network Console**.

### **1️⃣ Enable API Access in UniFi**
1. **Login to UniFi Network Console** (UDM, UDM Pro, UCK, etc.).
2. Go to **Settings → System → Network Application API**.
3. Click **Enable API Access**.

### **2️⃣ Generate an API Key**
1. In **UniFi Network Console**, navigate to **User Settings**.
2. Click **API Keys** → **Generate New API Key**.
3. Copy and save the key securely.

### **3️⃣ Get Your UniFi Console IP**
You need the **local IP address** of your UniFi Console:
- **UDM/UDM-Pro Default**: `192.168.1.1`
- **UniFi Cloud Key Default**: `192.168.1.2`
- Or find it in **Settings → Network → Console IP**.

---

## 📊 **Sensors Created by the Integration**
Each UniFi client receives **two sensors** in Home Assistant:
| Sensor Name | Description |
|------------|-------------|
| `sensor.unifi_upload_MAC` | Current upload speed (bps) |
| `sensor.unifi_download_MAC` | Current download speed (bps) |

💡 **Example sensor IDs:**


✅ **Wildcard support:** You can use `sensor.unifi_upload_*` in automations!  

---

## 🔧 **Troubleshooting**
1. **No sensors appearing?**
   - Restart Home Assistant after installation.
   - Check API Key & UniFi Console IP.
   - Verify API access is enabled in UniFi settings.

2. **Some clients missing?**
   - Ensure they are actively using bandwidth.
   - Reconnect devices to refresh UniFi’s client list.

3. **Need more help?**
   - Check **Home Assistant logs**:  
     ```
     ha core logs | grep unifi_bandwidth
     ```
   - Open an issue on [GitHub](https://github.com/TheFreeman/TF_hass_plugin_unifi_bandwidth/issues).

---

## 🔥 **Roadmap & Future Features**
- ✅ **Current version:** Supports real-time upload/download monitoring.
- 🛠 **Next features:** 
  - Add HACS support (coming soon!)
  - Aggregate total daily/weekly/monthly data
  - Create **alerts for high bandwidth usage**

---

## 📄 **License**

This project is licensed under the **Non-Commercial Open Source License (NCOSL) v1.0**.  
You are **free to use, copy, modify, and distribute** this software **for non-commercial purposes only**.  

For full details, please refer to the **[LICENSE.txt](LICENSE.txt)** file.  

### **Summary of License Terms**  
- ✅ Free for personal and non-commercial use  
- 🔄 Modifications and redistribution allowed with attribution  
- ❌ No commercial use or selling of this software or derivatives  
- ⚠️ Provided "as is" without any warranty  

By using this software, you agree to the terms outlined in the **LICENSE.txt** file.  

---
