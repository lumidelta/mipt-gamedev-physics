import sympy as sp
import math
y0 = [10]
x0 = [0]
m = 0.1
g = 9.8
k = 5.0
l = 1.0

x1 = (sp.Function('x1'))
x2 = (sp.Function('x2'))
y1 = (sp.Function('y1'))
y2 = (sp.Function('y2'))
t = sp.symbols('t')

sqrt1 = ((x1(t) - x0[0])**2 + (y1(t) - y0[0])**2)**0.5
sqrt2 = ((x1(t) - x2(t))**2 + (y1(t) - y2(t))**2)**0.5
eq1x = sp.Eq(-k*(sqrt1 - l) * (x1(t) - x0[0])/sqrt1 -k * (sqrt1 - l) * (x2(t) - x1(t))/sqrt1, m * x1(t).diff(t, t))
eq2x = sp.Eq(-k * (sqrt1 - l) * (x1(t) - x2(t))/sqrt1, m * x2(t).diff(t, t))
eq1y = sp.Eq(-k*(sqrt1 - l) * (x1(t) - x0[0])/sqrt1 -k * (sqrt1 - l) * (x2(t) - x1(t))/sqrt1 - m * g, m * y1(t).diff(t, t))
eq2y = sp.Eq(-k * (sqrt1 - l) * (y1(t) - y2(t))/sqrt1 - m * g, m * y2(t).diff(t, t))
ics={y1(0): 9, x1(0): 0.1, y2(0):7, x2(0): 0, sp.diff(y1(t), t).subs(t,0): 0, sp.diff(y2(t), t).subs(t,0): 0, sp.diff(x1(t), t).subs(t,0): 0, sp.diff(x2(t), t).subs(t,0): 0}
sol = sp.solvers.ode.systems.dsolve_system([eq1x, eq2x, eq1y, eq2y], ics=ics)

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
