import RPi.GPIO as GPIO
import time
from threading import Thread, Event

# we use board layout

class LedControl:
  def __init__(self, leds, interpolator=0.01):
    """ setup the ports """ 
    self.leds = leds
    GPIO.setmode(GPIO.BOARD)
    for pin in self.leds.values():
      GPIO.setup(pin, GPIO.OUT)
    self.pwms = [GPIO.PWM(pin, 150) for pin in self.leds.values()]
    for pwm in self.pwms:
      pwm.start(0)
    self.level = 0
    class ApplyThread(Thread):
      def __init__(self, pwms, event, interpolater):
        Thread.__init__(self)
        self.stopped = event
        self.currentLevel = 0
        self.level = 0
        self.pwms = pwms
	self._interpolator = interpolator
      def set_level(self, level):
        """ set level of all the pwms to level
            :level: the intensity from 0 to 100
        """
        self.level = level
      def run(self):
        while not self.stopped.wait(0.1):
          self.currentLevel += (self.level - self.currentLevel)*self._interpolator
          for pwm in self.pwms:
            pwm.ChangeDutyCycle(self.currentLevel)
    self.stop_event = Event()
    self.thread = ApplyThread(self.pwms, self.stop_event, interpolator)
    self.thread.start()

  def setLevel(self, level): # TODO use snake case #ugly
    """ set level of all the pwms to level
        :level: the intensity from 0 to 100
    """
    self.thread.set_level(level)
  def clean(self):
    self.stop_event.set()
    for pwm in self.pwms:
      pwm.stop()
    GPIO.cleanup()
    self.timer.stop()

def main():
  try:
    leds = {'red': 16, 'blue': 22, 'green': 15, 'white': 24}
    m = LedControl(leds)
    while 1:
      for level in range(101):
        m.setLevel(level)
        time.sleep(0.1)
      for level in range(100, 0, -1):
        m.setLevel(level)
        time.sleep(0.1)
  except:
    pass
  m.clean()

if __name__ == '__main__':
  main()
