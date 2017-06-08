import time
from pyo import *
from collections import namedtuple, defaultdict
import random
from perlin import gen_perlin_ints
# do not edit! added by PythonBreakpoints
from pudb import set_trace as _breakpoint


s = Server().boot()
s.start()

tempo = 0.8

note_lengths = [
                1.0/16.0,
                1.0/8.0,
                1.0/4.0,
                1.0/2.0,
                1.0,
                2.0,
                3.0,
                4.0,
                ]
pauses = [0.124 * x for x in range(8)]

note_lengths = [length * tempo for length in note_lengths]
pauses = [pause * tempo for pause in pauses]

c5_pentatonic = [523, 587, 659, 740, 880] #major pentatonic scale starting at c5
c4_pentatonic = [ n / 2.0  for n in c5_pentatonic]
c3_pentatonic = [ n / 2.0  for n in c4_pentatonic]

midi_notes = range(50,70, 2)
midi_notes = [midiToHz(freq) for freq in midi_notes]


NOW = 0.0
timestep =  0.125 * tempo
metronome = Metro(timestep).play()
def add_time():
    global NOW, timestep
    NOW += timestep

timer = TrigFunc(metronome, add_time)

per_num_patterns_allowed = defaultdict(lambda: gen_perlin_ints(2,6))
per_pattern_length = defaultdict(lambda: gen_perlin_ints(3,7))
per_note_lens = defaultdict(lambda: gen_perlin_ints(0,len(note_lengths)))
per_pauses = defaultdict(lambda: gen_perlin_ints(0,len(pauses)))
jamie_patterns = defaultdict(list)

Note = namedtuple("Note", ["time", "freq", "length"])

class Instrument(object):
    def __init__(self, instrument, notes=None, envelope = None, mul=1):
        self.envelope = envelope or Fader(fadein=.001, fadeout=.01, dur=.12, mul=mul)
        self.instrument = instrument
        self.instrument.setMul(self.envelope)
        self.instrument.out()

        self.notes = notes or c5_pentatonic # to be respected by the scheduler
        self.note_schedule = [] # ordered list of notes to play

        self._triggerer = TrigFunc(metronome, self.play_note)

    def play_note(self):
        if not self.envelope.isPlaying():
            if self.note_schedule and NOW >= self.note_schedule[0].time:
                note_to_play = self.note_schedule.pop(0)
                self.instrument.setFreq(note_to_play.freq)
                self.envelope.setDur(note_to_play.length)
                self.envelope.play()

    def schedule(self, notes_to_insert):
        # take a list of notes with absolute offsets and insert them into our schedule, so it is sorted at the end.
        for note in notes_to_insert:
            if note.freq not in self.notes:
                raise Exception("Tried to insert note %s but only %s are allowed" % (note, self.notes))
            self.note_schedule.append(Note(NOW + note.time, note.freq, note.length))

        self.note_schedule.sort(key=lambda n: n.time)



instruments = []
instruments.append(Instrument(SineLoop(feedback=0.02), notes=c3_pentatonic, mul=1.0))
instruments.append(Instrument(SineLoop(feedback=0.02),  notes=c4_pentatonic, mul=0.3))
# instruments.append(Instrument(SineLoop(feedback=0.05), notes=c5_pentatonic, mul=0.15))
instruments.append(Instrument(SineLoop(feedback=0.02), notes=midi_notes, mul=0.3))



def gen_pattern(instr):
    cur_time = 0
    pattern = []
    for x in range(0, next(per_pattern_length[instr])):
        cur_note_length = note_lengths[next(per_note_lens[instr])]
        pattern.append(Note(cur_time, random.choice(instr.notes), cur_note_length))
        cur_time = cur_time + cur_note_length + pauses[next(per_pauses[instr])]
    return pattern

def mutate_pattern(instr, old_pattern):
    # change the freq of one note
    old_pattern = old_pattern[:]
    index = random.randint(0, len(old_pattern) - 1)
    print 'mutating note %s of %s ' % (index, len(old_pattern))
    old_pattern[index] = old_pattern[index]._replace(freq = random.choice(instr.notes))
    return old_pattern

def schedule_notes(instrument):
    global NOW, jamie_patterns, per_num_patterns_allowed

    if not instrument.note_schedule:
        if not jamie_patterns.get(instrument) or random.random() > 0.90:
            new_pattern = gen_pattern(instrument)
            instrument.schedule(new_pattern)
            jamie_patterns[instrument].append(new_pattern)

        elif random.random() > 0.7:
            old_pattern = random.choice(jamie_patterns[instrument])
            mutated_pattern = mutate_pattern(instrument, old_pattern)
            instrument.schedule(mutated_pattern)
            jamie_patterns[instrument].append(mutated_pattern)

        else:
            old_pattern = random.choice(jamie_patterns[instrument])
            instrument.schedule(old_pattern)

        # only let us keep a certain number of patterns around
        allowed_num_patterns = next(per_num_patterns_allowed[instrument])
        print "%s %s %s" % (len(jamie_patterns[instrument]), allowed_num_patterns , hash(instrument))
        jamie_patterns[instrument] = jamie_patterns[instrument][0:allowed_num_patterns]


scheduler = TrigFunc(metronome, schedule_notes, arg=instruments)


time.sleep(60.000000)
s.stop()
time.sleep(0.25)
s.shutdown()
