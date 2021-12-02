from cicliminds_lib.query.datasets import get_datasets_for_block
from cicliminds_lib.unify.merge import get_merged_dataset


def get_merged_dataset_by_query(datasets_reg, query):
    filtered_datasets_reg = get_datasets_for_block(datasets_reg, query)
    dataset = get_merged_dataset(filtered_datasets_reg, query["scenario"])
    return dataset
