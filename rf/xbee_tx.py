'''*-----------------------------------------------------------------------*---
                                                         Author: Jason Ma
                                                         Date  : Dec 05 2019
                                      SARC

  File Name  : xbee_tx.py
  Description: Xbee transmitter
---*-----------------------------------------------------------------------*'''

from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice

import matplotlib.pyplot as plt
import sys
import time

import xbee_utils
import config

MSG = ""
MSG = MSG.join(['a' for i in range(92)])

MAX_LEN = 92
PORT = config.PORT_XBEE_TX
BAUD_RATE = config.BAUD_XBEE
REMOTE_NODE_ID = "xb1"
NUM_TX = 100
SC = "0010"
device = XBeeDevice(PORT, BAUD_RATE)
c = xbee_utils.XBee_Controller(device, PORT)
try:
  #open connection and write params
  c.device.open()
  c.set_channel(SC)

  #find remote device
  c.setup_connection()

  #accept user input
  cmd = ""
  while cmd != 'q':
    cmd = input("[cmd] [t] run tx [c] change channel [q] quit --- :")
    if len(cmd) > 0 and cmd[0] == 'q':
      break
    elif len(cmd) > 0 and cmd[0] == 't':
      c.tx(data=MSG)
      plt.plot(range(len(c.times)), c.times)
      plt.xlabel("Packet")
      plt.ylabel("Time to send")
      #plt.show(block=False)
      plt.draw()
      plt.pause(0.001)
    elif len(cmd) > 0 and cmd[0] == 'c':
      arg = cmd.strip('\n').split(' ')
      if len(arg) > 1:
        arg = cmd.strip('\n').split(' ')[1]
        print("[cmd] change channel: %s" % (arg))
        c.remote_device = None
        c.set_channel(arg)
        c.setup_connection()
      else:
        print("[cmd] need to specify channel bits")
except KeyboardInterrupt:
  print("[cmd] Ctrl+C received. Stopping")
finally:
  c.close_device()
