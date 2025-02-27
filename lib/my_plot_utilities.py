def plot_map_minmax_nocb (
    p_ds_ax,
    p_ds_name,
    p_ds_var,
    p_target_var,
    p_lon, p_lat,
    p_ds_var_min, p_ds_var_max
):
    """
    Creates a map figure.
        
    Parameters
    ----------
    p_ds_ax :                       ax
                                    An ax for the figure as returned by plt.subplots.
    p_ds_name :                     str
                                    Title for the plot (usually containing the name of the dataset being plotted).
    p_ds_var :                      MaskedArray
                                    The values of the variable to plot the map of as extracted from the NetCDF dataset.
    p_target_var :                  str
                                    The target variable as requested in input.
    p_lon, p_lat :                  MaskedArray
                                    The values of the longitude and latitude to plot the map of as extracted from the NetCDF dataset.
    p_ds_var_min, p_ds_var_max :    int or float
                                    Min and Max values of target variable to print the colorbar range (set in config file).

    Returns
    -------
    mesh                            QuadMesh
                                    The image to be shown/saved.
    """
    mesh = p_ds_ax.pcolormesh(
        p_lon, 
        p_lat, 
        p_ds_var, 
        cmap="coolwarm", 
        vmin=p_ds_var_min, vmax=p_ds_var_max
    )
    p_ds_ax.set_title(f"{p_target_var} {p_ds_name}")
    p_ds_ax.set_xlabel("Longitude")
    p_ds_ax.set_ylabel("Latitude")

    return mesh


def on_pick(event, lines, legend, fig):
    """
    Handles the pick event to toggle line visibility.

    Parameters
    ----------
    event :                     event
                                The pick event triggered by clicking on a legend item.
    lines :                     list
                                List of Line2D objects plotted on the axes.
    legend :                    Legend
                                The legend object where the click occurs.
    fig :                       Figure
                                The figure object to redraw after visibility changes.
    """
    legend_item = event.artist
    for line, legend_line in zip(lines, legend.get_lines()):
        if legend_line == legend_item:
            visible = not line.get_visible()
            line.set_visible(visible)
            legend_item.set_alpha(1.0 if visible else 0.2)  # Dim the legend item if the line is hidden
            fig.canvas.draw_idle()
