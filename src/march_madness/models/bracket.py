import os
import csv
import math

from march_madness.settings import TEAM_YEARS, BRACKET_DIR


class Game(object):

    def __init__(self, rid, gid, team1, seed1, score1, team2, seed2, score2, overtime):
        """
        Game representation
        :param rid: int
        :param gid: int
        :param team1: str
        :param seed1: int
        :param score1: int
        :param team2: str
        :param seed2: int
        :param score2: int
        """
        self.rid = rid
        self.gid = gid
        self.team1 = team1
        self.seed1 = seed1
        self.score1 = score1 if score1 and score1 > -1 else None
        self.team2 = team2
        self.seed2 = seed2
        self.score2 = score2 if score2 and score2 > -1 else None
        self.overtime = overtime

    @property
    def winner(self):
        """
        Get the winner of the game
        :return:
        """
        if self.score1 and self.score2:
            return self.team1 if self.score1 > self.score2 else self.team2
        return None

    def __str__(self):
        if self.team1 == self.winner:
            loser = self.team2
        else:
            loser = self.team1
        if self.winner is not None:
            return f"R{self.rid}G{self.gid} {self.winner} beat {loser}"
        return f"R{self.rid}G{self.gid} {self.team1} vs {self.team2}"

    def __repr__(self):
        if self.team1 == self.winner:
            loser = self.team2
        else:
            loser = self.team1
        if self.winner is not None:
            return f"R{self.rid}G{self.gid} {self.winner} beat {loser}"
        return f"R{self.rid}G{self.gid} {self.team1} vs {self.team2}"







class Bracket(object):

    def __init__(self, year, *args):
        """
        Abstract class for a bracket
        :param year:
        :param args:
        """
        self.round_mapping = {

            1: {
                "west": [1, 2, 3, 4, 5, 6, 7, 8],
                "east": [9, 10, 11, 12, 13, 14, 15, 16],
                "south": [17, 18, 19, 20, 21, 22, 23, 24],
                "midwest": [25, 26, 27, 28, 29, 30, 31, 32]
            },

            2: {
                "west": [1, 2, 3, 4],
                "east": [5, 6, 7, 8],
                "south": [9, 10, 11, 12],
                "midwest": [13, 14, 15, 16]
            },

            3: {
                "west": [1, 2],
                "east": [3, 4],
                "south": [5, 6],
                "midwest": [7, 8]
            },

            4: {
                "west": [1],
                "east": [2],
                "south": [3],
                "midwest": [4]
            },

            5: {
                "west": [1],
                "east": [1],
                "south": [2],
                "midwest": [2],
            },

            6: {
                "west": [1],
                "east": [1],
                "south": [1],
                "midwest": [1],
            }
        }

        self.year = int(year)
        if self.year not in TEAM_YEARS:
            raise Exception(f"{year} is not a valid year.")

        self.path = os.path.join(BRACKET_DIR, f"{year}.csv")


class BracketActual(Bracket):

    def __init__(self, year, *args):
        """
        Create a bracket with results
        :param year:
        """
        super().__init__(year)
        self.bracket = self.load_bracket()

    def load_bracket(self):
        """
        Load the complete bracket of the given year
        :return:
        """
        results = {(i+1): {} for i in range(6)}
        with open(self.path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rid = int(row[0])
                gid = int(row[1])
                team1 = row[2]
                seed1 = int(row[3])
                score1 = int(row[4].split(" ")[0]) if "OT" in row[4] else int(row[4])
                team2 = row[5]
                seed2 = int(row[6])
                score2 = int(row[7].split(" ")[0]) if "OT" in row[7] else int(row[7])
                overtime = "OT" in row[7] or "OT" in row[4]
                game = Game(rid, gid, team1, seed1, score1, team2, seed2, score2, overtime)
                results[rid][gid] = game
        return results

    def score_bracket(self, bracket):
        """
        Score a simulated bracket
        :param bracket:
        :return:
        """
        total = 0.0
        correct = 0.0
        for rid in bracket:
            for gid in bracket[rid]:
                if bracket[rid][gid].winner == self.bracket[rid][gid].winner:
                    correct += 1.0
                total += 1.0
        if total == 0:
            return None
        return correct / total


class BracketSimulator(Bracket):

    def __init__(self, year, predictor):
        """
        Create a bracket for simulation
        :param year:
        :param predictor:
        :return:
        """
        super().__init__(year)
        self.method = predictor.name
        self.bracket = self.load_bracket()
        self.predictor = predictor
        self.current_round = 1

    def load_bracket(self):
        """
        Load the first round of the given bracket
        :return:
        """
        results = {(i+1): {} for i in range(6)}
        with open(self.path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rid = int(row[0])
                if rid > 1:
                    break

                gid = int(row[1])
                team1 = row[2]
                seed1 = int(row[3])
                score1 = None
                team2 = row[5]
                seed2 = int(row[6])
                score2 = None
                overtime = "OT" in row[7] or "OT" in row[4]


                game = Game(rid, gid, team1, seed1, score1, team2, seed2, score2, overtime)
                results[rid][gid] = game

        for rid in self.round_mapping:
            if rid == 1:
                continue

            sections = self.round_mapping[rid]
            for section in sections:
                gids = sections[section]
                for gid in gids:
                    game = Game(rid, gid, None, None, None, None, None, None, None)
                    results[rid][gid] = game

        return results

    def simulate_season(self):
        """
        Simulate an entire season
        :return:
        """
        for i in range(6):
            self.simulate_round()
        return self.bracket

    def simulate_round(self):
        """
        Simulate the current round
        :return:
        """
        if self.current_round > 7:
            raise Exception("No more rounds to simulate.")

        games = self.bracket[self.current_round]
        for gid in games:
            game = games[gid]
            self.predictor.predict(game)
            winner = game.winner
            if winner == game.team1:
                sid = game.seed1
            else:
                sid = game.seed2
            self.prepare_next_round(game.rid, game.gid, winner, sid)

        self.current_round += 1

    def prepare_next_round(self, rid, gid, team, sid):
        """
        Prepare the next round for simulation
        :param rid: int
        :param gid: int
        :param team: str
        :param sid: int
        :return:
        """
        if rid + 1 < 7:
            next_rid = rid + 1
            gvalue = gid / 2.0
            next_gid = math.ceil(gid / 2.0)
            if next_gid > gvalue:
                self.bracket[next_rid][next_gid].team1 = team
                self.bracket[next_rid][next_gid].seed1 = sid
            else:
                self.bracket[next_rid][next_gid].team2 = team
                self.bracket[next_rid][next_gid].seed2 = sid

