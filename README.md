# sesame-melody

Python-based framework for melody recognition on a Raspberry Pi.


http://raspberrypi.stackexchange.com/questions/19705/usb-card-as-my-default-audio-device

## LED

LED is up and running using the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) python module, see [led-test.py](/led-test.py]. 

### Wiring
* PIN14 GND (longest/center LED pin)
* PIN15 RED (next longest/right LED pin)
* PIN16 GREEN (shortest/left LED pin)

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
 
