import time
import network
import urequests as requests
from machine import Pin
import uasyncio as asyncio

check_interval_sec = 0.25
door_sensor = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT, value=1)

# Configure your WiFi SSID and password
ssid = 'TODO-Wifi Name'
password = 'TODO-Wifi Password'

# Initial value for the sensor
sensor_value = None

# Turn on netowrk adater
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)  # Diable powersave mode
wlan.connect(ssid, password)

# Wait for connect or fail
def blink_led(frequency = 0.5, num_blinks = 3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

def sensor_update():
    global sensor_value

    old_value = sensor_value
    sensor_value = door_sensor.value()

    # Garage door is open.
    if sensor_value == 1:
        if old_value != sensor_value:
            print('Door is open.')
            r = requests.post("https://maker.ifttt.com/trigger/"TODO-Event Name"/with/key/"TODO-WebHook"")
            r.close()
        led.on()

    # Garage door is closed.
    elif sensor_value == 0:
        if old_value != sensor_value:
            print('Door is closed.')
            r = requests.post("https://maker.ifttt.com/trigger/"TODO-Event Name"/with/key/"TODO-WebHook"")
            r.close()
        led.off()

async def main():
    print("Door state....")
    while True:
        sensor_update()
        await asyncio.sleep(check_interval_sec)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

