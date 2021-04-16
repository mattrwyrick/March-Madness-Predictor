import json

from march_madness.settings import ACTUAL_EXCLUDE_YEARS
from march_madness.models.bracket import BracketActual, BracketSimulator


class PrinterOverall(object):
    def __init__(self, years, predictor, print_years=False):
        """
        Print out the accuracy of a simulated bracket for the given years
        :param years:
        :param predictor:
        :param print_years:
        """
        print()
        print(f"### {predictor.name} ###")
        stats = []
        accuracy_total = 0
        accuracy_count = 0
        for year in years:
            pred = predictor(year)
            simulator = BracketSimulator(year, pred)
            results = simulator.simulate_season()
            method = simulator.method
            winner = simulator.bracket[6][1].winner
            accuracy = "N/A"
            if year not in ACTUAL_EXCLUDE_YEARS:
                actual = BracketActual(year)
                accuracy = actual.score_bracket(results)
                accuracy_total += accuracy
                accuracy_count += 1

            result = f"{year} {accuracy} {winner}"
            stats.append(result)

        print(f"Overall: {accuracy_total / accuracy_count}")
        if print_years:
            print(json.dumps(stats, indent=4, sort_keys=True))


class PrinterByYear(object):

    def __init__(self, years, predictors, print_bracket=False):
        """
        Print out the accuracy of a simulated bracket for the given years
        :param years:
        :param predictors:
        :param print_bracket:
        """
        self.print_bracket = print_bracket

        for year in years:
            print()
            print(f"### {year} ###")
            print()
            for PClass in predictors:
                predictor = PClass(year)
                simulator = BracketSimulator(year, predictor)
                results = simulator.simulate_season()
                method = simulator.method
                winner = simulator.bracket[6][1].winner
                accuracy = "N/A"
                if year not in ACTUAL_EXCLUDE_YEARS:
                    actual = BracketActual(year)
                    accuracy = actual.score_bracket(results)
                self.printout(method, winner, accuracy, results)

    def printout(self, method, winner, accuracy, results):
        """
        Printout the results of a bracket
        :param method:
        :param winner:
        :param accuracy:
        :param results:
        :return:
        """
        print(method)
        print(winner)
        print(accuracy)
        if self.print_bracket:
            print(results)
        print()
        print()
