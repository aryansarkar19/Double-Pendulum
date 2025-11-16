# Double pendulum simulation + animation (complete)
import numpy as np
from scipy.integrate import odeint
import sympy as sm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

# -----------------------------
# 1) Derive equations with sympy (unchanged approach)
# -----------------------------
t = sm.symbols('t')
m_1, m_2, g = sm.symbols('m_1 m_2 g', positive=True)

# define theta1(t), theta2(t)
th1_f, th2_f = sm.symbols(r'\theta_1 \theta_2', cls=sm.Function)
th1 = th1_f(t)
th2 = th2_f(t)

# coordinates (unit rod lengths assumed)
x1 = sm.sin(th1)
y1 = -sm.cos(th1)
x2 = x1 + sm.sin(th2)
y2 = y1 - sm.cos(th2)

# derivatives
th1_d = sm.diff(th1, t)
th2_d = sm.diff(th2, t)
th1_dd = sm.diff(th1_d, t)
th2_dd = sm.diff(th2_d, t)

x1_d = sm.diff(x1, t)
y1_d = sm.diff(y1, t)
x2_d = sm.diff(x2, t)
y2_d = sm.diff(y2, t)

# kinetic and potential energies (unit length rods)
T1 = sm.Rational(1,2) * m_1 * (x1_d**2 + y1_d**2)
T2 = sm.Rational(1,2) * m_2 * (x2_d**2 + y2_d**2)
V1 = m_1 * g * y1
V2 = m_2 * g * y2

L = T1 + T2 - (V1 + V2)

# Euler-Lagrange equations
LE1 = sm.diff(sm.diff(L, th1_d), t) - sm.diff(L, th1)
LE2 = sm.diff(sm.diff(L, th2_d), t) - sm.diff(L, th2)
LE1 = sm.simplify(LE1)
LE2 = sm.simplify(LE2)

# Solve symbolic for second derivatives th1_dd, th2_dd
sol = sm.solve([LE1, LE2], (th1_dd, th2_dd), dict=True)
if len(sol) == 0:
    raise RuntimeError("Sympy could not solve for accelerations symbolically.")
sol = sol[0]

# Create numeric functions for accelerations (lambdify)
LEF1 = sm.lambdify((th1, th2, th1_d, th2_d, m_1, m_2, g), sol[th1_dd], 'numpy')
LEF2 = sm.lambdify((th1, th2, th1_d, th2_d, m_1, m_2, g), sol[th2_dd], 'numpy')

# -----------------------------
# 2) Numerical integration parameters
# -----------------------------
# Initial conditions: [theta1, theta1_dot, theta2, theta2_dot]
initial_conditions = [np.pi/4, 0.0, np.pi/4, 0.0]   # tune as desired
m1_val = 1.0
m2_val = 1.0
g_val = 9.81

def system_of_odes(y, t, m_1, m_2, g):
    th1, th1_d, th2, th2_d = y
    th1_dd = LEF1(th1, th2, th1_d, th2_d, m_1, m_2, g)
    th2_dd = LEF2(th1, th2, th1_d, th2_d, m_1, m_2, g)
    return [th1_d, th1_dd, th2_d, th2_dd]

# Time array
T = 10.0
dt = 0.02
time_points = np.arange(0, T + dt, dt)

# Solve
soln = odeint(system_of_odes, initial_conditions, time_points, args=(m1_val, m2_val, g_val))
th1_sol = soln[:, 0]
th1_d_sol = soln[:, 1]
th2_sol = soln[:, 2]
th2_d_sol = soln[:, 3]

# Convert to Cartesian coordinates (rod length = 1)
L1 = 1.0
L2 = 1.0
x1_p = L1 * np.sin(th1_sol)
y1_p = -L1 * np.cos(th1_sol)
x2_p = x1_p + L2 * np.sin(th2_sol)
y2_p = y1_p - L2 * np.cos(th2_sol)

# -----------------------------
# 3) Animation setup
# -----------------------------
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
pad = 0.2
max_range = L1 + L2 + pad
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.grid(True)

# Line artists
line1, = ax.plot([], [], '-', lw=2, color='black')   # rod 1
line2, = ax.plot([], [], '-', lw=2, color='black')   # rod 2
mass1, = ax.plot([], [], 'o', ms=10, color='red')    # mass 1
mass2, = ax.plot([], [], 'o', ms=10, color='blue')   # mass 2

# Optional trails
trail_len = int(1.0 / dt)  # trail length ~ 1 second
trail1, = ax.plot([], [], '--', lw=1, color='orange', alpha=0.7)
trail2, = ax.plot([], [], '--', lw=1, color='purple', alpha=0.7)

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    mass1.set_data([], [])
    mass2.set_data([], [])
    trail1.set_data([], [])
    trail2.set_data([], [])
    time_text.set_text('')
    return line1, line2, mass1, mass2, trail1, trail2, time_text

def update(frame):
    # current positions
    x1c = x1_p[frame]; y1c = y1_p[frame]
    x2c = x2_p[frame]; y2c = y2_p[frame]

    # update rods and masses
    line1.set_data([0, x1c], [0, y1c])
    line2.set_data([x1c, x2c], [y1c, y2c])
    mass1.set_data([x1c], [y1c])
    mass2.set_data([x2c], [y2c])

    # update trails
    start = max(0, frame - trail_len)
    trail1.set_data(x1_p[start:frame+1], y1_p[start:frame+1])
    trail2.set_data(x2_p[start:frame+1], y2_p[start:frame+1])

    time_text.set_text(f't = {frame*dt:.2f} s')
    return line1, line2, mass1, mass2, trail1, trail2, time_text

# create animation
anim = FuncAnimation(fig, update, frames=len(time_points), init_func=init,
                     interval=dt*1000, blit=True)

plt.show()

# -----------------------------
# 4) Optional: save the animation
# -----------------------------
# To save as MP4 (requires ffmpeg installed):
# writer = FFMpegWriter(fps=int(1/dt))
# anim.save('double_pendulum.mp4', writer=writer, dpi=200)
#
# Or save as GIF (slower):
# writer = PillowWriter(fps=int(1/dt))
# anim.save('double_pendulum.gif', writer=writer)
