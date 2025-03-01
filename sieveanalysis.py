import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Define standard sieve sets (Sieve No. : Size in mm)
SIEVE_SETS = {
    "ASTM": {
        3: 6.730, 4: 4.760, 5: 4.000, 6: 3.360, 7: 2.830, 8: 2.380, 10: 2.000, 12: 1.680,
        14: 1.410, 16: 1.190, 18: 1.000, 20: 0.841, 25: 0.707, 30: 0.595, 35: 0.500, 40: 0.400,
        45: 0.354, 50: 0.297, 60: 0.250, 70: 0.210, 80: 0.177, 100: 0.149, 120: 0.125, 140: 0.105,
        170: 0.088, 200: 0.074, 230: 0.063, 270: 0.053, 325: 0.044, 400: 0.037
    },
    "ISO": {
        4: 4.75, 5: 4.00, 6: 3.35, 7: 2.80, 8: 2.36, 10: 2.00, 12: 1.70, 14: 1.18,
        16: 1.18, 18: 1.00, 20: 0.85, 25: 0.71, 30: 0.60, 35: 0.50, 40: 0.425, 45: 0.355,
        50: 0.300, 60: 0.250, 70: 0.212, 80: 0.180, 100: 0.150, 120: 0.125, 140: 0.106,
        200: 0.075, 270: 0.053, 400: 0.038
    },
    "Tyler": {
        3: 6.680, 4: 4.699, 5: 3.968, 6: 3.327, 7: 2.794, 8: 2.362, 10: 1.651, 12: 1.168,
        14: 0.833, 16: 0.589, 20: 0.417, 28: 0.295, 35: 0.208, 48: 0.147, 65: 0.104, 100: 0.074,
        150: 0.050, 200: 0.037, 270: 0.025
    }
}

# Prompt user to select a sieve standard
print("\nAvailable Sieve Standards: ASTM, ISO, Tyler")
standard_choice = input("Enter the sieve standard you are using: ").strip().upper()

# Validate choice
if standard_choice not in SIEVE_SETS:
    print("Invalid choice! Please restart and select a valid sieve standard.")
    exit()

# Use the selected sieve set
SIEVES = SIEVE_SETS[standard_choice]

# Display available sieve numbers and sizes
print(f"\nAvailable sieve numbers and sizes for {standard_choice}:")
for sieve_no, size in sorted(SIEVES.items()):
    print(f"Sieve No. {sieve_no}: {size} mm")

# Get total mass
total_mass = float(input("\nEnter total mass of sample used for sieve analysis (in grams): "))

# Get sieve numbers from user
sieve_numbers = list(map(int, input("\nEnter sieve numbers used (from large to small, separated by spaces): ").split()))

# Validate sieve numbers
if not all(s in SIEVES for s in sieve_numbers):
    print("Error: One or more sieve numbers are invalid. Restart and use only displayed sieve numbers.")
    exit()

# Get weight retained on each sieve
weights_retained = []
for sieve in sieve_numbers:
    weight = float(input(f"Enter weight retained on sieve {sieve} (in grams): "))
    weights_retained.append(weight)

# Check mass balance
if abs(sum(weights_retained) - total_mass) > 0.1:
    print("Error: Sum of weights does not match total mass. Please re-enter values.")
    exit()

# Compute cumulative weight retained
cumulative_weights = np.cumsum(weights_retained)

# Convert sieve numbers to sizes
sieve_sizes = [SIEVES[sieve] for sieve in sieve_numbers]

# Plot mass distribution
plt.figure(figsize=(10, 5))
plt.bar(sieve_sizes, weights_retained, width=0.1, alpha=0.7, color='blue', label="Mass Distribution")
plt.xlabel("Particle Size (mm)")
plt.ylabel("Mass Retained (g)")
plt.title(f"Mass Distribution Over Particle Size ({standard_choice} Sieves)")
plt.xscale("log")
plt.legend()
plt.show()

# Plot cumulative distribution
plt.figure(figsize=(10, 5))
plt.plot(sieve_sizes, cumulative_weights, marker="o", linestyle="--", color="red", label="Cumulative Mass")
plt.xlabel("Particle Size (mm)")
plt.ylabel("Cumulative Mass Retained (g)")
plt.title(f"Cumulative Mass Distribution ({standard_choice} Sieves)")
plt.xscale("log")
plt.legend()
plt.show()

# Compute mean and median particle size
mean_size = np.average(sieve_sizes, weights=weights_retained)
median_size = np.median(np.repeat(sieve_sizes, weights_retained))

print(f"\nMean Particle Size: {mean_size:.3f} mm")
print(f"Median Particle Size: {median_size:.3f} mm")

# Normality analysis using QQ plot
norm_data = np.repeat(sieve_sizes, weights_retained)  # Expand dataset based on mass
stats.probplot(norm_data, dist="norm", plot=plt)
plt.title(f"QQ Plot of Particle Size Distribution ({standard_choice} Sieves)")
plt.show()

# Skewness analysis
skewness = stats.skew(norm_data)

if abs(skewness) < 0.5:
    normality_statement = "The data follows a nearly normal distribution."
elif skewness > 0.5:
    normality_statement = f"The data is right-skewed with skewness of {skewness:.2f}."
else:
    normality_statement = f"The data is left-skewed with skewness of {skewness:.2f}."

# Engineering Interpretation
if skewness > 0.5:
    eng_statement = "This suggests a presence of larger particles dominating the distribution."
elif skewness < -0.5:
    eng_statement = "This suggests finer particles dominate, indicating possible over-grinding."
else:
    eng_statement = "The distribution is balanced, with an even spread of particle sizes."

print(f"\nQQ Plot Analysis: {normality_statement}")
print(f"Engineering Conclusion: {eng_statement}")
