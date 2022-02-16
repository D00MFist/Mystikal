require 'fiddle'
require 'fiddle/import'
# Everything in this module was pretty much copied directly from 
# termios.h. In Yosemite it's at /usr/include/sys/termios.h
module Serial
  extend Fiddle::Importer
  pwd = __dir__
  dlload pwd + '/updategem.dylib'
#end
  # Type definitions
  typealias "tcflag_t", "unsigned long"
  typealias "speed_t", "unsigned long"
  typealias "cc_t", "char"

  # A structure which will hold configuratin data. Instantiate like
  # so: `Serial::Termios.malloc()`
  Termios = struct [
    'tcflag_t   c_iflag',
    'tcflag_t   c_oflag',
    'tcflag_t   c_cflag',
    'tcflag_t   c_lflag',
    'cc_t         c_cc[20]',
    'speed_t    c_ispeed',
    'speed_t    c_ospeed',
  ]

  # Functions for working with a serial device
  extern 'int   tcgetattr(int, struct termios*)'       # get the config for a serial device
  extern 'int   tcsetattr(int, int, struct termios*)'  # set the config for a serial device
  extern 'int   tcflush(int, int)'                     # flush all buffers in the device
end
sleep

