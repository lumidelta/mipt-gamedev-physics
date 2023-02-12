#%%
import sympy as sp
import sys
import math
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt
from numpy.linalg import eig
import numpy as np

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

def addLines(xxdata, xydata):
    alpha = 0.05
    n = 5
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

N = 3
m = 0.1
g = 9.8
k = 5.0
l = 1.0
x0 = [0]
y0 = [- l - N * m * g / k]
for i in range(1, N):
    y0.append(y0[i-1] - l - (N - i + 1) * m * g / k)
    x0.append(0)

Mx = [[0 for _ in range(N)] for _ in range(N)]
My = [[0 for _ in range(N)] for _ in range(N)]
for i in range(0, N):
    for j in range(0, N):
        if (j == i - 1):
            Mx[i][j] = k * (1 - l/abs(y0[i] - y0[i - 1]))
            My[i][j] = k
        elif (j == i):
            if i == 0:
                Mx[i][j] = -k * (1 - l/abs(y0[i] -         0)) - k * (1 - l/abs(y0[i] - y0[i + 1]))
                My[i][j] = -2 * k
            elif i != N-1:
                Mx[i][j] = -k * (1 - l/abs(y0[i] - y0[i - 1])) - k * (1 - l/abs(y0[i] - y0[i + 1]))
                My[i][j] = -2 * k
            else:
                Mx[i][j] = -k * (1 - l/abs(y0[i] - y0[i - 1]))
                My[i][j] = -k
        elif (j == i + 1):
            Mx[i][j] = k * (1 - l/abs(y0[i] - y0[i + 1]))
            My[i][j] = k
        else:
            Mx[i][j] = 0

M = [[0 for _ in range(4*N)] for _ in range(4*N)]
B = [[0 for _ in range(4*N)] for _ in range(4*N)]

for i in range(4*N):
    if (i < 2 * N):
        M[2 * N + i][i] = 1
    elif (i < 3 * N):
        for j in range(N):
            M[j][i] = Mx[j][i % N]
    else:
        for j in range(N):
            M[N + j][i] = Mx[j][i % N]
            B[N + j][i] = Mx[j][i % N]


# for i in range(N/2):
# Проверка наших уравнений
x = []
x0 = []
eqs = []
for i in range(N):
    x.append(sp.Function('vx' + str(i)))
    x0.append(0)
for i in range(N):
    x.append(sp.Function('vy' + str(i)))
    x0.append(0)
for i in range(N):
    x.append(sp.Function('x' + str(i)))
    x0.append(0)
for i in range(N):
    x.append(sp.Function('y' + str(i)))
    x0.append(y0[i])


t = sp.symbols('t')
xi = Matrix(x)
x0 = Matrix(x0)

for i in range(len(x)):
    Mi = Matrix(M[i])
    res = 0
    for j in range(len(x)):
        res = res + Mi[j] * x[j](t) + B[i][j] * x0[j]
    eqs.append(sp.Eq(x[i](t).diff(t), res))

# Initial conditions
y_ics = y0
ics = [0] * 4*N 
# Velocities and x's
for i in range(3*N):
    ics[i] = 0.0
# y's
for i in range(3*N, 4*N):
    ics[i] = y_ics[i-3*N]

ics_sympy = sp.Matrix(ics)

print(ics_sympy)
w, v = eig(M)
A = sp.Matrix(M)
V, _ = A.diagonalize()

Y = Matrix(len(w), len(w), lambda i,j: w[i] * t if i == j else 0)
exp_A = V * Y * V.inv()
result = (exp_A * ics_sympy).applyfunc(sp.simplify)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.t = 0
        self.dt = 0.1
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
        t_result = result.subs({t: self.t})
        print(t_result)
        self.t += self.dt
        self.xdata, self.ydata = addLines(t_result[2*N:3*N], t_result[3*N:4*N])
        
        # Clear the canvas
        self.canvas.axes.cla()
        # Set axes size
        self.canvas.axes.set_xbound(-1, 1)
        self.canvas.axes.set_ybound(0, -25)
        # Draw
        self.canvas.axes.plot(self.xdata, self.ydata, 'r', scalex=False, scaley=False, )
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()