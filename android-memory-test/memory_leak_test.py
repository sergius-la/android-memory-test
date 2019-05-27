from config import Config
from config import Path
from adb import ADB
from datetime import date
from report import Report
from memory_usage import MemoryUsage

class Runner:

    def __init__(self, dev_id, *packages):
        self.dev_id = dev_id
        self.packages = packages
        Config.generate(str(date.today()))
        self.memory_usage = MemoryUsage(dev_id)
        self.report = Report()
    
    def _get_pids(self):
        pids = ["sys"]
        for i in self.packages:
            pid = ADB.get_pid(self.dev_id, i)
            Config.add_pid_csv(pid)
            pids.append(pid)
        return pids

    def data_collector(self, iterations):
        pids = self._get_pids()
        self.before_test()
        for i in range(1, iterations+1):
            print("Iteration #{i}".format(i=i))
            self.test_actions(i)
            for pid in pids:
                self.memory_usage.collect_memory_snapshot(pid)
        self.after_test(pids)

    def before_test(self):
        pass
    
    def test_actions(self, i):
        pass
        # ADB.swipe(self.dev_id, 370, 1200, 370, 160) 

    def after_test(self, pids):
        for pid in pids:
            if pid == "sys":
                pid = ""
            ADB.save_meminfo(self.dev_id, Path.processing_dir(), pid)
        self.report.generate_report("test", pids) # TODO: Change name input

if __name__ == "__main__":
    dev_id = ADB.get_connected_devices()[0]
    runner = Runner(dev_id, "com.google.android.youtube")
    runner.data_collector(100)
