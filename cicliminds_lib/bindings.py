import tempfile

from cicliminds_lib.config import CFG
from cicliminds_lib.utils import run_fs_cmd
from cicliminds_lib.utils import data_to_data

FLOAT_MISSING_VALUE = -9.99999979021476795361e+33
CDO_EXECUTABLE = CFG.cdo_executable
NCWA_EXECUTABLE = "ncwa -4"


def remove_grid(fout_path, fin_path):
    with tempfile.NamedTemporaryFile("r") as f1:
        run_fs_cmd(f1.name, "ncks -O -C -x -v lat_bnds,lon_bnds", fin_path)
        run_fs_cmd(fout_path, "ncatted -O -a bounds,lat,d,, -a bounds,lon,d,,", f1.name)


remove_grid_from_data = data_to_data(remove_grid)


def cdo_fldmean(fout_path, fin_path):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L -fldmean", fin_path)


cdo_fldmean_from_data = data_to_data(cdo_fldmean)


def nco_fldmean(fout_path, fin_path, dims=None):
    dims_str = "" if not dims else "-a" + ",".join(dims)
    run_fs_cmd(fout_path, f"{NCWA_EXECUTABLE} -O {dims_str}", fin_path)


nco_fldmean_from_data = data_to_data(nco_fldmean)


def cdo_fldmin(fout_path, fin_path):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L -fldmin", fin_path)


cdo_fldmin_from_data = data_to_data(cdo_fldmin)


def cdo_fldmax(fout_path, fin_path):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L -fldmax", fin_path)


cdo_fldmax_from_data = data_to_data(cdo_fldmax)


def cdo_fldpctl(fout_path, fin_path, pctl):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L -fldpctl,{pctl}", fin_path)


cdo_fldpctl_from_data = data_to_data(cdo_fldpctl)


def cdo_gridweights(fout_path, fin_path):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L gridweights", fin_path)


cdo_gridweights_from_data = data_to_data(cdo_gridweights, "cell_weights")


def cdo_cat(fout_path, fin_paths):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L cat", fin_paths)


def cdo_remapcon(fout_path, fin_path, lon, lat):
    run_fs_cmd(fout_path, f"{CDO_EXECUTABLE} -O -L remapcon,r{lon}x{lat}", fin_path)


cdo_remapcon_from_data = data_to_data(cdo_remapcon)
