from display import SPIRAL_DISPLAY, MIX_DISPLAY

off = [
	{'name': 'vol', 'min': 0., 'max': 1., 'default': 1., 'type': 'float', 'exp1': {'min': 0, 'max': 1.5}},  # max 1.5 allows for some dead space
]

midi_osc = [
	{'name': 'mstr', 'min': 0, 'max': 1, 'default': 1, 'type': 'float', 'display': MIX_DISPLAY, 'exp2': {'min': 0, 'max': 1}},
	{'name': 'tune', 'min': -36, 'max': 36, 'default': 0., 'type': 'float'},
	{'name': 'ftun', 'min': -0.5, 'max': 0.5, 'default': 0., 'type': 'float'},
	{'name': 'ftu2', 'min': -3.5, 'max': 3.5, 'default': 0., 'type': 'float', 'exp1': {'min': 0.5, 'max': 0.5}},
	]

stutter = [
	{'name': ' dly', 'min': 10, 'max': 1000, 'default': 200, 'type': 'float', 'exp1': {'min': 10, 'max': 1000}},
	{'name': 'amnt', 'min': 0, 'max': 1, 'default': 0.6, 'type': 'float'},
	{'name': ' inp', 'min': 0, 'max': 1, 'default': 0.0, 'type': 'float', 'exp2': {'min': 0, 'max': 1}},
]

