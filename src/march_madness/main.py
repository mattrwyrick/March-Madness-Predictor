import json

from march_madness.tools import create_team_index
from march_madness.models.display import PrinterOverall
from march_madness.models.bracket import BracketSimulator, BracketActual

from march_madness.models.predictors.random import RandomPredictor
from march_madness.models.predictors.simple import SimpleV1Predictor, SimpleV2Predictor


years = [2018, 2019]
predictors = [RandomPredictor, SimpleV1Predictor, SimpleV2Predictor]


if __name__ == "__main__":
    create_team_index()
    PrinterOverall(years, SimpleV1Predictor)
    PrinterOverall(years, SimpleV2Predictor)

    year = 2021
    p = SimpleV1Predictor(year)
    bracket = BracketSimulator(year, p)
    results = bracket.simulate_season()

    for rid in results:
        for gid in results[rid]:
            game = results[rid][gid]
            team1 = game.team1
            team2 = game.team2
            if game.winner == team1:
                if game.seed1 > game.seed2:
                    print(f"{game.seed1}:{game.seed2} {game}")
            elif game.winner == team2:
                if game.seed2 > game.seed1:
                    print(f"{game.seed2}:{game.seed1} {game}")


    check = 1



