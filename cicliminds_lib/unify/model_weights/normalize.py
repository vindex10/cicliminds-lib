import xarray as xr


def align_model_weights_with_dataarray(weights_df, dataset_variable):
    weights_df = weights_df.assign(model=weights_df.model + "_" + weights_df.init_param)
    res = dataset_variable.copy()*0
    dataset_models_with_weights = set(list(weights_df["model"].values)).intersection(list(res.model.values))
    weights_df = weights_df[weights_df["model"].isin(dataset_models_with_weights)]
    weights_xr = xr.DataArray(data=weights_df["weight"].values,
                              dims=["model"],
                              coords={"model": weights_df["model"].values},
                              name=res.name)
    _, augmented_weights = xr.broadcast(res.sel(model=weights_df["model"].values),
                                        weights_xr)
    res.loc[dict(model=weights_df["model"].values)] = augmented_weights
    return res


def density_model_weights(weights_xr):
    return weights_xr/weights_xr.sum(dim=["model"])
