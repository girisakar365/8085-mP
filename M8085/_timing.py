import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from json import load

class TimingDiagram:
    def __init__(self):
        self.colors = ['#FF0000', '#0000FF', '#0000FF', '#008000', '#008000', '#FFA500', '#FF00FF', '#FF00FF', '#A52A2A', '#00FFFF']

    def plot_full(self, instructions):
        with open('timegraph.json', 'r') as file:
            timing_instruction = load(file)
        decoded_timing = timing_instruction[list(instructions.split(' '))[0].upper()]
        plot_functions = {
            'opcode': self.__plot_opcodefetch,
            'read': self.__plot_read,
            'write': self.__plot_write,
            'io_read': self.__plot_io_read,
            'io_write': self.__plot_io_write
        }
        fig = plt.figure(figsize=(15, 8)) 
        dynamic_wratio = [6 if op =='opcode' else 4.5 for op in decoded_timing]
        gs = gridspec.GridSpec(1, len(decoded_timing), width_ratios=dynamic_wratio)
        for i, operation in enumerate(decoded_timing):
            if operation in plot_functions:
                plt.subplot(gs[i])
                plot_functions[operation]()
            else:
                print(f"Unknown operation: {operation}")
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.legend(instructions)
        plt.show()

    def __plot_table(self, column_label, row_label):
        cell_text = [['']* len(column_label) for _ in range(len(row_label))] 
        table = plt.table(cellText=cell_text, colLabels=column_label, rowLabels=row_label,
                          cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
        cellDict = table.get_celld()
        for i in range(len(row_label)):
            for j in range(len(column_label)):
                cellDict[(i + 1, j)].visible_edges = 'LR'

    def __plot_data(self, x_data, y_data, colors):
        for x, y, color in zip(x_data, y_data, colors):
            plt.plot(x, y, color=color)

    def __set_plot_limits(self, title, xlim, ylim):
        plt.title(title)
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.xticks([])
        plt.yticks([])

    def __plot_timing_diagram(self, title, column_label, row_label, x_data, y_data, xlim, ylim):
        self.__plot_table(column_label, row_label)
        self.__plot_data(x_data, y_data, self.colors)
        self.__set_plot_limits(title, xlim, ylim)

    def __plot_opcodefetch(self):
        title = 'Opcode Fetch'
        column_label = ['T1', 'T2', 'T3', 'T4']
        row_label = ['Clock', 'A₁₅-A₈', 'A₇-A₀', 'ALE', 'IO/M\'S₁S₀', 'RD\'', 'WR\'']
        x_data, y_data = self.__get_opcodefetch_data()
        x_lim , y_lim = [0, 6], [0,8]
        self.__plot_timing_diagram(title, column_label, row_label, x_data, y_data, x_lim, y_lim)

    def __plot_read(self):
        title = 'Read'
        column_label = ['T1', 'T2', 'T3']
        row_label = ['' for _ in range(8)]
        x_data, y_data = self.__get_read_data()
        x_lim , y_lim = [0, 4.5], [0,8]
        self.__plot_timing_diagram(title, column_label, row_label, x_data, y_data, x_lim, y_lim)
        
    def __plot_write(self):
        title = 'Write'
        column_label = ['T1', 'T2', 'T3']
        row_label = ['' for _ in range(8)]
        x_data, y_data = self.__get_write_data()
        x_lim , y_lim = [0, 4.5], [0,8]
        self.__plot_timing_diagram(title, column_label, row_label, x_data, y_data, x_lim, y_lim)

    def __plot_io_read(self):
        title = 'IO Read'
        column_label = ['T1', 'T2', 'T3']
        row_label = ['' for _ in range(8)]
        x_data, y_data = self.__get_io_read_data()
        x_lim , y_lim = [0, 4.5], [0,8]
        self.__plot_timing_diagram(title, column_label, row_label, x_data, y_data, x_lim, y_lim)
        
    def __plot_io_write(self):
        title = 'IO Write'
        column_label = ['T1', 'T2', 'T3']
        row_label = ['' for _ in range(8)]
        x_data, y_data = self.__get_io_write_data()
        x_lim , y_lim = [0, 4.5], [0,8]
        self.__plot_timing_diagram(title, column_label, row_label, x_data, y_data, x_lim, y_lim)

    def __get_opcodefetch_data(self):
        x_data = [
            np.array([0, 0.15, 0.75, 0.90, 1.5, 1.65, 2.25, 2.40, 3, 3.15, 3.75, 3.90, 4.5, 4.65, 5.25, 5.40, 6]),
            np.array([0, 0.15, 0.25, 4.65, 4.75, 6]),
            np.array([0, 0.15, 0.25, 4.65, 4.75, 6]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 6]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 6]),
            np.array([0, 0.15, 0.75, 0.90, 6]),
            np.array([0, 0.15, 0.25,  6]),
            np.array([0, 0.15, 0.25,  6]),
            np.array([0, 0.15,1.75,2.25,2.45, 3.65,3.85, 6]),
            np.array([0, 0.15,  6])
            ]   
        y_data = [
            np.array([6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8]),
            np.array([5.8, 5.8, 5.1, 5.1, 5.8, 5.8]),
            np.array([5.1, 5.1, 5.8, 5.8, 5.1, 5.1]),
            np.array([4.8, 4.8, 4.1, 4.1, 4.45, 4.45, 4.1, 4.1, 4.45, 4.45]),
            np.array([4.1, 4.1, 4.8, 4.8, 4.45, 4.45, 4.8, 4.8, 4.45, 4.45]),
            np.array([3.1, 3.8, 3.8, 3.1, 3.1]),
            np.array([2.8, 2.8, 2.1, 2.1]),
            np.array([2.1, 2.1, 2.8, 2.8]),
            np.array([1.1, 1.8, 1.8,1.8,1.1, 1.1,1.8, 1.8]),
            np.array([0.1, 0.8, 0.8])
        ]
        return x_data, y_data

    def __get_read_data(self):
        x_data = [
            np.array([0, 0.15, 0.75, 0.90, 1.5, 1.65, 2.25, 2.40, 3, 3.15, 3.75, 3.90, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.75, 0.90, 4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 1.75, 2.25, 2.45, 3.65, 3.85, 4.5]),
            np.array([0, 4.5])
            ]   
        y_data = [
            np.array([6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8]),
            np.array([5.8, 5.8, 5.1, 5.1]),
            np.array([5.1, 5.1, 5.8, 5.8]),
            np.array([4.45, 4.45, 4.1, 4.1, 4.45, 4.45, 4.1, 4.1, 4.45, 4.45]),
            np.array([4.45, 4.45, 4.8, 4.8, 4.45, 4.45, 4.8, 4.8, 4.45, 4.45]),
            np.array([3.1, 3.8, 3.8, 3.1, 3.1]),
            np.array([2.8, 2.8, 2.1, 2.1]),
            np.array([2.1, 2.1, 2.8, 2.8]),
            np.array([ 1.8, 1.8,1.8,1.1, 1.1,1.8, 1.8]),
            np.array([ 0.8, 0.8])
        ] 
        return x_data , y_data

    def __get_write_data(self):
        x_data = [
            np.array([0, 0.15, 0.75, 0.90, 1.5, 1.65, 2.25, 2.40, 3, 3.15, 3.75, 3.90, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.75, 0.90, 4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 4.5]),
            np.array([0, 1.75, 2.25, 2.45, 3.65, 3.85, 4.5])
            ]   
        y_data = [
            np.array([6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8]),
            np.array([5.8, 5.8, 5.1, 5.1]),
            np.array([5.1, 5.1, 5.8, 5.8]),
            np.array([4.45, 4.45, 4.1, 4.1, 4.45, 4.45, 4.1, 4.1, 4.45, 4.45]),
            np.array([4.45, 4.45, 4.8, 4.8, 4.45, 4.45, 4.8, 4.8, 4.45, 4.45]),
            np.array([3.1, 3.8, 3.8, 3.1, 3.1]),
            np.array([2.8, 2.8, 2.1, 2.1]),
            np.array([2.1, 2.1, 2.8, 2.8]),
            np.array([ 1.8, 1.8]),
            np.array([ 0.8, 0.8,0.8,0.1, 0.1,0.8, 0.8])
        ]
        return x_data, y_data

    def __get_io_read_data(self):
        x_data = [
            np.array([0, 0.15, 0.75, 0.90, 1.5, 1.65, 2.25, 2.40, 3, 3.15, 3.75, 3.90, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.75, 0.90, 4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 1.75, 2.25, 2.45, 3.65, 3.85, 4.5]),
            np.array([0, 4.5])
            ]   
        y_data = [
            np.array([6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8]),
            np.array([5.8, 5.8, 5.1, 5.1]),
            np.array([5.1, 5.1, 5.8, 5.8]),
            np.array([4.45, 4.45, 4.1, 4.1, 4.45, 4.45, 4.1, 4.1, 4.45, 4.45]),
            np.array([4.45, 4.45, 4.8, 4.8, 4.45, 4.45, 4.8, 4.8, 4.45, 4.45]),
            np.array([3.1, 3.8, 3.8, 3.1, 3.1]),
            np.array([2.8, 2.8, 2.1, 2.1]),
            np.array([2.1, 2.1, 2.8, 2.8]),
            np.array([ 1.8, 1.8,1.8,1.1, 1.1,1.8, 1.8]),
            np.array([ 0.8, 0.8])
        ]
        return x_data, y_data

    def __get_io_write_data(self):
        x_data = [
            np.array([0, 0.15, 0.75, 0.90, 1.5, 1.65, 2.25, 2.40, 3, 3.15, 3.75, 3.90, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.25, 1.65, 1.75,2.25, 2.35,3.75,3.85, 4.5]),
            np.array([0, 0.15, 0.75, 0.90, 4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 0.15, 0.25,  4.5]),
            np.array([0, 4.5]),
            np.array([0, 1.75, 2.25, 2.45, 3.65, 3.85, 4.5])
            ]   
        y_data = [
            np.array([6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8, 6.1, 6.1, 6.8, 6.8]),
            np.array([5.8, 5.8, 5.1, 5.1]),
            np.array([5.1, 5.1, 5.8, 5.8]),
            np.array([4.45, 4.45, 4.1, 4.1, 4.45, 4.45, 4.1, 4.1, 4.45, 4.45]),
            np.array([4.45, 4.45, 4.8, 4.8, 4.45, 4.45, 4.8, 4.8, 4.45, 4.45]),
            np.array([3.1, 3.8, 3.8, 3.1, 3.1]),
            np.array([2.8, 2.8, 2.1, 2.1]),
            np.array([2.1, 2.1, 2.8, 2.8]),
            np.array([ 1.8, 1.8]),
            np.array([ 0.8, 0.8,0.8,0.1, 0.1,0.8, 0.8])
        ] 
        return x_data, y_data