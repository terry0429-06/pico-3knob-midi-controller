import time
import board
import analogio
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

pot1 = analogio.AnalogIn(board.GP26)
pot2 = analogio.AnalogIn(board.GP27)
pot3 = analogio.AnalogIn(board.GP28)

CC_Nums = [14, 15, 16]

last_values = [None, None, None]

THRESHOLD = 3

def read_pot(pot):
    return 127 - int(pot.value * 127/65535)

while True:
    pots = [pot1, pot2, pot3]
    
    for i, pot in enumerate(pots):
        raw_val = read_pot(pot)

        if last_values[i] is None or abs(raw_val - last_values[i]) >= THRESHOLD:
            last_values[i] = raw_val
        
            cc_msg = ControlChange(CC_Nums[i], raw_val)
            midi.send(cc_msg)
            print(f"Pot {i+1} (GP {26 + i}) -> CC{CC_Nums[i]}): {raw_val}")
        
    time.sleep(0.06)