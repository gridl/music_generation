import time
from pyo import *

def play(osc, adsr, length=6.0):
    adsr.play()
    osc.out()
    time.sleep(length)
    osc.stop()

s = Server().boot()
s.start()
lfo = Sine(freq=2, mul=10)
mod = Sine(freq=6, mul=50)
f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
a = Sine(freq=mod + 440, mul=f).out()
# play(a, f)

# a.setFreq([400, 800, 1200])
# play(a, f)

# a.setFreq(mod + 500)
# play(a, f)

# f.setAttack(1)
# play(a, f)

# f.setAttack(.01)
# mod.setFreq(20)
# play(a, f)


mod.setFreq(lfo)
play(a, f)

s.stop()

time.sleep(0.25)
s.shutdown()
