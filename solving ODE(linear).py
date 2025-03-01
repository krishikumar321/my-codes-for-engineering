import numpy as np
import matplotlib.pyplot as plt
import cmath  # For complex numbers

# Function to define the ODE dy/dx = f(x, y)
def f(x, y):
    try:
        return eval(func, {"x": x, "y": y, "np": np, "cmath": cmath})
    except Exception as e:
        print(f"Error in function evaluation: {e}")
        exit()

# Euler's Method
def euler_method(f, x0, y0, h, n):
    x_vals, y_vals = [x0], [y0]
    for _ in range(n):
        y0 += h * f(x0, y0)
        x0 += h
        x_vals.append(x0)
        y_vals.append(y0)
    return x_vals, y_vals

# Improved Euler (Heun's Method)
def heun_method(f, x0, y0, h, n):
    x_vals, y_vals = [x0], [y0]
    for _ in range(n):
        y_pred = y0 + h * f(x0, y0)
        y_corr = y0 + (h / 2) * (f(x0, y0) + f(x0 + h, y_pred))
        x0 += h
        y0 = y_corr
        x_vals.append(x0)
        y_vals.append(y0)
    return x_vals, y_vals

# Runge-Kutta 4th Order (RK4)
def runge_kutta_4(f, x0, y0, h, n):
    x_vals, y_vals = [x0], [y0]
    for _ in range(n):
        k1 = h * f(x0, y0)
        k2 = h * f(x0 + h / 2, y0 + k1 / 2)
        k3 = h * f(x0 + h / 2, y0 + k2 / 2)
        k4 = h * f(x0 + h, y0 + k3)
        y0 += (k1 + 2*k2 + 2*k3 + k4) / 6
        x0 += h
        x_vals.append(x0)
        y_vals.append(y0)
    return x_vals, y_vals

# User Input with Validation
print("\n🔹 Numerical Solution of First-Order Differential Equations 🔹\n")
print("👉 Enter the function dy/dx = f(x, y) using valid Python syntax.")
print("👉 Available functions: exp(x), log(x), log10(x), sin(x), cos(x), tan(x), sinh(x), cosh(x), complex(a, b)")

while True:
    try:
        func = input("Enter the function f(x, y): ").strip()
        test_eval = eval(func, {"x": 1, "y": 1, "np": np, "cmath": cmath})  # Test function
        break
    except Exception as e:
        print(f"Invalid function! Please re-enter. Error: {e}")

x0 = float(input("Enter initial x (x0): "))
y0 = complex(input("Enter initial y (y0), supports complex (e.g., 1+2j): "))
x_end = float(input("Enter final x value: "))
h = float(input("Enter step size (h): "))

n = int((x_end - x0) / h)  # Number of steps

# Choose a method
print("\nAvailable Methods:")
print("1 - Euler's Method")
print("2 - Improved Euler (Heun's Method)")
print("3 - Runge-Kutta 4th Order (RK4)")

while True:
    try:
        method = int(input("Choose a method (1, 2, or 3): "))
        if method in [1, 2, 3]:
            break
        else:
            print("Invalid choice! Enter 1, 2, or 3.")
    except ValueError:
        print("Invalid input! Enter a number (1, 2, or 3).")

# Solve using chosen method
if method == 1:
    x_vals, y_vals = euler_method(f, x0, y0, h, n)
    method_name = "Euler's Method"
elif method == 2:
    x_vals, y_vals = heun_method(f, x0, y0, h, n)
    method_name = "Improved Euler (Heun's Method)"
elif method == 3:
    x_vals, y_vals = runge_kutta_4(f, x0, y0, h, n)
    method_name = "Runge-Kutta 4th Order (RK4)"

# Plot the results (only for real values)
plt.figure(figsize=(8, 5))
plt.plot(x_vals, [y.real for y in y_vals], 'bo-', label=method_name)
plt.xlabel("x")
plt.ylabel("y (Real part)")
plt.title(f"Solution using {method_name}")
plt.legend()
plt.grid()
plt.show()

# Print results
print("\n🔹 Computed values:")
for i in range(len(x_vals)):
    print(f"x = {x_vals[i]:.4f}, y = {y_vals[i]}")

print("\n📢 Complex solutions are also supported! The graph shows only real values.")

