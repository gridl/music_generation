import time
from pyo import *

s = Server().boot()
s.start()

sixteenth_met = Metro(time=1.0/16, poly=1).play()

notes = range(300,500, 50)
# notes = [500,800]

def instrument(notes, amp=1.0):
    t = CosTable([(0,0), (50,1), (250,.3), (8191,0)])
    note_len = TrigRand(sixteenth_met, min=1.0/8, max=2.0)
    note_freq = TrigRand(sixteenth_met, min=1.0/4, max=1.0)
    met = Metro(time=note_freq, poly=2).play()

    volume = TrigEnv(met, table=t, dur=note_len, mul=.4 * amp)
    freq = TrigChoice(met, notes)

    a = Sine(freq=freq, mul=volume )
    return a

instruments = []
instruments.append(instrument(notes))
instruments.append(instrument(range(100,200,20), amp= 1.5))
instruments.append(instrument(range(1000,1500,100), amp=0.25))

mix = Mix(instruments)
fin = Chorus(mix, depth=[1.5,1.6], feedback=0.5, bal=0.5)
fin.out()


time.sleep(60.000000)
s.stop()
time.sleep(0.25)
s.shutdown()
