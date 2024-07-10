from pynput import mouse, keyboard
from screeninfo import get_monitors

numpad_mapping = {
    keyboard.Key.numpad0: '0',
    keyboard.Key.numpad1: '1',
    keyboard.Key.numpad2: '2',
    keyboard.Key.numpad3: '3',
    keyboard.Key.numpad4: '4',
    keyboard.Key.numpad5: '5',
    keyboard.Key.numpad6: '6',
    keyboard.Key.numpad7: '7',
    keyboard.Key.numpad8: '8',
    keyboard.Key.numpad9: '9',
}

# Distance to move the cursor
MOVE_DISTANCE = 20

# State to track pressed keys
pressed_keys = set()

# State to track if listener is active
listener_active = False

# Setup mouse controller
mouse_controller = mouse.Controller()

def start_listener():
    global listener_active
    listener_active = not listener_active
    if listener_active:
        print("Listener activated")
    else:
        print("Listener deactivated")

def keychar(char):
    return keyboard.KeyCode.from_char(char)

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
        pressed_keys.add(key)
        print(int(key))
        # Check for Ctrl + M combination
        if  keychar("q") in pressed_keys and keychar("w") in pressed_keys and keychar("e") in pressed_keys:
            start_listener()
            return

        # Exit condition: Ctrl + K
        if  keychar("a") in pressed_keys and keychar("s") in pressed_keys and keychar("d") in pressed_keys:
            print("Exiting...")
            exit()

        # Move mouse if listener is active
        if listener_active:
            move_cursor()

        if isinstance(key, keyboard.KeyCode):
            if key.char.isdigit():
                default_courser(int(key.char))

    except AttributeError:
        pass

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

def move_cursor():
    # Get current position of the cursor
    x, y = mouse_controller.position

    # Determine new position based on pressed keys
    if keyboard.Key.up in pressed_keys and keyboard.Key.left in pressed_keys:
        mouse_controller.position = (x - MOVE_DISTANCE, y - MOVE_DISTANCE)
    elif keyboard.Key.up in pressed_keys and keyboard.Key.right in pressed_keys:
        mouse_controller.position = (x + MOVE_DISTANCE, y - MOVE_DISTANCE)
    elif keyboard.Key.down in pressed_keys and keyboard.Key.left in pressed_keys:
        mouse_controller.position = (x - MOVE_DISTANCE, y + MOVE_DISTANCE)
    elif keyboard.Key.down in pressed_keys and keyboard.Key.right in pressed_keys:
        mouse_controller.position = (x + MOVE_DISTANCE, y + MOVE_DISTANCE)
    else:
        if keyboard.Key.up in pressed_keys:
            mouse_controller.position = (x, y - MOVE_DISTANCE)
        if keyboard.Key.down in pressed_keys:
            mouse_controller.position = (x, y + MOVE_DISTANCE)
        if keyboard.Key.left in pressed_keys:
            mouse_controller.position = (x - MOVE_DISTANCE, y)
        if keyboard.Key.right in pressed_keys:
            mouse_controller.position = (x + MOVE_DISTANCE, y)
    if keyboard.Key.space in pressed_keys:
        mouse_controller.click(mouse.Button.left, 1)

# Setup keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
