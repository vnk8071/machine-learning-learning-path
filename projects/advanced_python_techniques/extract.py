import csv
import json

from models import NearEarthObject, CloseApproach
from logger import get_logger


logger = get_logger(__name__)


def load_neos(neo_csv_path: str):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path) as f:
        data_csv = csv.DictReader(f)
        neos_list = [NearEarthObject(
            designation=str(row["pdes"]),
            name=row["name"] if row["name"] else None,
            diameter=float(
                row["diameter"]) if row["diameter"] else float('nan'),
            hazardous=True if row["pha"] == "Y" else False
        ) for row in data_csv]
    return neos_list


def load_approaches(cad_json_path: str):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches_list = []
    with open(cad_json_path) as f:
        data_json = json.load(f)
        fields = data_json["fields"]
        for row in data_json["data"]:
            row = dict(zip(fields, row))
            approach = CloseApproach(
                designation=str(row["des"]),
                time=row["cd"] if row["cd"] else None,
                distance=float(row["dist"]) if row["dist"] else 0.0,
                velocity=float(row["v_rel"] if row["v_rel"] else 0.0)
            )
            approaches_list.append(approach)
    return approaches_list


if __name__ == '__main__':
    neo_csv_path = "data/neos.csv"
    logger.info(f"Running load_neos with {neo_csv_path} file")
    data_csv = load_neos(neo_csv_path=neo_csv_path)
    assert len(data_csv) == 23967
    logger.info(f"First NEO: {data_csv[0]}")
    logger.info(f"Last NEO: {data_csv[-1]}")
    logger.info("load_neos passed")
    cad_json_path = "data/cad.json"
    logger.info(f"Running load_approaches with {cad_json_path} file")
    data_json = load_approaches(cad_json_path=cad_json_path)
    assert len(data_json) == 406785
    logger.info(f"First approach: {data_json[0]}")
    logger.info(f"Last approach: {data_json[-1]}")
    logger.info("load_approaches passed")
