import tempfile

from cicliminds_lib.utils import run_fs_cmd
from cicliminds_lib.utils import data_to_data


def remove_grid(fout_path, fin_path):
    with tempfile.NamedTemporaryFile("r") as f1:
        run_fs_cmd(f1.name, "ncks -O -C -x -v lat_bnds,lon_bnds", fin_path)
        run_fs_cmd(fout_path, "ncatted -O -a bounds,lat,d,, -a bounds,lon,d,,", f1.name)


remove_grid_from_data = data_to_data(remove_grid)


def cdo_fldmean(fout_path, fin_path):
    run_fs_cmd(fout_path, "cdo -O -L -fldmean", fin_path)


cdo_fldmean_from_data = data_to_data(cdo_fldmean)


def cdo_fldmin(fout_path, fin_path):
    run_fs_cmd(fout_path, "cdo -O -L -fldmin", fin_path)


cdo_fldmin_from_data = data_to_data(cdo_fldmin)


def cdo_fldmax(fout_path, fin_path):
    run_fs_cmd(fout_path, "cdo -O -L -fldmax", fin_path)


cdo_fldmax_from_data = data_to_data(cdo_fldmax)


def cdo_fldpctl(fout_path, fin_path, pctl):
    run_fs_cmd(fout_path, f"cdo -O -L -fldpctl,{pctl}", fin_path)


cdo_fldpctl_from_data = data_to_data(cdo_fldpctl)


def cdo_gridweights(fout_path, fin_path):
    run_fs_cmd(fout_path, "cdo -O -L gridweights", fin_path)


cdo_gridweights_from_data = data_to_data(cdo_gridweights, "cell_weights")


def cdo_cat(fout_path, fin_paths):
    run_fs_cmd(fout_path, "cdo -O -L cat", fin_paths)
