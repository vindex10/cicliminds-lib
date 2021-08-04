from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_median_idx(ax, dat, idx, scale=1):
    val = dat[idx].median(dim=["lon", "lat"])/scale
    is_yr = dat.frequency == "yr"
    time_scale = 60*60*24*1E9 * (365 if is_yr else 1)
    time_origin = np.datetime64(datetime.strptime(dat.time.time_origin, "%Y-%m-%d %H:%M:%S"))
    origin_year = (time_origin.astype('object').year if is_yr else 0)  # pylint: disable=no-member
    time_range = (dat.time.values - time_origin)/time_scale
    time = origin_year + time_range
    ax.plot(time, val)
    print(dat[idx].long_name)
    ax.set_title(idx)


def plot_spatial_idx_at_t(ax, dat, idx, t, scale=1):
    val = dat[idx].sel(time=t)/scale
    # mesh_lon, mesh_lat = np.meshgrid(val.lon, val.lat)
    # ax.contourf(mesh_lon, mesh_lat, val, transform=ccrs.PlateCarree())
    val.plot(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs={"shrink": 0.5})
    print(dat[idx].long_name)
    ax.set_title(f"time: {t}")


def plot_idx_value(dat, idx):
    ax = plt.axes(projection=ccrs.Robinson())
    ax.coastlines()
    ax.stock_img()
    ax.set_global()
    plot_spatial_idx_at_t(ax, dat, idx, t=dat.time.values[0], scale=np.timedelta64(1, 'D'))
    plt.show()
    plt.close()
