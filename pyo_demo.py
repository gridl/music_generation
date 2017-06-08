from pyo import *
# s = Server().boot()
# s.start()
# sf = SfPlayer("path/to/your/sound.aif", speed=1, loop=True).out()
# Granulate an audio buffer:

# s = Server().boot()
# s.start()
# snd = SndTable("path/to/your/sound.aif")
# env = HannTable()
# pos = Phasor(freq=snd.getRate()*.25, mul=snd.getSize())
# dur = Noise(mul=.001, add=.1)
# g = Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=.1).out()
# Generate melodies:

s = Server().boot()
s.start()
wav = SquareTable()
env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
met = Metro(.125, 12).play()
amp = TrigEnv(met, table=env, mul=.1)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
out = Osc(table=wav, freq=pit, mul=amp).out()
s.gui(locals())
