#!/usr/bin/env python2
import pymcu
import time

mb = pymcu.mcuModule()

pin = 11
mode = 2

while True:
    mb.serialWrite(pin, mode, 'r')
    time.sleep(0.01)
