#!/usr/bin/env python
"""
Project: ML pipeline for Shot-Term Rental Prices in NYC
Author: vnk8071
Date: 2023-08-20
"""

import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop the duplicates
    logger.info("Dropping duplicates")
    df = df.drop_duplicates().reset_index(drop=True)

    # Drop outliers
    logger.info("Dropping outliers")
    logger.info(f"Number of rows before dropping outliers: {df.shape[0]}")
    idx_price = df['price'].between(args.min_price, args.max_price)
    df = df[idx_price].reset_index(drop=True)
    idx = df['longitude'].between(-74.25, -
                                  73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    logger.info(f"Number of rows after dropping outliers: {df.shape[0]}")

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Save the dataframe to a csv file and log it as an artifact
    logger.info("Saving cleaned dataframe to csv")
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)

    logger.info("Logging artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This steps cleans the data")
    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Clone of the raw data artifact in Weights & Biases",
        required=True
    )
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of the output artifact",
        required=True
    )
    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of the output artifact",
        required=True
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )
    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price of the cars in the NYC dataset",
        required=True
    )
    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price of the cars in the NYC dataset",
        required=True
    )
    args = parser.parse_args()
    go(args)
