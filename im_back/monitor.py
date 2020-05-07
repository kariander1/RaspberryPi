import gpio
import time
import sys
import threading


monitors=[]
def stop_monitors():
    temp_monitors = monitors.copy()
    for monitor in temp_monitors:
        monitor.join()
class Monitor(threading.Thread):
    
    __last_thread=None
    __rate_ms=100
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    interation = 0    
    method_running = False
    def __init__(self,monitor_name,method_to_execute,rate_ms, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
        self.method_to_execute = method_to_execute
        self.__rate_ms = rate_ms
        self.monitor_name = monitor_name
        monitors.append(self)
    def set_rate(self,rate):
        self.__rate_ms=rate
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def resume(self):
        self._stop.clear()
        self.run()
    def run(self):
        #self.interation = self.interation+1
        if(self.stopped()):
            return
        th = threading.Timer(self.__rate_ms/1000, self.run)
        th.start()
        
        if self.method_running :
            #log_message(self.monitor_name+ " Previous run not finished ")#+str(self.interation))
            return
        self.method_running = True
        self.__last_thread = th
        self.method_to_execute()
        self.method_running = False
        
    def join(self, timeout=None):
        if not self.stopped():
            """ Stop the thread and wait for it to end. """
            #log_message(self.monitor_name+ ' exiting thread')
            self._stop.set()
            if(self.__last_thread!=None):
                self.__last_thread.join()
            #monitors.remove(self)
            #log_message(self.monitor_name+ ' exiting thread successfully')
    def __del__(self):
        self.join()
   # def __exit__(self):
    #    self.join()