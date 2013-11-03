spectraldelay = [
	{'name': 'del-sin', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'fb-sin', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'gain-flat', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	]

stepvibrato = [
	{'name': 'depth', 'min': 0., 'max': 40., 'default': 15., 'type': 'float'},
	{'name': 'speed', 'min': 0.5, 'max': 30., 'default': 4., 'type': 'float'},
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
	{'name': 'mix', 'min': 0, 'max': 1, 'default': 1, 'type': 'float'},
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
	{'name': 'mix', 'min': 0, 'max': 1, 'default': 0.5, 'type': 'float'},
	{'name': 'roomsize', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
	{'name': 'damping', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'},
	{'name': 'freeze', 'min': 0, 'max': 1, 'default': 0, 'type': 'integer'},
]

weird = [
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
	{'name': 'dunno', 'min': -0.9, 'max': 0.9, 'default': 0, 'type': 'float'},
]