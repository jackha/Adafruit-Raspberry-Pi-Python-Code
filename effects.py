from time import sleep
import socket
from scroller import Scroller


def init_pd_socket():
    # Create a socket (SOCK_STREAM means a TCP socket)
    # client of puredata: use 'netreceive 3000' in pd
    print "init send socket to Pd..."
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.connect(('localhost', 3000))
    return send_sock
    

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
        #self.step_sizes = 8*[1]  # for settings
        #self.load()
        self.effect_on = False
        self.load(off_effect['patch_name'])
        self.off_effect = off_effect
        self.scrollers = []
        # Determine step sizes
        self.step_sizes = []
        self.exp1 = []
        self.exp2 = []
        self.ldr = []

        self.off_step_sizes = []
        self.off_exp1 = {}
        self.off_settings = 8*[0]  # Off has settings too!

        for idx, setting in enumerate(self.off_effect['settings']):
            if setting['type'] == 'float':
                self.off_step_sizes.append((setting['max'] - setting['min']) / 100.)
            else:
                self.off_step_sizes.append(1)
            if 'exp1' in setting:
                self.off_exp1[idx] = setting['exp1']

        for effect in self.available_effects:
            curr_step_sizes = []
            curr_exp1 = {}  # key is option number, value is {'min': xx, 'max': yy}
            curr_exp2 = {}
            curr_ldr = {}
            for idx, setting in enumerate(effect['settings']):
                if setting['type'] == 'float':
                    curr_step_sizes.append((setting['max'] - setting['min']) / 100.)
                else:
                    curr_step_sizes.append(1)
                if 'exp1' in setting:
                    curr_exp1[idx] = setting['exp1']
                if 'exp2' in setting:
                    curr_exp2[idx] = setting['exp2']
                if 'ldr' in setting:
                    curr_ldr[idx] = setting['ldr']
            self.step_sizes.append(curr_step_sizes)
            self.exp1.append(curr_exp1)
            self.exp2.append(curr_exp2)
            self.ldr.append(curr_ldr)
        #for effect in self.available_effects:
        #    self.scrollers.append(Scroller(effect['full_name']))

    @property
    def settings(self):
        return self.available_effects[self.current_effect]['settings']

    def step_size(self, idx):
        return self.step_sizes[self.current_effect][idx]

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
        sleep(0.2)  # essential! Or Pd will sometimes stop with a segmentation fault.
        self.send_sock = init_pd_socket()

    def unload(self):
        if not self.loaded:
            return
        self.send_sock.close()
        sleep(.1)  # essential!
        self.loader_socket.sendall('unload %s;' % self.loaded_patch)
        self.loaded = False
        self.loaded_patch = None

    def set_default_settings(self):
        """ Set all default settings"""
        for idx, setting in enumerate(self.settings):
            self.current_settings[idx] = setting['default']
            self.setting(idx, self.current_settings[idx])

    def setting(self, idx, value=None, delta=0):
        """ Add delta to setting and update to Pd. 

        Return curr value"""
        if not self.effect_on:
            # do our effect off thing, ugly because it's the same as effect on
            # print 'off setting' + str(idx) + ' ' + str(value)
            idx = 0
            if value is not None:
                self.off_settings[idx] = value
            self.off_settings[idx] += delta * self.off_step_sizes[idx]
            if self.off_settings[idx] < self.off_effect['settings'][idx]['min']:
                self.off_settings[idx] = self.off_effect['settings'][idx]['min']
            if self.off_settings[idx] > self.off_effect['settings'][idx]['max']:
                self.off_settings[idx] = self.off_effect['settings'][idx]['max']
            if self.off_effect['settings'][idx]['type'] == 'float':
                self.send_sock.sendall('%s %f;' % (self.option_names[idx], self.off_settings[idx]))
            else:
                self.send_sock.sendall('%s %d;' % (self.option_names[idx], self.off_settings[idx]))
            return self.off_settings[idx]

        if idx >= len(self.settings):
            return
        if value is not None:
            self.current_settings[idx] = value
        self.current_settings[idx] += delta * self.step_size(idx)
        if self.current_settings[idx] < self.settings[idx]['min']:
            self.current_settings[idx] = self.settings[idx]['min']
        if self.current_settings[idx] > self.settings[idx]['max']:
            self.current_settings[idx] = self.settings[idx]['max']
        if self.settings[idx]['type'] == 'float':
            self.send_sock.sendall('%s %f;' % (self.option_names[idx], self.current_settings[idx]))
        else:
            self.send_sock.sendall('%s %d;' % (self.option_names[idx], self.current_settings[idx]))
        return self.current_settings[idx]

    def setting_norm(self, idx):
        """Return normalized value 0..1"""
        if self.effect_on:
            return ((float(self.current_settings[idx]) - self.settings[idx]['min']) / 
                        (self.settings[idx]['max'] - self.settings[idx]['min']))
        else:
            return ((float(self.off_settings[idx]) - self.off_settings[idx]['min']) / 
                        (self.off_settings[idx]['max'] - self.off_settings[idx]['min']))

    def expression1(self, raw_value):
        """Raw value is 0..1023"""
        if self.effect_on:
            for k, v in self.exp1[self.current_effect].items():
                value = v['min'] + raw_value / 1024. * (v['max'] - v['min'])
                self.setting(k, value=value)
        else:
            for k, v in self.off_exp1.items():
                value = v['min'] + raw_value / 1024. * (v['max'] - v['min'])
                self.setting(k, value=value)

    def expression2(self, raw_value):
        for k, v in self.exp2[self.current_effect].items():
            value = v['min'] + raw_value / 1024. * (v['max'] - v['min'])
            self.setting(k, value=value)

    def lightsensor(self, raw_value):
        for k, v in self.ldr[self.current_effect].items():
            value = v['min'] + raw_value / 1024. * (v['max'] - v['min'])
            self.setting(k, value=value)

    def settings_as_eight(self, selected=None):
        """Return byte array of 8 settings. Optionally give index for selected setting"""
        lookup_add = [128, 1, 2, 4, 8, 16, 32, 64]
        if not self.effect_on:
            # TODO: currently this is lame. Use display function instead.
            value = self.off_settings[0]
            row_value = 0
            normalized_value = (8*(float(value) - self.off_effect['settings'][0]['min']) / 
                (self.off_effect['settings'][0]['max'] - self.off_effect['settings'][0]['min']))
            for col in range(0, 8):
                if normalized_value >= col:
                    row_value += lookup_add[col]
            return 8*[row_value]
        
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
