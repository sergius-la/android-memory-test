from bs4 import BeautifulSoup
from config import Path
from graph import Graph
import os

class Report:
    
    def __init__(self):
        with open(Path.template_report()) as file:
            self.soup = BeautifulSoup(file, features="html.parser")
            self.soup.body.append(Report._add_process())

    def save_report(self, name):
        with open(os.path.join(Path.processing_dir(), "{}.html".format(name)), "w") as file:
            file.write(str(self.soup).replace("&lt;", "<").replace("&gt;", ">")) 
    
    @staticmethod
    def _add_process(pid):
        with open(Path.template_process()) as file:
            soup = BeautifulSoup(file, features="html.parser")
        tag = soup.find(id="graph")
        tag.string = Graph.gen_pid_graph(pid)
        return soup

if __name__ == "__main__":
   x = Report()
   x.save_report("test")
