KEYBOARD_KEY_TO_MIDI_NOTE = {
    "a": 60, # C3
    "w": 61, # C#3
    "s": 62, # D3
    "e": 63, # D#3
    "d": 64, # E3
    "f": 65, # F3
    "t": 66, # F#3
    "g": 67, # G3
    "y": 68, # G#3
    "h": 69, # A3
    "u": 70, # A#3
    "j": 71, # B3
    "k": 72, # C4
}


from config import CENTRAL_NOTE

def midi_note_to_speed(midi_note):
    difference = midi_note - CENTRAL_NOTE
    return pow(2, difference / 12)
