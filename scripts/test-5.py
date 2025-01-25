import matplotlib
matplotlib.use('webAgg')

from matplotlib import pyplot as plt
from matplotlib.backends.backend_webagg import new_figure_manager, show

# Start the WebAgg server only once
manager = new_figure_manager(11, (10, 6))  # Reuse figure ID 1
fig = manager.canvas.figure

# Function to update the figure
def update_plot():
    fig.clf()  # Clear existing content
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3], [4, 5, 6], label="Updated Data")
    ax.set_title("Updated Plot")
    ax.legend()
    manager.canvas.draw()

# Initial plot
update_plot()

# Keep the server alive
show()
