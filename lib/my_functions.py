def plot_map_minmax_nocb (
    ds_ax,
    ds_name,
    ds_var,
    ds_lon_min, ds_lon_max,
    ds_lat_min, ds_lat_max,
    ds_sst_min, ds_sst_max
):
    """
    Creates a map figure.
        
    Parameters
    ----------
    ds_ax :                     ax
                                An ax for the figure as returned by plt.subplots.
    ds_name :                   tr
                                Name of the dataset e.g. CMEMS or MITgcm.
    ds_var :                    MaskedArray
                                The variable to plot the map of as extracted by the NetCDF dataset.
    ds_lon_min, ds_lon_max :    float
                                Min and Max values of longitude in the dataset.
    ds_lat_min, ds_lat_max :    float
                                Min and Max values of latitude in the dataset.
    ds_sst_min, ds_sst_max :    int or float
                                Min and Max values of temperature to print the colorbar range.

    Returns
    -------
    matplotlib.image.AxesImage
        The image to be shown/saved.
    """
    ds_im = ds_ax.imshow(
        ds_var, 
        extent=[
            ds_lon_min, ds_lon_max, 
            ds_lat_min, ds_lat_max
        ],
        origin='lower', 
        cmap='coolwarm', 
        vmin=ds_sst_min, 
        vmax=ds_sst_max
    ) 
    ds_ax.set_title(f"SST {ds_name}")
    ds_ax.set_xlabel("Longitude")
    ds_ax.set_ylabel("Latitude")

    return ds_im