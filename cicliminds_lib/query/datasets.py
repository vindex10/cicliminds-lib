from cicliminds_lib.utils import filter_pdarray
from cicliminds_lib.bindings.cdo import cdo_cat


def get_list_of_files(datasets, config, with_scenario=None):
    files = filter_pdarray(datasets, {
            "model": config["model"],
            "scenario": config["scenario"],
            "init_params": config["init_params"],
            "frequency": config["frequency"]
        })
    tmpfile = yield
    for fileinfo in files.itertuples():
        variable = fileinfo.variable
        res = fileinfo.Index
        if with_scenario is not None:
            scenario_file = _get_scenario(datasets, fileinfo, with_scenario)
            _add_scenario(tmpfile, scenario_file, fileinfo.Index)
            res = tmpfile
        tmpfile = yield res, variable


def _get_scenario(datasets, fileinfo, scenario):
    files = filter_pdarray(datasets, {
        "model": fileinfo.model,
        "scenario": scenario,
        "variable": fileinfo.variable,
        "init_params": fileinfo.init_params,
        "frequency": fileinfo.frequency
    })
    if files.shape[0] > 1:
        raise Exception("Duplicate ssp model")
    if files.shape[0] == 0:
        raise Exception("ssp model not found")
    return files.index.values[0]


def _add_scenario(output_file, scenario_file, input_file):
    cdo_cat(output_file, [input_file, scenario_file])
