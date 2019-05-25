from adb import ADB

class MemoryUsage:
    
    def __init__(self, dev_id):
        self.dev_id = dev_id
    
    # TODO: Check for process not found
    def _get_ps_meminfo(self, ps) -> list:

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

if __name__ == "__main__":
    dev_id = ADB.get_connected_devices()[0]
    memory = MemoryUsage(dev_id)
    memory._get_ps_meminfo("28703")
