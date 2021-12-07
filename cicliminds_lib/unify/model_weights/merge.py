from functools import reduce
import pandas as pd


MODEL_WEIGHTS_COLUMNS = ["model", "init_param", "scenario", "weight"]
MODEL_WEIGHTS_ID_COLUMNS = MODEL_WEIGHTS_COLUMNS[:3]


def get_merged_model_weights(model_weights_reg, model_weight_names):
    if not model_weight_names:
        return None
    weight_dfs = get_weight_dfs(model_weights_reg, model_weight_names)
    stacked_weights = stack_model_weights(weight_dfs)
    merged_weights = merge_model_weights(stacked_weights)
    return merged_weights


def get_weight_dfs(model_weights_reg, model_weight_names):
    res = {}
    for name in model_weight_names:
        reg_row = model_weights_reg[model_weights_reg["name"] == name]
        filepath = reg_row.index.values[0]
        df = pd.read_csv(filepath, sep="\t", header=False, comment="#")
        df = df.iloc[:, 0:len(MODEL_WEIGHTS_COLUMNS)]
        df.columns = MODEL_WEIGHTS_COLUMNS
        res[name] = df
    return res


def stack_model_weights(weight_dfs):
    parts = []
    for name, df in weight_dfs.items():
        df = df.rename(columns={"weight": name})
        parts.append(df)
    return reduce(lambda left, right: left.merge(right, how="inner", on=MODEL_WEIGHTS_ID_COLUMNS), parts)


def merge_model_weights(df):
    weight_cols = [col for col in df.columns if col not in MODEL_WEIGHTS_ID_COLUMNS]
    prod_col = df[weight_cols].prod(axis=1)
    return df[MODEL_WEIGHTS_ID_COLUMNS].assign(weight=prod_col)
