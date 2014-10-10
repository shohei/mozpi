import time
import threading
import datetime

shutdown_event = threading.Event()


def dowork():
  wlen = random.random()
  sleep(wlen) # Emulate doing some work
  print 'work done in %0.2f seconds' % wlen

def main():
  while 1:
    t = threading.Thread(target=dowork)
    time.sleep(4)

if __name__ == '__main__':
    main()
