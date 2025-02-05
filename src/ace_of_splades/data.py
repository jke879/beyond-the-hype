"""Provide functions for data imports and management."""

from pathlib import Path

import polars as pl


def get_movies_dataset(sample: int = 0, *, local: bool = False) -> pl.DataFrame:
    """Retrieve a dataset of movies with embeddings vectors.

    Args:
        sample: number of rows to sample from the dataset.
        local: whether to load the dataset from a local file or from the web.

    Returns:
        A dataset of movies with their plots.

    """
    file_name = "movies_plots_dataset_embd_minilm.parquet"
    if local:
        here = Path(__file__)
        source = here.parent.parent.parent / f"data/{file_name}"
    else:
        source = f"https://raw.githubusercontent.com/xtreamsrl/ace-of-splades/main/data/{file_name}"

    if sample:
        return pl.read_parquet(source).sample(sample)

    movies = pl.read_parquet(source).rename(
        {
            "Release Year": "release_year",
            "Title": "title",
            "Origin/Ethnicity": "origin",
            "Director": "director",
            "Cast": "cast",
            "Genre": "genre",
            "Wiki Page": "wiki_page",
            "Plot": "plot",
        },
    )

    return movies.with_columns(
        pl.col("cast").str.split(by=",").alias("cast"),
        pl.col("genre").str.split(by="/").alias("genre"),
    )
