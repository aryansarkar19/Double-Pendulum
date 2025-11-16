# Double Pendulum Simulation

This repository contains a Python implementation of a **Double Pendulum Simulation**. The simulation numerically solves the coupled nonlinear differential equations governing the motion of a double pendulum and visualizes the resulting chaotic dynamics.

## 📌 Overview

The double pendulum is a classic example of a chaotic system. Small variations in the initial conditions can lead to drastically different trajectories. This project simulates the motion using **numerical integration (ODE solving)** and optionally provides animation support.

## 🧮 Features

* Numerical solution of the double pendulum differential equations
* Adjustable physical parameters
* Configurable initial conditions
* Real-time or saved animation of the motion
* Clear modular code structure

## 📁 File Structure

```
DoublePendulum.py      # Main simulation script
```

## 📦 Requirements

Make sure you have the following Python packages installed:

```
numpy
scipy
matplotlib
```

Install them using:

```
pip install numpy scipy matplotlib
```

## ▶️ How to Run

Run the simulation using:

```
python DoublePendulum.py
```

This will:

* Solve the system of differential equations
* Display a matplotlib animation showing the motion of the double pendulum

## ⚙️ How the Code Works

### 1. **Import Libraries**

The script uses:

* `numpy` for numerical operations
* `scipy.integrate.odeint` for solving ODEs
* `matplotlib` for visualization

### 2. **Define System Parameters**

* Masses: `m1`, `m2`
* Rod lengths: `L1`, `L2`
* Gravity: `g`

These parameters can be modified in the script.

### 3. **Define the Differential Equations**

The dynamics are computed using the Lagrange formalism. The system is expressed as four first‑order ODEs:

* θ₁ (angle of first pendulum)
* θ₂ (angle of second pendulum)
* ω₁ = dθ₁/dt
* ω₂ = dθ₂/dt

These equations are coded inside the `derivatives()` function.

### 4. **Solve Using ODEINT**

`odeint()` numerically integrates the system for a specified time interval.

### 5. **Animate the Results**

`matplotlib.animation` renders the pendulum motion.

## 📊 Output

* Animation window showing the pendulum motion
* Optionally, energy or trajectory plots (depending on the code provided)

## 🧩 Customization

You can change:

* `theta1`, `theta2` (initial angles)
* `omega1`, `omega2` (initial angular velocities)
* simulation time range
* physical constants

## 📝 License

This project is released for academic and learning purposes.

---

If you'd like, I can also:

* Generate a **GitHub‑ready README with screenshots and GIFs**
* Add equations using LaTeX
* Add more documentation like theory, derivations, and explanation
* Convert your script into a clean OOP version or Jupyter notebook.

