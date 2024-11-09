import pyautogui
import time
from PIL import ImageGrab
import numpy as np
import keyboard

# Prevent auto-clicker from going out of control
pyautogui.FAILSAFE = True

def detect_color(x, y, width, height):
    """
    Detect if the specified region contains more green or red pixels
    Returns: 'green' or 'red'
    """
    screenshot = np.array(ImageGrab.grab(bbox=(x, y, x + width, y + height)))
    
    # Define color ranges (BGR format)
    green_mask = (screenshot[:, :, 1] > 100) & (screenshot[:, :, 0] < 100)
    red_mask = (screenshot[:, :, 2] > 100) & (screenshot[:, :, 1] < 100)
    
    green_pixels = np.sum(green_mask)
    red_pixels = np.sum(red_mask)
    
    return 'green' if green_pixels > red_pixels else 'red'

def setup_positions():
    """
    Setup clicking positions for the trading interface
    """
    print("Setup mode:")
    positions = {}
    
    print("Move your mouse to the BUY button and press 'b'")
    while 'buy' not in positions:
        if keyboard.is_pressed('b'):
            positions['buy'] = pyautogui.position()
            time.sleep(0.5)
    
    print("Move your mouse to the SELL button and press 's'")
    while 'sell' not in positions:
        if keyboard.is_pressed('s'):
            positions['sell'] = pyautogui.position()
            time.sleep(0.5)
    
    print("Move your mouse to the price indicator area and press 'p'")
    while 'price' not in positions:
        if keyboard.is_pressed('p'):
            positions['price'] = pyautogui.position()
            time.sleep(0.5)
    
    return positions

def main():
    print("Trading Auto Clicker")
    print("-------------------")
    print("1. First, we'll set up the button positions")
    print("2. Press 'q' at any time to quit")
    print("3. Press 'r' to start/pause the auto clicker")
    
    # Get button positions
    positions = setup_positions()
    
    print("\nSetup complete! Press 'r' to start auto clicking")
    
    running = False
    while True:
        # Check for quit command
        if keyboard.is_pressed('q'):
            print("Quitting...")
            break
            
        # Toggle running state
        if keyboard.is_pressed('r'):
            running = not running
            print("Auto clicker:", "Running" if running else "Paused")
            time.sleep(0.3)
        
        if running:
            # Get the color from the price area
            color = detect_color(
                positions['price'].x - 50,  # Adjust these values based on your interface
                positions['price'].y - 50,
                100,  # width of detection area
                100   # height of detection area
            )
            
            # Click appropriate button based on color
            if color == 'green':
                pyautogui.click(positions['buy'])
                print("Clicked BUY")
            else:
                pyautogui.click(positions['sell'])
                print("Clicked SELL")
            
            # Wait before next check
            time.sleep(0.5)  # Adjust this delay as needed

if __name__ == "__main__":
    main()
