# sesame-melody

Python-based framework for melody recognition on a Raspberry Pi.


http://raspberrypi.stackexchange.com/questions/19705/usb-card-as-my-default-audio-device

## LED

LED (Kingbright, L-115WEGW bi-color LED) is up and running using the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) python module.

### Wiring
* PIN14 GND (longest/center LED pin)
* PIN13 RED (next longest/right LED pin)
* PIN16 GREEN (shortest/left LED pin)

## Dot Matrix Display

Dot Matrix Display (Kingbright, TA07-11SRWA, 5x7) up and running using the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) python module. 

### Wiring
C for column
R for row
DMD for internal wiring
GPIO pin naming
PIN physical numbering
* C1 = DMD1  = GPIO11 = PIN23
* C2 = DMD3  = GPIO8  = PIN24
* C3 = DMD10 = GPIO7  = PIN26
* C4 = DMD7  = GPIO5  = PIN29
* C5 = DMD8  = GPIO6  = PIN31
* R1 = DMD12 = GPIO12 = PIN32
* R2 = DMD11 = GPIO13 = PIN33
* R3 = DMD2  = GPIO19 = PIN35
* R4 = DMD9  = GPIO16 = PIN36
* R5 = DMD4  = GPIO26 = PIN37
* R6 = DMD5  = GPIO20 = PIN38
* R7 = DMD6  = GPIO21 = PIN40

## Servo

Using the [RPIO](http://pythonhosted.org/RPIO/index.html) python module the servo control works with PIN 12/GPIO 18 and its hardware PWM as signal PIN. See [servo-hpwm-test.py](/servo-hpwm-test.py) for a working example. (I also tried the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) module with less success as it is using a not that stable software emulated PWM; see [servo-test.py](/servo-test.py))

### Wiring
* PIN2 +5V (red)
* PIN6 GND (brown)
* PIN12 PWM signal (yellow)

### Some links
* http://pythonhosted.org/RPIO/index.html
* http://stackoverflow.com/questions/20081286/controlling-a-servo-with-raspberry-pi-using-the-hardware-pwm-with-wiringpi
* http://raspberrypi.stackexchange.com/questions/298/can-i-use-the-gpio-for-pulse-width-modulation-pwm
* http://elinux.org/RPi_BCM2835_GPIOs
* http://elinux.org/RPi_Low-level_peripherals
* https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2835/README.md
* https://www.raspberrypi.org/documentation/usage/gpio/README.md
* https://www.raspberrypi.org/documentation/hardware/raspberrypi/gpio/README.md
 