spectraldelay = [
	{'name': 'mmix', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'display': MIX_DISPLAY, 'exp1': {'min': 0, 'max': 1}},
	{'name': ' del', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': '  fb', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'gain', 'min': 0., 'max': 1., 'default': 1., 'type': 'float', 'display': MIX_DISPLAY},
	{'name': 'lpfq', 'min': 1, 'max': 880, 'default': 220, 'type': 'float'},
	{'name': 'slpe', 'min': -0.1, 'max': -0.001, 'default': -0.04, 'type': 'float'},
	]

reverb = [
	{'name': 'mmix', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'display': MIX_DISPLAY},
	{'name': 'roomsize', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float', 'exp1': {'min': 0, 'max': 1}},
	{'name': 'damping', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
]

stepvibrato = [
	{'name': 'depth', 'min': 0., 'max': 40., 'default': 15., 'type': 'float', 'exp1': {'min': 20, 'max': 10}},
	{'name': 'speed', 'min': 0.5, 'max': 30., 'default': 4., 'type': 'float', 'exp1': {'min': 0.5, 'max': 10}},
]

synth = [{'name': 'octave', 'min': 0, 'max': 1, 'default': 0, 'type': 'integer'},
	]

hexxiter = [
	{'name': 'threshold', 'min': 10, 'max': 25, 'default': 15, 'type': 'float'},
	{'name': 'speed', 'min': 1000, 'max': 9000, 'default': 9000, 'type': 'float'},
	{'name': 'attack-decay', 'min': 5, 'max': 50, 'default': 50, 'type': 'float'},
	{'name': 'length', 'min': 50, 'max': 150, 'default': 60, 'type': 'float'},
	{'name': 'rev1', 'min': 0, 'max': 80, 'default': 50, 'type': 'float'},
	{'name': 'rev2', 'min': 0, 'max': 80, 'default': 60, 'type': 'float'},
	{'name': 'volume', 'min': 0.001, 'max': 1, 'default': 0.9, 'type': 'float'},
]

ringmodulator = [
	{'name': 'mmix', 'min': 0, 'max': 1, 'default': 1, 'type': 'float', 'display': MIX_DISPLAY},
	{'name': 'lfo_freq', 'min': 0, 'max': 40, 'default': 4, 'type': 'float'},

]

whammy = [
	{'name': 'orig', 'min': 0, 'max': 1, 'default': 1, 'type': 'float'},
	{'name': 'pitch1', 'min': -24, 'max': 24, 'default': 5, 'type': 'integer'},
	{'name': 'mix1', 'min': 0, 'max': 2, 'default': 1.5, 'type': 'float'},
	{'name': 'pitch2', 'min': -24, 'max': 24, 'default': 9, 'type': 'integer'},
	{'name': 'mix2', 'min': 0, 'max': 2, 'default': 0, 'type': 'float'},
]

boldaslove = [
	{'name': 'attack', 'min': 0, 'max': 600, 'default': 300, 'type': 'float'},
	{'name': 'sensitivity', 'min': 0, 'max': 100, 'default': 60, 'type': 'float'},

]

weird = [
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': -0.9, 'max': 0.9, 'default': 0, 'type': 'float'},
]

# fourtap = [
# 	{'name': 'dunno', 'min': 0, 'max': 25, 'default': 15, 'type': 'float'},
# 	{'name': 'mod-add', 'min': 0, 'max': 15, 'default': 5, 'type': 'integer'},
# 	{'name': 'mod-multiply', 'min': 0, 'max': 15, 'default': 5, 'type': 'integer'},
# 	]

diy2pitch = [
	{'name': 'transpose', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'window', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'delay', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.8, 'type': 'float'},
	{'name': 'metro-speed', 'min': 100, 'max': 2000, 'default': 1000, 'type': 'float'},
	{'name': 'metro-vol', 'min': 0, 'max': 1, 'default': 0, 'type': 'float'},	
]

diy2highpass = [
	{'name': 'cuto', 'min': 0, 'max': 1, 'default': 0.2, 'type': 'float', 'exp1': {'min': 0.5, 'max': 0}},
	{'name': 'amnt', 'min': 0, 'max': 1, 'default': 1, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
]

diy2material = [
	{'name': 'form', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'exp1': {'min': 0, 'max': 1}},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
]

diy2vcf = [
	{'name': 'cuto', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'exp1': {'min': 0, 'max': 1}},
	{'name': 'reso', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
]

diy2wetfilter = [
	{'name': ' dly', 'min': 0, 'max': 1, 'default': 1, 'type': 'float', 'exp1': {'min': 0, 'max': 1}},
	{'name': '   q', 'min': 0, 'max': 1, 'default': 1, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
]

diy2vibrato = [
	{'name': ' spd', 'min': 0, 'max': 1, 'default': 0.2, 'type': 'float', 'exp1': {'min': 0, 'max': 0.5}},
	{'name': 'dept', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
	{'name': 'fdbk', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'slope', 'min': 0.1, 'max': 5000, 'default': 0.1, 'type': 'float'},
]

diy24tap = [
	{'name': ' 1st', 'min': 0, 'max': 1, 'default': 0.1, 'type': 'float'},
	{'name': ' 2nd', 'min': 0, 'max': 1, 'default': 0.6, 'type': 'float'},
	{'name': ' 3rd', 'min': 0, 'max': 1, 'default': 0.7, 'type': 'float'},
	{'name': ' 4th', 'min': 0, 'max': 1, 'default': 0.9, 'type': 'float'},
	{'name': 'scale', 'min': 0, 'max': 1, 'default': 1, 'type': 'float', 'exp1': {'min': 0, 'max': 1}},
	{'name': 'slide', 'min': 0, 'max': 1, 'default': 1, 'type': 'float'},
]

diy2xfm = [
	{'name': 'nume', 'min': 0, 'max': 1, 'default': 0.1, 'type': 'float'},
	{'name': 'deno', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'fbka', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'fbkb', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'slid', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'type', 'min': 0, 'max': 1, 'default': 1, 'type': 'integer'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float', 'exp1': {'min': 0, 'max': 0.5}},
	{'name': 'frequency', 'min': 44, 'max': 880, 'default': 440, 'type': 'float', 'ldr': {'min': 44, 'max': 880}},
]

diy2xfm2 = [
	{'name': 'nume', 'min': 0, 'max': 1, 'default': 0.1, 'type': 'float'},
	{'name': 'deno', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'fbka', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'fbkb', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'slid', 'min': 0, 'max': 1, 'default': 0.4, 'type': 'float'},
	{'name': 'type', 'min': 0, 'max': 1, 'default': 1, 'type': 'integer'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float', 'exp1': {'min': 0, 'max': 0.5}},
]