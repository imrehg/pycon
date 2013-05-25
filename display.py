#!/usr/bin/env python2
"""
Quick code to get Facebook like count for PyMCU
"""
import pymcu
import time
import datetime
import urllib2
import simplejson
import socket

class LCD:
    """ SparkFun SerLCD 2.5 module, serial communication """

    def __init__(self, pin, mode):
        self.pin = pin
        self.mode = mode
        self.mb = pymcu.mcuModule()
        self._write = lambda cmd: self.mb.serialWrite(self.pin, self.mode, cmd)

    def _sendcmds(self, cmdlist):
        for cmd in cmdlist:
            self._write(cmd)
            time.sleep(0.01)

    def lightLevel(self, level):
        if level < 0:
            level = 0
        elif level > 29:
            level = 29
        self._sendcmds([0x7C, 128+level]);

    def clearDisplay(self):
        self._sendcmds([0xFE, 0x01])

    def write(self, text):
        self._write(text)
        time.sleep(0.1)

    def pos(self, line, loc):
        locbit = 0
        if line == 0:
            locbit = loc;
        elif line == 1:
            locbit = 64 + loc;
        locbit += 128;
        self._sendcmds([0xFE, locbit]);

    def boxCursor(self, on):
        if on:
            cmd = 0x0D;
        else:
            cmd = 0x0C;
        self._sendcmds([0xFE, cmd]);

def getLikes():
    req = urllib2.Request("http://graph.facebook.com/TaipeiHackerspace")
    opener = urllib2.build_opener()
    f = opener.open(req)
    data = simplejson.load(f)
    return int(data['likes'])

pin = 11
mode = 2  # 9600 baud
lcd = LCD(pin, mode);
lcd.clearDisplay();
lcd.boxCursor(False);

while True:
    now = datetime.datetime.now()
    timestr = now.strftime("%H:%M:%S")
    lcd.pos(0, 0)
    lcd.write("TPEHACK "+timestr);

    try:
        likes = getLikes()
    except socket.error:
        print "Socket error... (network gotcha)"

    lcd.pos(1, 0)
    lcd.write("Like count: "+str(likes));
    time.sleep(2)
