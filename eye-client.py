"""
Stream the esp-eye camera output to a network device

 ESP-EYE development kit from Espressif
 with circuit python loaded (https://circuitpython.org/board/espressif_esp32s3_eye/)

# SPDX-FileCopyrightText: Copyright (c) 2022 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Copyright (c) 2024 Mike Yudaken

"""

import board
import espcamera
import wifi
import socketpool
import time
from ulab import numpy as np
from secrets import secrets

wifi.radio.connect(secrets['SSID'], secrets['PASSWORD'])
pool = socketpool.SocketPool(wifi.radio)
print("My IP", wifi.radio.ipv4_address)

HOST = "192.168.0.169"
PORT = 9999

cam = espcamera.Camera(
    data_pins=board.CAMERA_DATA,
    external_clock_pin=board.CAMERA_XCLK,
    pixel_clock_pin=board.CAMERA_PCLK,
    vsync_pin=board.CAMERA_VSYNC,
    href_pin=board.CAMERA_HREF,
    pixel_format=espcamera.PixelFormat.JPEG,
    frame_size=espcamera.FrameSize.HVGA,
    i2c=board.I2C(),
    external_clock_frequency=20_000_000,
    framebuffer_count=2,
    grab_mode=espcamera.GrabMode.WHEN_EMPTY)

cam.vflip = True

while True:
    frame = cam.take(1)
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.connect((HOST, PORT))
   
    data = np.frombuffer(frame, dtype = np.uint8)
    j = 0
    while True:
        try:
            sent = s.send(data[j:j+1440])
            j += sent
        except:
            pass
        if j >= len(data):
            break
    s.close()
    time.sleep(0.05)
   
