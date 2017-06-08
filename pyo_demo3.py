
import time
from pyo import *
s = Server().boot()
s.start()
snd = SNDS_PATH + "/transparent.aif"
sf = SfPlayer(snd, speed=[.75,.8, .9, .6, 2], loop=True, mul=.3).out()
time.sleep(10.000000)
s.stop()
time.sleep(0.25)
s.shutdown()
