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

def addLines(xxdata, xydata):
    alpha = 0.05
    n = 49
    xdata = [xxdata[0]]
    ydata = [xydata[0]]
    for i in range(1, len(xxdata)):
        dx = xxdata[i] - xxdata[i-1]
        dy = xydata[i] - xydata[i-1]
        angle = math.atan2(dy, dx)
        for j in range(1, n):
            xdata.append(xxdata[i-1] + j * dx/n + alpha * math.sin(angle) if j % 2 == 0 else xxdata[i-1] + j * dx/n - alpha * math.sin(angle))
            ydata.append(xydata[i-1] + j * dy/n - alpha * math.cos(angle) if j % 2 == 0 else xydata[i-1] + j * dy/n + alpha * math.cos(angle))
        xdata.append(xxdata[i])
        ydata.append(xydata[i])
    return [xdata, ydata]

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        self.len = 0.1
        self.dt = 0.1
        self.g = 9.8
        self.k = 500
        self.xdata = []
        self.ydata = []
        self.xxdata = [0.5 for i in range(10, 1, -1)]
        self.xydata = [i * 0.1 for i in range(10, 1, -1)]
        self.vxdata = [0 for i in range(100, 0, -1)]
        self.vydata = [0 for i in range(100, 0, -1)]
        # self.xxdata = [random.randint(1, 10) * 0.1  for i in range(10, 0, -1)]
        # self.xydata = [i * 0.1 for i in range(10, 0, -1)]
        # self.vxdata = [0 for i in range(10, 0, -1)]
        # self.vydata = [0 for i in range(10, 0, -1)]
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
        nextx = self.xxdata
        nexty = self.xydata
        for i in range(len(self.xxdata) - 1, 0, -1):
            next_angle = math.atan2((self.xydata[i - 1] - self.xydata[i]), (self.xxdata[i - 1] - self.xxdata[i]))
            next_len_diff = math.sqrt((self.xydata[i - 1] - self.xydata[i]) ** 2 + (self.xxdata[i - 1] - self.xxdata[i]) ** 2) - self.len
            dvx = self.dt * (-prev_len_diff * math.cos(prev_angle) + next_len_diff * math.cos(next_angle)) 
            dvy = self.dt * (-prev_len_diff * math.sin(prev_angle) + next_len_diff * math.sin(next_angle) - self.g/self.k)
            self.xxdata[i] += (self.vxdata[i] + dvx/2) * self.dt
            self.xydata[i] += (self.vydata[i] + dvy/2) * self.dt
            self.vxdata[i] += dvx
            self.vydata[i] += dvy
            prev_angle = next_angle
            prev_len_diff = next_len_diff
        self.xxdata = nextx
        self.xydata = nexty
        self.xdata, self.ydata = addLines(self.xxdata, self.xydata)

        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r', scalex=False)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
# %%
