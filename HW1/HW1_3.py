import sympy as sp
N = 3
m = 0.1
g = 9.8
k = 5.0
l = 1.0
# x0 = [0]
# y0 = [10]
# for i in range(1, N):
#     y0.append(y0[i-1] - l - (N - i + 1) * m * g / k)
#     x0.append(0)


x1 = (sp.Function('x1'))
t = sp.symbols('t')
eq = sp.Eq(- k * (x1(t)**3)/(l**2), m * x1(t).diff(t, t))
sp.dsolve(eq, ics ={x1(0): 0.1, sp.diff(x1(t), t).subs(t,0): 0})
a = 1
