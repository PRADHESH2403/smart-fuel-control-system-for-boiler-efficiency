# --- Import Libraries ---
import machine
import time
from machine import I2C, Pin, PWM
from time import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# --- Initialize LEDs ---
green_led = machine.Pin(15, machine.Pin.OUT)  # Green LED (Oxygen Required)
red_led = machine.Pin(16, machine.Pin.OUT)    # Red LED (Excess Air)

# --- Initialize I2C LCD ---
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # I2C Bus 0
lcd = I2cLcd(i2c, 0x27, 2, 16)  # LCD Address 0x27, 16x2 Display

# --- Initialize Motor Control Pins (L298N Driver) ---
motor_in1 = machine.Pin(12, machine.Pin.OUT)
motor_in2 = machine.Pin(13, machine.Pin.OUT)
motor_en = machine.PWM(machine.Pin(11))  # Motor Enable Pin as PWM
motor_en.freq(1000)  # Set PWM frequency to 1kHz

# --- Motor Control Functions ---
def motor_forward():
    motor_en.duty_u16(16384)  # 50% duty cycle
    motor_in1.value(1)
    motor_in2.value(0)
    return "FWD"

def motor_reverse():
    motor_en.duty_u16(16384)
    motor_in1.value(0)
    motor_in2.value(1)
    return "REV"

def motor_stop():
    motor_en.duty_u16(0)  # Motor Stop
    motor_in1.value(0)
    motor_in2.value(0)
    return "STOP"

# --- Combustion Calculation Functions ---
def calculate_oxygen_requirement(c, h2, s, o2):
    """Calculate oxygen required for complete combustion"""
    return (8/3 * c) + (8 * h2) + s - o2

def calculate_air_requirement(oxygen_needed):
    """Calculate minimum air required for combustion"""
    return (100/23) * oxygen_needed

def calculate_flue_gas(c, h2, s, n):
    """Calculate flue gas production"""
    return (11/3 * c) + (9 * h2) + (2 * s) + n

# --- Main Program Loop ---
while True:
    # --- Input Section ---
    print("\n### Enter Coal Composition in Decimal Fraction ###")
    c = float(input("Carbon (C): "))
    h2 = float(input("Hydrogen (H2): "))
    s = float(input("Sulphur (S): "))
    o2 = float(input("Oxygen (O2): "))
    n = float(input("Nitrogen (N2): "))

    total_coal_supplied = float(input("Enter total coal supplied to boiler (TPH): "))
    total_air_supply = float(input("Enter total air supply (TPH): "))

    # --- Calculation Section ---
    oxygen_needed = calculate_oxygen_requirement(c, h2, s, o2) * total_coal_supplied
    min_air = calculate_air_requirement(oxygen_needed)
    flue_gas = calculate_flue_gas(c, h2, s, n)
    excess_air = total_air_supply - min_air

    # --- Display Results (Terminal) ---
    print(f"\nOxygen Required: {oxygen_needed:.2f} TPH")
    print(f"Minimum Air Required: {min_air:.2f} TPH")
    print(f"Flue Gas Produced: {flue_gas:.2f} TPH")
    print(f"Total Coal Supplied: {total_coal_supplied:.2f} TPH")
    print(f"Total Air Supply: {total_air_supply:.2f} TPH")
    print(f"Excess Air: {excess_air:.2f} TPH")

    # --- LED and Motor Control Logic ---
    if total_air_supply < min_air:
        # Less air supplied -> Need more oxygen
        green_led.value(1)
        red_led.value(0)
        motor_status = motor_forward()
        print("Status: More Oxygen Needed (Green LED ON, Motor Forward)")

    elif total_air_supply > min_air:
        # More air supplied -> Excess oxygen
        green_led.value(0)
        red_led.value(1)
        motor_status = motor_reverse()
        print("Status: Excess Air (Red LED ON, Motor Reverse)")

    else:
        # Perfect air balance
        green_led.value(0)
        red_led.value(0)
        motor_status = motor_stop()
        print("Status: Oxygen Flow Stable (Both LEDs OFF, Motor Stopped)")

    # --- Display Results (LCD Display) ---
    lcd.clear()
    lcd.putstr(f"Min Air:{min_air:.1f}TPH")
    lcd.putstr(f"Flue Gas:{flue_gas:.1f}TPH")
    sleep(6)

    lcd.clear()
    lcd.putstr(f"Excess Air:{excess_air:.1f}TPH")
    lcd.putstr(f"Motor:{motor_status}")
    sleep(4)

    # --- Reset States Before Next Input ---
    time.sleep(6)
    green_led.value(0)
    red_led.value(0)
    motor_stop()

    # --- Short Delay ---
    time.sleep(3)
    lcd.clear()
