from pynput import mouse
from pynput import keyboard as keyb
import keyboard
from screeninfo import get_monitors

# Distance to move the cursor
MOVE_DISTANCE_X = 340
MOVE_DISTANCE_Y = 250

# State to track pressed keys
pressed_keys = set()

# State to track if listener is active
listener_active = False

# Setup mouse controller
mouse_controller = mouse.Controller()

# Dictionary to map key codes to numbers on the numlock keypad
numlock_keys = {
    96: 0,
    97: 1,
    98: 2,
    99: 3,
    100: 4,
    101: 5,
    102: 6,
    103: 7,
    104: 8,
    105: 9
}


def start_listener():
    global listener_active
    listener_active = not listener_active
    if listener_active:
        print("Listener activated")
    else:
        print("Listener deactivated")

def keychar(char):
    return keyb.KeyCode.from_char(char)

def default_courser(num):
    x_guide = [0.25,0.5,0.75]
    y_guide = [0.25,0.5,0.75]

    # Get the screen dimensions
    all_monitor = get_monitors()
    monitor = None
    for m in all_monitor:
        if m.is_primary:
            monitor = m
    print(monitor)
    if num == 7:
        x = monitor.width * x_guide[0]
        y = monitor.height * y_guide[0]
    elif num == 8:
        x = monitor.width * x_guide[1]
        y = monitor.height * y_guide[0]
    elif num == 9:
        x = monitor.width * x_guide[2]
        y = monitor.height * y_guide[0]

    elif num == 4:
        x = monitor.width * x_guide[0]
        y = monitor.height * y_guide[1]
    elif num == 5:
        x = monitor.width * x_guide[1]
        y = monitor.height * y_guide[1]
    elif num == 6:
        x = monitor.width * x_guide[2]
        y = monitor.height * y_guide[1]

    elif num == 1:
        x = monitor.width * x_guide[0]
        y = monitor.height * y_guide[2]
    elif num == 2:
        x = monitor.width * x_guide[1]
        y = monitor.height * y_guide[2]
    elif num == 3:
        x = monitor.width * x_guide[2]
        y = monitor.height * y_guide[2]
    else:
        x = monitor.width // 2
        y =  monitor.height // 2
    mouse_controller.position = (x, y)

    print(monitor.width,monitor.height)

# Function to move the cursor
def on_press(key):
    try:
        # Toggle script
        pressed_keys.add(key)
        if keyboard.is_pressed('alt+s'):
            start_listener()
            return

        # Terminate script
        if  keyboard.is_pressed('alt+d'):
            print("Exiting...")
            exit()

        # Move mouse if listener is active
        if listener_active:
            print(key)
            # Move curser with arrows
            if key in [keyb.Key.left, keyb.Key.right, keyb.Key.up, keyb.Key.down]:
                print("ARROW")
                move_cursor() 

            # Fast move with numpad.
            elif hasattr(key, 'vk') and key.vk in numlock_keys:
                print("WORKED",key)
                default_courser(numlock_keys[key.vk])

            # Click when pressing space
            elif key == keyb.Key.space:
                mouse_controller.click(mouse.Button.left, 1)
        
    except Exception as e:
        print(f"Error occurred: {e}")

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

def move_cursor():
    # Get current position of the cursor
    x, y = mouse_controller.position

    # Determine new position based on pressed keys
    if keyb.Key.up in pressed_keys and keyb.Key.left in pressed_keys:
        mouse_controller.position = (x - MOVE_DISTANCE_X, y - MOVE_DISTANCE_Y)
    elif keyb.Key.up in pressed_keys and keyb.Key.right in pressed_keys:
        mouse_controller.position = (x + MOVE_DISTANCE_X, y - MOVE_DISTANCE_Y)
    elif keyb.Key.down in pressed_keys and keyb.Key.left in pressed_keys:
        mouse_controller.position = (x - MOVE_DISTANCE_X, y + MOVE_DISTANCE_Y)
    elif keyb.Key.down in pressed_keys and keyb.Key.right in pressed_keys:
        mouse_controller.position = (x + MOVE_DISTANCE_X, y + MOVE_DISTANCE_Y)
    else:
        if keyb.Key.up in pressed_keys:
            mouse_controller.position = (x, y - MOVE_DISTANCE_Y)
        if keyb.Key.down in pressed_keys:
            mouse_controller.position = (x, y + MOVE_DISTANCE_Y)
        if keyb.Key.left in pressed_keys:
            mouse_controller.position = (x - MOVE_DISTANCE_X, y)
        if keyb.Key.right in pressed_keys:
            mouse_controller.position = (x + MOVE_DISTANCE_X, y)


def ctrl_pressed():
    print("CTRL!")

# Setup keyboard listener
with keyb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
