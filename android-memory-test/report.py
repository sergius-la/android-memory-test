from bs4 import BeautifulSoup
from config import Path
from graph import Graph
import os

class Report:
    
    def __init__(self):
        with open(Path.template_report()) as file:
            self.soup = BeautifulSoup(file, features="html.parser")

    def generate_report(self, name, pids):
        for pid in pids:
            self.soup.body.append(Report._add_process(pid))
        self._save_report(name)

    def _save_report(self, name):
        with open(os.path.join(Path.processing_dir(), "{}.html".format(name)), "w") as file:
            file.write(str(self.soup).replace("&lt;", "<").replace("&gt;", ">"))
    
    @staticmethod
    def _add_process(pid):
        with open(Path.template_process()) as file:
            soup = BeautifulSoup(file, features="html.parser")
        tag_graph = soup.find(id="graph")
        tag_graph.string = Graph.gen_pid_graph(pid)
        tag_meminfo = soup.find(id="meminfo")
        tag_meminfo.string = "<object height=100% width=100% type='text/plain' data=\"./{pid}.txt\"></object>".format(pid=pid)
        return soup

if __name__ == "__main__":
   x = Report(5084)
   x.save_report("test")
