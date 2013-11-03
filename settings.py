spectraldelay = [
	{'name': 'del-sin', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'fb-sin', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	{'name': 'gain-flat', 'min': 0., 'max': 1., 'default': 1., 'type': 'float'},
	]

stepvibrato = [
	{'name': 'depth', 'min': 0, 'max': 40, 'default': 15, 'type': 'float'},
	{'name': 'speed', 'min': 0, 'max': 5, 'default': 1, 'type': 'float'},
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