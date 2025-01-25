# Debug the backend
import matplotlib
print(f"Current backend: {matplotlib.get_backend()}")  # Confirm the backend being used

# Set the backend
matplotlib.use('webAgg')  # Use 'Qt5Agg', 'nbAgg', or 'WebAgg' depending on your environment

import matplotlib.pyplot as plt  # Import after setting the backend

# Example datasets
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
x2 = [1, 2, 3, 4, 5]
y2 = [10, 8, 6, 4, 2]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the first dataset
line1, = ax.plot(x1, y1, label='Dataset 1', marker='o', linestyle='solid', color='b')

# Plot the second dataset
line2, = ax.plot(x2, y2, label='Dataset 2', marker='x', linestyle='dashed', color='g')

# Add title and labels
ax.set_title("Interactive Plot with Visibility Control")
ax.set_xlabel("X-Axis")
ax.set_ylabel("Y-Axis")
ax.grid(True)

# Add an interactive legend
legend = ax.legend(loc="upper right", title="Click to toggle visibility", fancybox=True)
lines = [line1, line2]

# Function to toggle visibility on legend click
def on_pick(event):
    legend_item = event.artist
    for line, legend_line in zip(lines, legend.get_lines()):
        if legend_line == legend_item:
            visible = not line.get_visible()
            line.set_visible(visible)
            legend_item.set_alpha(1.0 if visible else 0.2)  # Dim the legend item if the line is hidden
            fig.canvas.draw_idle()
            print(f"Line visibility toggled: {line.get_label()} -> {'Visible' if visible else 'Hidden'}")

# Enable picking on legend items
for legend_line in legend.get_lines():
    legend_line.set_picker(True)
    print(f"Legend item picker enabled: {legend_line.get_label()}")

# Connect the pick event to the toggle function
fig.canvas.mpl_connect('pick_event', on_pick)

# Debug: Check if the event connection works
print("Event connections established. Ready to show the plot.")

# Show the plot
plt.show()
