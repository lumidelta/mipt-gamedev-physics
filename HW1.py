#%%
import sys
import math
import matplotlib
import random
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        self.len = 0.1
        self.dt = 0.01
        self.g = 9.8
        self.k = 500
        # self.xdata = [0.5, 0.75, 0.5, 0.25, 0.5, 0.75, 0.5, 0.25, 0.5]
        # self.ydata = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        # self.vxdata = [0 for i in range(10, 0, -1)]
        # self.vydata = [0 for i in range(10, 0, -1)]
        self.xdata = [random.randint(1, 10) * 0.1  for i in range(10, 0, -1)]
        self.ydata = [i * 0.1 for i in range(10, 0, -1)]
        self.vxdata = [0 for i in range(10, 0, -1)]
        self.vydata = [0 for i in range(10, 0, -1)]
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        prev_angle = 0
        prev_len_diff = 0
        nextx = self.xdata
        nexty = self.ydata
        for i in range(len(self.xdata) - 1, 0, -1):
            if self.ydata[i - 1] == self.ydata[i]:
                next_angle = 0
            else:
                next_angle = math.atan2((self.xdata[i - 1] - self.xdata[i]), (self.ydata[i - 1] - self.ydata[i]))
            next_len_diff = math.sqrt((self.ydata[i - 1] - self.ydata[i]) ** 2 + (self.xdata[i - 1] - self.xdata[i]) ** 2) - self.len
            dvx = self.dt * (-prev_len_diff * math.sin(prev_angle) + next_len_diff * math.sin(next_angle)) 
            dvy = self.dt * (-prev_len_diff * math.cos(prev_angle) + next_len_diff * math.cos(next_angle) - self.g/self.k)
            self.xdata[i] += (self.vxdata[i] + dvx/2) * self.dt
            self.ydata[i] += (self.vydata[i] + dvy/2) * self.dt
            self.vxdata[i] += dvx
            self.vydata[i] += dvy
            prev_angle = next_angle
            prev_len_diff = next_len_diff
        self.xdata = nextx
        self.ydata = nexty

        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
# %%
