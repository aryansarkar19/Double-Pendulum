# Double-Pendulum
The double pendulum is a classic physical system consisting of two masses (pendulums) attached by rigid rods, where one mass is suspended from the other. Due to the interaction between the two masses, the system exhibits complex, non-linear, and chaotic motion, which is highly sensitive to initial conditions.
The motion of the double pendulum is described using the Lagrangian formulation of mechanics. The Lagrangian, denoted as L, is the difference between the system's kinetic energy (T) and potential energy (V):
L\ =\ T\ -\ V\ 

                                                        
n the chosen coordinate system, 𝑥 and 𝑦 are expressed as follows:
x_1=l_1\cos{\left(\theta_1\right)}
x_2=l_2\sin{\left(\theta_1\right)}
The kinetic energy of the system accounts for both masses moving with their respective velocities. The velocities are related to the angular velocities of the two pendulums, as well as their positions.
T_1=\frac{1}{2}m_1\left(\dot{{x_1}^2}+\dot{{y_1}^2}\right)

T_2=\frac{1}{2}m_2\left(\dot{{x_2}^2}+\dot{{y_2}^2}\right)

Where:  
 \dot{x_1}=l_1\dot{\theta_1}\cos{\left(\theta_1\right)}       \ \dot{x_2}=\dot{x_1}+l_2\dot{\theta_2}\cos{\left(\theta_2\right)}  
\ \dot{y_1}=l_1\dot{\theta_1}\sin{\left(\theta_1\right)}                  \dot{y_2}=\dot{y_1}+l_2\dot{\theta_2}\sin{\left(\theta_2\right)}

 
Thus, the total kinetic energy of the system is:
T=T_1+T_2


Potential Energy of the system due to gravitational forces acting on both masses, which depends on their vertical positions, V_{1\ }&\ V_2 are the potential energies of the first mass(m_1) & the second mass(m_2), V_{1\ }determined by its height above a reference level, which is proportional to the cosine of the angle  \theta

V_1=-m_1gl_1\cos{\left(\theta_1\right)}

& V_2 depends on both angle of the second pendulum and the position of the first pendulum
V_2=-m_2g\left(l_1\cos{\left(\theta_1\right)}+l_2\cos{\left(\theta_2\right)}\right)

Thus, the total potential energy of the system is:
V=V_1+V_2

 Lagrange's Equations of Motion

\frac{d}{dt}\left(\frac{\partial L}{\partial\dot{\theta_1}}\right)-\frac{\partial L}{\partial\theta_1}=0

\frac{d}{dt}\left(\frac{\partial L}{\partial\dot{\theta_2}}\right)-\frac{\partial L}{\partial\theta_2}=0

These equations result in two second-order differential equations that describe the angular accelerations d²θ₁/dt² and d²θ₂/dt² for the two pendulums.

Numerical Simulation
The equations of motion are solved numerically using the scipy.integrate.solve_ivp function to integrate the system of ordinary differential equations. Initial conditions such as the angles and angular velocities of the two pendulums can be adjusted to observe different behaviors.



Importing the essential Libraries
import numpy as np
from scipy.integrate import odeint
import sympy as sm

Defining Symbols and Variables Using sympy.symbols()
t = sm.symbols('t')

m_1, m_2, g = sm.symbols('m_1 m_2 g', positive=True)

the1, the2 = sm.symbols(r'\theta_1, \theta_2', cls=sm.Function) # sm.Function states that the position is a function

the1 = the1(t) # Specifying the variable
the2 = the2(t)

x1 = sm.sin(the1)
y1 = -sm.cos(the1)

x2 = x1 + sm.sin(the2)
y2 = y1 + -sm.cos(the2)

x1

Calculating the first and second derivative of \theta_i: \frac{d\theta_i}{dt} and \frac{d^2\theta_i}{dt^2}, As well as {v_x}_iand {v_y}_i(for Energies) using `sympy.diff()`

i = 1 -> for the 1^{st}mass.         i = 2 -> for the 2^{nd} mass

the1_d = sm.diff(the1, t) # Angular Velocity
the1_dd = sm.diff(the1_d, t) # Angular Acceleration

x1_d = sm.diff(x1, t)
y1_d = sm.diff(y1, t)

the2_d = sm.diff(the2, t) # Angular Velocity
the2_dd = sm.diff(the2_d, t) # Angular Acceleration

x2_d = sm.diff(x2, t)
y2_d = sm.diff(y2, t)

Defining Kinetic T and Potential Energies V and the Lagrangian L for the double pendulum for each mass.

                        T=\frac{1}{2}\ \ \left(\left(\frac{dx\left(t\right)}{dt}\right)^2+\left(\frac{dy\left(t\right)}{dt}\right)^2\right)
 V=m\ g\ y(t)
L = T –V
T_1 = 1/2 * m_1 * ((x1_d)**2+(y1_d)**2)
T_2 = 1/2 * m_2 * ((x2_d)**2+(y2_d)**2)

V_1 = m_1 * g * y1
V_2 = m_2 * g * y2

L = T_1 + T_2 - (V_2 + V_1)

We formulate Lagrange's Equation for a non-damped system, since we have two mass, we have two equations q=\{\theta_1,\theta_2\}:

\frac{d}{dt}\left(\frac{\partial L}{\partial\dot{\theta_1}}\right)-\frac{\partial L}{\partial\theta_1}=0
 

\frac{d}{dt}\left(\frac{\partial L}{\partial\dot{\theta_2}}\right)-\frac{\partial L}{\partial\theta_2}=0
 

LE1 = sm.diff(sm.diff(L, the1_d), t) - sm.diff(L, the1)
LE2 = sm.diff(sm.diff(L, the2_d), t) - sm.diff(L, the2)

# use .simplyfy() if necessary
LE1 = LE1.simplify()
LE2 = LE2.simplify()

solutions = sm.solve([LE1, LE2], the1_dd, the2_dd)
LEF1 = sm.lambdify((the1, the2, the1_d, the2_d, t, m_1, m_2, g), solutions[the1_dd])
LEF2 = sm.lambdify((the1, the2, the1_d, the2_d, t, m_1, m_2, g), solutions[the2_dd])

We solve our problem numerically using `odeint()` the provided function of `scipy.integrate`.
We are interessted in finding the angles and angular velocities of the two mass in form of a vector:

\vec{y}=\left(\theta_1,\dot{\theta_1},\theta_2,\dot{\theta_2}\right)

In numerical analysis, the Runge–Kutta are a family of implicit and explicit iterative methods, which include the Euler method, used in temporal discretization for the approximate solutions of simultaneous nonlinear equations.

\vec{y_{n+1}}=\vec{y_n}+\Delta t\left(y_n,t\right)
To make it simpler think of it as the Euler Method:

\vec{y_{n+1}}=\vec{y_n}+\Delta t\ \frac{d\vec{y}}{dt}

In other words, we have the following numerical scheme:

{\theta_1}_{i+1}={\theta_1}_i+\Delta t\ \frac{d\theta_1}{dt}
\dot{{\theta_1}_{i+1}}=\dot{{\theta_1}_i}+\Delta t\ \frac{d^2\theta_1}{dt^2}
{\theta_2}_{i+1}={\theta_2}_i+\Delta t\ \frac{d\theta_2}{dt}
\dot{{\theta_2}_{i+1}}=\dot{{\theta_2}_i}+\Delta t\ \frac{d^2\theta_2}{dt^2}
In other words:
\vec{y_{i+1}}=\vec{y_i}+\Delta t\ \frac{d\vec{y}}{dt} 
