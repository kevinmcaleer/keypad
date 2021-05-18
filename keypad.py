# A simple keypad Demo
# Kevin McAleer
# May 2021

from machine import Pin, Timer
from time import sleep

class KeyPad():

    # CONSTANTS
    KEY_UP   = const(0)
    KEY_DOWN = const(1)

    def __init__(self):

        keys = [
                '1', '2', '3', 'A',
                '4', '5', '6', 'B',
                '7', '8', '9', 'C',
                '*', '0', '#', 'D',
            ]
        
        self.keys = [ {'char':key, 'state' : self.KEY_UP} for key in keys ]

        # Pin names for Pico
        self.rows = [0, 1, 2, 3]
        self.cols = [4, 5, 6, 7]

        # set pins for rows as outputs
        self.row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in self.rows]

        # set pins for cols as inputs
        self.col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in self.cols]

        self.timer = Timer()
        self.timer.init(freq=100, mode=Timer.PERIODIC)
        # self.timer.callback(None)

        self.scan_row = 0
        self.key_code = None
        self.key_char = None


    def get_key(self):
        """ Get last key pressed """

        key_char = self.key_char
        self.key_code = None
        self.key_char = None

        return key_char

    def key_process(self, key_code, col_pin):
        """ Process a key press or release """

        key_event = None
        if col_pin.value():
            if self.keys[key_code]['state'] == self.KEY_UP:
                key_event = self.KEY_DOWN
                self.keys[key_code]['state' == key_event]
        else:
            if self.keys[key_code]['state'] == self.KEY_DOWN:
                key_event = self.KEY_UP
                self.keys[key_code]['state'] == key_event

        return key_event

    def scan_row_update(self):

        self.row_pins[self.scan_row].value(0)

        self.scan_row = (self.scan_row + 1) % len(self.row_pins)

        self.row_pins[self.scan_row].value(1)

    def timer_callback(self, timer):
        key_code = self.scan_row * len(self.cols)

        for col in range(len(self.cols)):
            # process state
            key_event = self.key_process(key_code,self.col_pins[col])

            # proces key event
            if key_event == self.KEY_DOWN:
                self.key_code = key_code
                self.key_char = self.keys[key_code]['char']

            # Next key code
            key_code += 1

        self.scan_row_update()

    def start(self):
        """ Start the timer """
        self.timer.init(callback=self.timer_callback)

    def stop(self):
        """ Stop the timer """
        self.timer.init(callback=None)

# create a keypad

print("starting")
keypad = KeyPad()
keypad.start()

# loop forever
while True:
    key = keypad.get_key()
    if key:
        print("keypad: got key:", key)
        sleep(1)

keypad.stop()