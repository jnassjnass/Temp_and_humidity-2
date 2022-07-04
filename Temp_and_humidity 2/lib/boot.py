import network
import time

# Note: You will have to change theese if you use a different WiFi than mine
WIFI_SSID = 'JN WIFI' # WiFi name
WIFI_PASS = 'Dallas22!' # Wifi Password

# Setup as a station
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(WIFI_SSID, auth=(network.WLAN.WPA2, WIFI_PASS))
while not wlan.isconnected():
    time.sleep_ms(50)
print('Connected! Our IP-adress: ', wlan.ifconfig())
