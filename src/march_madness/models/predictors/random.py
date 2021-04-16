import random

from march_madness.models.predictors.base import Predictor


class RandomPredictor(Predictor):

    name = "random"

    def __init__(self, *args):
        """
        Predictor class to support bracket simulations
        :param args:
        """
        pass

    def _predict(self, game):
        """
        Update the game to reflect the winner
        :param game: Game
        :return:
        """

        score1 = random.randint(2, 10)
        score2 = random.randint(2, 10)
        if score1 == score2:
            tie = random.randint(0, 10)
            score1 = score1 + 1 if tie % 2 == 0 else score1 - 1

        game.score1 = score1
        game.score2 = score2
        return game.winner
