import sympy as sp

y0 = [10, 9, 8]
m = 0.1
g = 9.8
k = 5.0
l = 1.0

y1 = (sp.Function('y1'))
y2 = (sp.Function('y2'))
t = sp.symbols('t')

dl1 = y0[0] - y1(t) - l
dl2 = y1(t) - y2(t) - l

eq = [sp.Eq( k * (dl1 - dl2) - m * g, m * y1(t).diff(t, t)), sp.Eq( k * dl2 - m * g, m * y2(t).diff(t, t))]
sol = sp.dsolve(eq, ics={y1(0): 9, y2(0):7, sp.diff(y1(t), t).subs(t,0): 0, sp.diff(y2(t), t).subs(t,0): 0})
sol_0t = sol[0].subs({k: 5.0, m:0.1, l:1.0, g:10.0}).rhs
sol_1t = sol[1].subs({k: 5.0, m:0.1, l:1.0, g:10.0}).rhs
a = 1
# sp.plot(sol_0t, (t, 0, 50))
# sp.plot(sol_1t, (t, 0, 50))

import math
def addLines(xxdata, xydata):
    alpha = 0.05
    n = 9
    xxdata = [sp.re(i) for i in xxdata]
    xydata = [sp.re(i) for i in xydata]
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

import sys
import matplotlib
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
        self.t = 0
        self.dt = 0.01
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
        t_result = [10, sol_0t.subs({t: self.t}), sol_1t.subs({t: self.t})]
        self.t += self.dt
        self.xdata, self.ydata = addLines([0, 0, 0], t_result)
        
        # Clear the canvas
        self.canvas.axes.cla()
        # Set axes size
        self.canvas.axes.set_xbound(-1, 1)
        self.canvas.axes.set_ybound(10, 5)
        # Draw
        self.canvas.axes.plot(self.xdata, self.ydata, 'r', scalex=False, scaley=False, )
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
