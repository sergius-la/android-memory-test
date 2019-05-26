import configparser
import csv
import os

class Config:
    
    @staticmethod
    def add_pid_csv(pid):
        Config._add_value("pids_csv", pid, os.path.join(Path.processing_dir(), "{}.csv".format(pid)))

    @staticmethod
    def generate(processing_dir):
        """
        Generate config.ini file
        """

        work_dir = os.getcwd()
        config = configparser.ConfigParser()
        config["Paths"] = { "home_dir" : work_dir,
                            "processing_dir" : os.path.join(work_dir, "reports", processing_dir)}
        config["pids_csv"] = { "sys" :  os.path.join(work_dir, "reports", processing_dir, "sys.csv")}
        with open("config.ini", "w") as configfile:
                config.write(configfile)
        
        processing_dir = Path.processing_dir()
        if not os.path.exists(processing_dir):
            os.makedirs(processing_dir)
        else:
            files = os.listdir(processing_dir)
            for f in files:
                os.remove(os.path.join(processing_dir, f))

    @staticmethod
    def _get_config():
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    @staticmethod
    def _add_value(section, option, value):
        """
        Add value into config.ini file
        """

        config = Config._get_config()
        config.set(section, option, value)
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    @staticmethod
    def get_section(section):
        """
        Get a section in dict
        """
        
        config = Config._get_config()
        return dict(config.items(section))
    
    @staticmethod
    def _get_value(key, value):
        """
        Method for getting value from config.ini file
        """

        config = Config._get_config()
        return config.get(key, value)

class Path:

    @staticmethod
    def pid(pid):
        return Config._get_value("pids_csv", str(pid))
    
    @staticmethod
    def sys():
        return Config._get_value("pids_csv", "sys")
    
    @staticmethod
    def processing_dir():
        return Config._get_value("Paths", "processing_dir")

class CSV:

    @staticmethod
    def append_row(path, row):
        with open(path, "a") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
    
    @staticmethod
    def get_csv_values(path, collumn) -> list:
        res = []
        with open(path, "r") as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                res.append(row[collumn])
        return res

if __name__ == "__main__":
    # Config.generate("test")
    # Config.add_pid_csv("28703")
    # print(Path.pid(247))
    # print(Path.processing_dir())
    x = CSV.get_csv_values(Path.sys(), 1)
    print(len(x))