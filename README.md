# smart-fuel-control-system-for-boiler-efficiency
An embedded system project for optimizing boiler efficiency using real-time combustion monitoring.
# 🔥 Smart Fuel Control System for Boiler Efficiency

This project uses a **Raspberry Pi Pico** running **MicroPython** to optimize combustion efficiency in boilers by controlling air supply based on the composition of coal.

---

## 📦 Features

- Real-time input of coal composition.
- Calculates:
  - Oxygen required
  - Minimum air needed
  - Flue gas produced
  - Excess air
- Motorized control of airflow using L298N driver
- LCD display of combustion data
- LED indication for excess or required oxygen

---

## 🧠 Formulae Used

- `Oxygen = (8/3 * C) + (8 * H₂) + S - O₂`
- `Minimum Air = (100/23) * Oxygen`
- `Flue Gas = (11/3 * C) + (9 * H₂) + (2 * S) + N`

---

## 🧾 File Descriptions

| File Name         | Description                          |
|------------------|--------------------------------------|
| `main.py`        | Main code with input, logic & output |
| `lcd_api.py`     | LCD driver API for MicroPython       |
| `pico_i2c_lcd.py`| LCD I2C interface wrapper            |

---

## 🔧 Hardware Used

- Raspberry Pi Pico
- 16x2 I2C LCD
- L298N Motor Driver
- Green & Red LEDs
- DC Motor
- 9V Battery

---

## 🚀 How to Run

1. Upload all `.py` files to your Raspberry Pi Pico using **Thonny IDE**.
2. Connect hardware as per GPIO pins in the code.
3. Run the script and enter coal composition when prompted.
4. Observe motor, LCD, and LED responses.

---

