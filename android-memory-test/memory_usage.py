from adb import ADB
from config import Path
from config import CSV
import os

class MemoryUsage:
    
    def __init__(self, dev_id):
        self.dev_id = dev_id
    
    def collect_memory_snapshot(self, pid="sys"):
        """
        Collecting memory snapshot into csv files
        :pid: process or package, by default getting snapshot from system
        """

        meminfo = self._get_sys_meminfo() if pid == "sys" else self._get_ps_meminfo(pid)
        headers_row = [i for i in meminfo.keys()]
        values_row = [i for i in meminfo.values()]
        path = Path.sys() if pid == "sys" else Path.pid(pid)
        
        if os.path.isfile(path):
            CSV.append_row(path, values_row)
        else:
            CSV.append_row(path, headers_row)
            CSV.append_row(path, values_row)  

    def _get_sys_meminfo(self) -> dict:
        sys_meminfo = {}
        raw_sys_meminfo = ADB.get_meminfo(self.dev_id)
        for line in raw_sys_meminfo:
            if "Free RAM:" in line:
                sys_meminfo["Free RAM"] = line.split()[2]
            elif "Used RAM:" in line:
                sys_meminfo["Used RAM"] = line.split()[2]
        return sys_meminfo

    # TODO: Check for process not found
    def _get_ps_meminfo(self, ps) -> dict:
        meminfo = {}
        raw_meminfo = ADB.get_meminfo(self.dev_id, ps)
        for line in raw_meminfo:
            if "Java Heap:" in line:
                meminfo["Java Heap"] = line.split()[2]
            elif "Native Heap:" in line:
                meminfo["Native Heap"] = line.split()[2]
            elif "Code:" in line:
                meminfo["Code"] = line.split()[1]
            elif "Stack:" in line:
                meminfo["Stack"] = line.split()[1]
            elif "Graphics:" in line:
                meminfo["Graphics"] = line.split()[1]
            elif "Private Other:" in line:
                meminfo["Private Other"] = line.split()[2]
            elif "System:" in line:
                meminfo["System"] = line.split()[1]
            elif "TOTAL:" in line:
                meminfo["Total"] = line.split()[1]
        return meminfo


