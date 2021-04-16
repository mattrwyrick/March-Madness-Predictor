import os
import csv
import json

from march_madness.settings import (
    DATA_DIR,
    CONFERENCE_WITH_TEAM_DIR,
    CONFERENCE_OVERALL_DIR,
    INDEX_DIR,
    TEAM_YEARS,
)


def get_unit_scores(v1, v2):
    """
    return the unit scores
    :param v1:
    :param v2:
    :return:
    """
    s1 = (v1 * 1.0) / (1.0 * v1 + 1.0 * v2)
    s2 = (v2 * 1.0) / (1.0 * v1 + 1.0 * v2)
    return s1, s2


def load_conference_data(year, conference):
    """

    :param year:
    :param conference:
    :return:
    """
    path = os.path.join(CONFERENCE_OVERALL_DIR, f"{year}.csv")
    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            name = row[1]
            if name == conference:
                return header, row
    print(conference)
    print(year)
    return None, None


def load_conference_team_data(year, conference, team):
    """
    Load the conference team data
    :param year:
    :param conference:
    :param team:
    :return:
    """
    path = os.path.join(CONFERENCE_WITH_TEAM_DIR, conference, f"{year}.csv")
    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            name = row[1]
            if name == team:
                return header, row


def create_team_index():
    """
    Create the index of team names (alt included), conferences, and year
    :return:
    """
    with open(os.path.join(DATA_DIR, "names.json")) as f:
        mapping = json.load(f)
        inverted_mapping = {mapping[key]: key for key in mapping}

    conferences = os.listdir(CONFERENCE_WITH_TEAM_DIR)
    index = {int(year): dict() for year in TEAM_YEARS}
    for conference in conferences:
        conf_path = os.path.join(CONFERENCE_WITH_TEAM_DIR, conference)
        for year_csv in os.listdir(conf_path):
            path = os.path.join(conf_path, year_csv)
            with open(path, "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    ctname = row[1]
                    btname = inverted_mapping[ctname] if ctname in inverted_mapping else ctname
                    year = int(year_csv.split(".")[0])
                    index[year][btname] = [ctname, conference]

    for year in index:
        path = os.path.join(INDEX_DIR, f"{year}.json")
        with open(path, "w") as f:
            json.dump(index[year], f, indent=4, sort_keys=True)


if __name__ == "__main__":
    create_team_index()




