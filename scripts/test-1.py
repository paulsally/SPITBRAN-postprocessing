import matplotlib.pyplot as plt

a_x = [1, 3, 5, 7, 9, 11]
a_y = [2, 8, 2, 7, 9, 12]

b_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
b_y = [4, 6, 8, 9, 3, 1, 8, 5, 2, 9, 4]

# b_y = [2, 8, 2, 7, 9]
# b_x = [1, 2, 3, 4, 5]

# Plot the temperature curves
plt.figure(figsize=(10, 6))
plt.plot(a_x, a_y, marker='o', linestyle='solid', color='b', label="CMEMS SST")
plt.plot(b_x, b_y, marker='x', linestyle='dashed', color='g', label="MITgcm-BFM")
# plt.plot(m_dates, m_temperatures_d, marker='+', linestyle='dotted', color='r', label="MITgcm-BFM - Daily Avg")

# Add title, labels, and grid
plt.title(f"Temperature Curve (Thetao) for the Month")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)

# Add legend
plt.legend(loc="upper right", bbox_to_anchor=(1, 1))

# Rotate the date labels for better readability
plt.xticks(rotation=45)

# Tight layout to avoid clipping of legend
plt.tight_layout()

# Show the plot
plt.show()