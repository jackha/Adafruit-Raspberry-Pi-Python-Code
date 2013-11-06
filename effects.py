from time import sleep

class Effects(object):

    # Option names in Pd.
    option_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def __init__(self, loader_socket, available_effects, off_effect):
        self.current_effect = 0  # by index of AVAILABLE_EFFECTS
        self.loader_socket = loader_socket
        self.loaded = False
        self.loaded_patch = None  
        self.available_effects = available_effects
        self.current_settings = 8*[0]
        self.step_sizes = 8*[1]  # for settings
        #self.load()
        self.effect_on = False
        self.load(off_effect['patch_name'])
        self.off_effect = off_effect
        self.scrollers = []
        for effect in self.available_effects:
            self.scrollers.append(Scroller(effect['full_name']))

    @property
    def settings(self):
        return self.available_effects[self.current_effect]['settings']

    @property
    def patch_name(self):
        display_name = self.available_effects[self.current_effect]['patch_name']
        return display_name

    @property
    def scroller(self):
        """return current scroller"""
        return self.scrollers[self.current_effect]

    @property
    def display_name(self):
        return self.available_effects[self.current_effect]['display_name']

    def effect_on_off(self):
        self.effect_on = not self.effect_on
        self.unload()
        if self.effect_on:
            self.load()
        else:
            self.load(self.off_effect['patch_name'])
        self.set_default_settings()

    def up(self):
        if self.effect_on:
            self.unload()
        self.current_effect = (self.current_effect + 1) % len(self.available_effects)
        if self.effect_on:
            self.load()
            self.set_default_settings()

    def down(self):
        if self.effect_on:
            self.unload()
        self.current_effect = (self.current_effect - 1) % len(self.available_effects)
        if self.effect_on:
            self.load()
            self.set_default_settings()

    def load(self, patch_name=None):
        if patch_name is None:
            patch_name = self.patch_name
        if self.loaded:
            return
        self.loaded = True
        self.loaded_patch = patch_name
        self.loader_socket.sendall('load %s;' % patch_name)
        sleep(0.3)  # essential! Or Pd will sometimes stop with a segmentation fault.
        self.send_sock = init_pd_socket()

    def unload(self):
        if not self.loaded:
            return
        self.send_sock.close()
        sleep(.2)  # essential!
        self.loader_socket.sendall('unload %s;' % self.loaded_patch)
        self.loaded = False
        self.loaded_patch = None

    def set_default_settings(self):
        """ Set all default settings and determine step sizes"""
        for idx, setting in enumerate(self.settings):
            self.current_settings[idx] = setting['default']
            if setting['type'] == 'float':
                self.step_sizes[idx] = (setting['max'] - setting['min']) / 100.
            else:
                self.step_sizes[idx] = 1
            self.setting(idx, 0)

    def setting(self, idx, value=None, delta=0):
        """ Add delta to setting and update to Pd. 

        Return curr value"""
        if idx >= len(self.settings):
            return
        if value is not None:
            self.current_settings[idx] = value
        self.current_settings[idx] += delta * self.step_sizes[idx]
        if self.current_settings[idx] < self.settings[idx]['min']:
            self.current_settings[idx] = self.settings[idx]['min']
        if self.current_settings[idx] > self.settings[idx]['max']:
            self.current_settings[idx] = self.settings[idx]['max']
        if self.settings[idx]['type'] == 'float':
            self.send_sock.sendall('%s %f;' % (self.option_names[idx], self.current_settings[idx]))
        else:
            self.send_sock.sendall('%s %d;' % (self.option_names[idx], self.current_settings[idx]))
        return self.current_settings[idx]

    def settings_as_eight(self, selected=None):
        """Return byte array of 8 settings. Optionally give index for selected setting"""
        lookup_add = [128, 1, 2, 4, 8, 16, 32, 64]
        result = []
        for row in range(0, len(self.settings)):
            row_value = lookup_add[0] if selected==row else 0
            normalized_value = (7*(float(self.current_settings[row]) - self.settings[row]['min']) / 
                    (self.settings[row]['max'] - self.settings[row]['min']))
            for col in range(0, 7):
                if normalized_value >= col:
                    row_value += lookup_add[col+1]

            result.append(row_value)
        for row in range(len(self.settings), 8):
            result.append(0)
        return result
