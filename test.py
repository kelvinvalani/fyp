import sys
from pynput import keyboard

def on_key_press(key):
    try:
        if key == keyboard.Key.space:
            print('Space bar pressed')
        elif key in [keyboard.Key.left, keyboard.Key.right, keyboard.Key.up, keyboard.Key.down]:
            print(f'Arrow key pressed: {key}')
        elif key.char == 'q':
            print('Exiting the script.')
            sys.exit()  # Exit the script when 'q' is pressed
    except AttributeError:
        # Handle non-special keys if needed
        pass

def on_key_release(key):
    # You can add code here to handle key releases if needed
    pass

# Create a listener for keyboard events
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
