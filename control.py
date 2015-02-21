from sound import TapTester
from ledcontrol import LedControl
import time

ZERO=12
ONE=40

if __name__ == "__main__":
    tt = TapTester()


    leds = {'red': 16, 'blue': 20, 'green': 21}
    last = 0
    last_time = time.time()
    m = LedControl(leds)
    try:
        while 1:
            amp = tt.listen()

            try:
              level = 100*(amp-ZERO)/(ONE-ZERO)
            except KeyboardInterrupt:
              raise
            except:
              print "level was reset to 0"
              level = 0
            a = min(100, max(0, level))
            if a > last:
                boost = 7
            else:
                boost = 3

            next = last+(a-last)*(time.time()-last_time)*boost

            m.setLevel(int(next))

            last=next
            last_time=time.time()
    except Exception as e:
        m.clean()
        print str(e)
