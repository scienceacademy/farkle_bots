
from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame, MINIMUM_SCORE

class ConservativeBot(FarkleBot):
    """A bot that plays very conservatively"""

    def make_decision(self, state: TurnState) -> BotDecision:
        game = FarkleGame(None, None)

        # Find best scorable combination
        combos = game.find_scorable_combinations(state.current_dice)
        if not combos:
            return BotDecision([], False)

        # Take the best combo
        best_combo, score = combos[0]

        # Always bank after getting some points
        # unless we have no score yet and haven't reached minimum
        if state.banked_score == 0 and state.turn_score + score < MINIMUM_SCORE:
            return BotDecision(list(best_combo), True)

        return BotDecision(list(best_combo), False)
