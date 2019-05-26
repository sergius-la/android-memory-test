from config import Config
from adb import ADB
from datetime import date
from memory_usage import MemoryUsage

class Runner:

    def __init__(self, dev_id, *packages):
        self.dev_id = dev_id
        self.packages = packages
        Config.generate(str(date.today()))
        self.memory_usage = MemoryUsage(dev_id)
    
    def _get_pids(self):
        pids = ["sys"]
        for i in self.packages:
            pid = ADB.get_pid(self.dev_id, i)
            Config.add_pid_csv(pid)
            pids.append(pid)
        return pids

    def data_collector(self, iterations):
        pids = self._get_pids()
        for i in range(iterations):
            self.test_actions()
            for pid in pids:
                self.memory_usage.collect_memory_snapshot(pid)
    
    def test_actions(self):
        pass

if __name__ == "__main__":
    dev_id = ADB.get_connected_devices()[0]
    runner = Runner(dev_id, "com.android.settings", "com.android.vending")
    runner.data_collector(10)
    # print(date.today())
