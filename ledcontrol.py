import RPi.GPIO as GPIO
import wiringpi2 as wp
import time
import sys
from threading import Thread, Event

class LedControl:
  def __init__(self, leds, interpolator=0.01):
    """ setup the ports """ 
    self.leds = leds
    wp.wiringPiSetupGpio()
    for pin in self.leds.values():
      wp.pinMode(pin, 1)
      wp.softPwmCreate(pin, 0,100)

  def setLevel(self, level): # TODO use snake case #ugly
    """ set level of all the pwms to level
        :level: the intensity from 0 to 100
    """
    for pin in self.leds.values():
      wp.softPwmWrite(pin, level)

def main():
  try:
    leds = {'red': 16, 'blue': 20, 'green': 21}
    m = LedControl(leds)
    while 1:
      for level in range(101):
        m.setLevel(level)
        time.sleep(0.01)
      for level in range(100, 0, -1):
        m.setLevel(level)
        time.sleep(0.01)
  #except KeyboardInterrupt
  except Exception, e:
     print e
  sys.exit(0)

if __name__ == '__main__':
  main()
