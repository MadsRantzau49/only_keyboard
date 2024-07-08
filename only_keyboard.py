from pynput import mouse, keyboard

# Distance to move the cursor
MOVE_DISTANCE = 10

# State to track pressed keys
pressed_keys = set()

# State to track if listener is active
listener_active = False

# Function to move the cursor
def on_press(key):
    global listener_active

    pressed_keys.add(key)
    print(pressed_keys)
    if  keyboard.Key.ctrl_l in pressed_keys and keyboard.KeyCode.from_char('p') in pressed_keys:
        listener_active = not listener_active
        if listener_active:
            print("Listener activated")
        else:
            print("Listener deactivated")
        return

    if keyboard.KeyCode.from_char('k') in pressed_keys and keyboard.Key.ctrl_l in pressed_keys:
        print("Exiting...")
        return False

    if listener_active:
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

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

# Setup mouse controller
mouse_controller = mouse.Controller()

# Setup keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
