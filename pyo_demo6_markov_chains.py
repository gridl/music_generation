import time
from pyo import *
import random

s = Server().boot()
s.start()

sixteenth_met = Metro(time=1.0/16, poly=1).play()

notes = [523, 587, 659, 740, 880] #major pentatonic scale starting at c5
notes = [ n / 2.0  for n in notes]
# notes = [500,800]


metronome = Metro(.125).play()

jamie_patterns = []
cur_pattern = []

def play_next_note(instrument, env, notes):
    instrument.freq = [choose_next_freq(), choose_next_freq()]
    env.play()

def choose_next_freq():
    global cur_pattern
    if not cur_pattern:
        cur_pattern = choose_next_pattern()[:]
    return cur_pattern.pop()

def choose_next_pattern():
    if not jamie_patterns or random.random() < 0.125:
        new_pattern = gen_new_pattern()
        jamie_patterns.append(new_pattern)
        return new_pattern
    return random.choice(jamie_patterns)

def gen_new_pattern():
    return [random.choice(notes) for _ in range(random.randint(2,10))]


def init_instrument(my_scale, metronome):
    f = Fader(fadein=.005, fadeout=.1, dur=.12, mul=.2)
    a = SineLoop(midiToHz([60,60]), feedback=0.05, mul=f)
    tf = TrigFunc(metronome, play_next_note)
    return a

instruments = [init_instrument(notes, metronome)]
mix = Mix(instruments).out()


time.sleep(60.000000)
s.stop()
time.sleep(0.25)
s.shutdown()
