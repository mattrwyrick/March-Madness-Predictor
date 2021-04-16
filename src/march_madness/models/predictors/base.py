
from march_madness.models.bracket import Game


class Predictor(object):

    name = "predictor"

    def predict(self, game):
        """
        Predict a game
        :param game:
        :return:
        """
        self.check_first_four(game)
        self._predict(game)
        return game.winner

    def check_first_four(self, game):
        """
        Check if a name is a rat tail game (use mutation on game object)
        :param Game: Game
        :return:
        """
        if game.rid == 1:
            if "/" in game.team1:
                t1, t2 = game.team1.split("/")
                tmp_game = Game(0, 0, t1, game.seed1, None, t2, game.seed1, None, None)
                winner = self._predict(tmp_game)
                if winner is None:
                    check = 1
                game.team1 = winner

            if "/" in game.team2:
                t1, t2 = game.team2.split("/")
                tmp_game = Game(0, 0, t1, game.seed2, None, t2, game.seed2, None, None)
                winner = self._predict(tmp_game)
                if winner is None:
                    check = 1
                game.team2 = winner

        return

    def _predict(self, game):
        """
        Predict the outcome of a game (use mutation on game object)
        :param game:
        :return:
        """
        pass
