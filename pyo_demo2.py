from pyo import *
s = Server().boot()
mod = Sine(freq=6, mul=50)
f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
a = Sine(freq=mod + 440, mul=f).out()
f.play()
s.gui(locals())

# from pyo import *
# s = Server().boot()
# f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
# a = Sine(mul=f).out()
# f.play()
# s.gui(locals())
