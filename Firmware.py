import serial
import serial.tools.list_ports
import time
import pyautogui

BAUD_RATE = 115200
def find_esp32_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "USB Serial" in p.description or "Standard" in p.description:
            return p.device
    return None

PORT = find_esp32_port()

if not PORT:
    print("Could not find ESP32. Please enter COM port manually (e.g. COM3):")
    PORT = input().strip()

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {PORT}")
except:
    print(f"Failed to connect to {PORT}. Check your connection.")
    exit()

print("Listening for button presses... (Press Ctrl+C to stop)")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            if "Button Pressed: 1" in line:
                print("Action: Volume Up")
                pyautogui.press('volumeup')
                
            elif "Button Pressed: 2" in line:
                print("Action: Volume Down")
                pyautogui.press('volumedown')
                
            elif "Button Pressed: 3" in line:
                print("Action: Toggle Mute")
                pyautogui.press('volumemute')
                
            elif "Button Pressed: 10" in line:
                print("Action: Play/Pause Media")
                pyautogui.press('playpause')

            elif "Encoder Value: " in line:
                pass

        time.sleep(0.01)
    except KeyboardInterrupt:
        print("Stopping...")
        ser.close()
        break
    except Exception as e:
        print(f"Error: {e}")
        break
