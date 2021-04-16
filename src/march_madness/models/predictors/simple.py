import os
import json

from march_madness.settings import INDEX_DIR
from march_madness.tools import load_conference_team_data, load_conference_data, get_unit_scores
from march_madness.models.predictors.base import Predictor


class SimpleV2Predictor(Predictor):

    name = "simple v2"

    def __init__(self, year):
        """
        Simple predictor using pre-calculated metrics
        :param year:
        """
        self.year = year
        self.index_path = os.path.join(INDEX_DIR, f"{self.year}.json")
        with open(self.index_path, "r") as f:
            self.index = json.load(f)

    def _predict(self, game):
        """
        Predict the game
        :param game:
        :return:
        """
        cname1 = self.index[game.team1][0]
        conf1 = self.index[game.team1][1]
        trow_header, trow1 = load_conference_team_data(self.year, conf1, cname1)
        crow_header, crow1 = load_conference_data(self.year, conf1)
        srs1 = trow1[10]
        conf_srs1 = crow1[6]

        cname2 = self.index[game.team2][0]
        conf2 = self.index[game.team2][1]
        trow_header, trow2 = load_conference_team_data(self.year, conf2, cname2)
        crow_header, crow2 = load_conference_data(self.year, conf2)
        srs2 = trow2[10]
        conf_srs2 = crow2[6]

        srs1 = float(srs1) if srs1 is not None else 0
        srs2 = float(srs2) if srs2 is not None else 0
        conf_srs1 = float(conf_srs1) if conf_srs1 is not None else 0
        conf_srs2 = float(conf_srs2) if conf_srs2 is not None else 0

        weight = .55
        score1 = (weight * srs1) + ((1-weight) * conf_srs1)
        score2 = (weight * srs2) + ((1-weight) * conf_srs2)

        if score1 > score2:
            game.score1 = 2
            game.score2 = 1
        else:
            game.score1 = 1
            game.score2 = 2

        return game.winner


class SimpleV1Predictor(Predictor):

    name = "simple v1"

    def __init__(self, year):
        """
        Simple predictor using pre-calculated metrics
        :param year:
        """
        self.year = year
        self.index_path = os.path.join(INDEX_DIR, f"{self.year}.json")
        with open(self.index_path, "r") as f:
            self.index = json.load(f)

    def _predict(self, game):
        """
        Predict the game
        :param game:
        :return:
        """
        cname1 = self.index[game.team1][0]
        conf1 = self.index[game.team1][1]
        trow_header, trow1 = load_conference_team_data(self.year, conf1, cname1)
        crow_header, crow1 = load_conference_data(self.year, conf1)
        srs1 = trow1[10]
        conf_srs1 = crow1[6]
        points1 = trow1[8]

        cname2 = self.index[game.team2][0]
        conf2 = self.index[game.team2][1]
        trow_header, trow2 = load_conference_team_data(self.year, conf2, cname2)
        crow_header, crow2 = load_conference_data(self.year, conf2)
        srs2 = trow2[10]
        conf_srs2 = crow2[6]
        points2 = trow2[8]

        srs1 = float(srs1)
        srs2 = float(srs2)
        conf_srs1 = float(conf_srs1)
        conf_srs2 = float(conf_srs2)
        points1 = float(points1)
        points2 = float(points2)

        w1 = 95  # srs team
        w2 = 5 # srs conf
        w3 = 0  # points per game
        wt = (w1 + w2 + w3) * 1.0

        srs1_score, srs2_score = get_unit_scores(srs1, srs2)
        conf_srs1_score, conf_srs2_score = get_unit_scores(conf_srs1, conf_srs2)
        p1_score, p2_score = get_unit_scores(points1, points2)

        score1 = (w1/wt * srs1_score) + (w2/wt * conf_srs1_score) + (w3/wt * p1_score)
        score2 = (w1/wt * srs2_score) + (w2/wt * conf_srs2_score) + (w3/wt * p2_score)

        if score1 > score2:
            game.score1 = 2
            game.score2 = 1
        else:
            game.score1 = 1
            game.score2 = 2

        return game.winner



