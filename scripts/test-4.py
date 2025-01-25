import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])

# Save as an interactive HTML file
from matplotlib.backends.backend_webagg import new_figure_manager
new_figure_manager(1, (8, 6))
