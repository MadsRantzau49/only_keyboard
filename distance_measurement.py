import pyautogui
import keyboard
from math import sqrt

class ClickDistanceMeasurer:
    def __init__(self):
        self.click_count = 0
        self.click_positions = []

    def start_measuring(self):
        print("Press 'm' key twice to measure distance.")
        keyboard.add_hotkey('m', self.on_hotkey_triggered)

    def on_hotkey_triggered(self):
        self.click_count += 1
        x, y = pyautogui.position()
        self.click_positions.append((x, y))
        
        if self.click_count == 2:
            self.measure_distance()

    def measure_distance(self):
        x1, y1 = self.click_positions[0]
        x2, y2 = self.click_positions[1]
        
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        print(f"Distance: {distance:.2f} pixels")
        
        # Reset click count and positions
        self.click_count = 0
        self.click_positions = []

if __name__ == "__main__":
    measurer = ClickDistanceMeasurer()
    measurer.start_measuring()
    keyboard.wait('esc')  # Wait for 'esc' key to exit (optional)
