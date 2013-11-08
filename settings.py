from display import SPIRAL_DISPLAY, MIX_DISPLAY


spectraldelay = [
	{'name': 'mmix', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'display': MIX_DISPLAY, 'exp1': {'min': 0, 'max': 1}},
	{'name': ' del', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': '  fb', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'gain', 'min': 0., 'max': 1., 'default': 1., 'type': 'float', 'display': MIX_DISPLAY},
	{'name': 'lpfq', 'min': 1, 'max': 880, 'default': 220, 'type': 'float'},
	{'name': 'slpe', 'min': -0.1, 'max': -0.001, 'default': -0.04, 'type': 'float'},
	]

stepvibrato = [
	{'name': 'depth', 'min': 0., 'max': 40., 'default': 15., 'type': 'float', 'exp1': {'min': 10, 'max': 20}},
	{'name': 'speed', 'min': 0.5, 'max': 30., 'default': 4., 'type': 'float', 'exp1': {'min': 10, 'max': 0.5}},
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

reverb = [
	{'name': 'mmix', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float', 'display': MIX_DISPLAY},
	{'name': 'roomsize', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
	{'name': 'damping', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
]

weird = [
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': -0.9, 'max': 0.9, 'default': 0, 'type': 'float'},
]

fourtap = [
	{'name': 'dunno', 'min': 0, 'max': 25, 'default': 15, 'type': 'float'},
	{'name': 'mod-add', 'min': 0, 'max': 15, 'default': 5, 'type': 'integer'},
	{'name': 'mod-multiply', 'min': 0, 'max': 15, 'default': 5, 'type': 'integer'},
	]

diy2pitch = [
	{'name': 'transpose', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'window', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'delay', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'gain', 'min': 0, 'max': 1, 'default': 0.8, 'type': 'float'},
	{'name': 'metro-speed', 'min': 100, 'max': 2000, 'default': 1000, 'type': 'float'},
	{'name': 'metro-vol', 'min': 0, 'max': 1, 'default': 0, 'type': 'float'},	
]