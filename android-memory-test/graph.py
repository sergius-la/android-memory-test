import plotly.offline
import plotly.graph_objs as go
from config import CSV
from config import Path

class Graph:

    @staticmethod
    def _get_scatter_trace_values(pid, collumn):
        raw_csv = CSV.get_csv_values(Path.pid(pid), collumn)
        y = raw_csv[1::]
        x = [i for i in range(0, len(y))]
        title = raw_csv[0]
        return [title, x, y]
    
    @staticmethod
    def _get_scatter_trace(pid, collumn):
        vl = Graph._get_scatter_trace_values(pid, collumn)
        trace = go.Scatter(
            x = vl[1],
            y = vl[2],
            name = vl[0],
            mode = 'lines+markers'
        )
        return trace
    
    @staticmethod
    def _get_pid_data(pid):
        index = 7 if pid != "sys" else 2
        data = []
        for i in range(0, index):
            data.append(Graph._get_scatter_trace(pid, i))
        return data

    @staticmethod
    def gen_pid_graph(pid):
        """
        Method generate grapth of memory usage
        """

        title = "PID {}".format(pid) if pid != "sys" else "System"
        data = Graph._get_pid_data(pid)
        layout = go.Layout(
            title=title,
        )

        div = plotly.offline.plot(
            {"data": data, "layout": layout},
            include_plotlyjs=False, 
            output_type='div')
        return div


if __name__ == "__main__":
    x = Graph.gen_pid_graph(28703)
    print(x)