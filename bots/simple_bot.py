
from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame, WIN_SCORE

# Rename this class to *your* name
# --------------------------------
class SimpleBot(FarkleBot):
    """A simple bot that makes basic decisions"""

    def make_decision(self, state: TurnState) -> BotDecision:
        game = FarkleGame(None, None)  # Just for using its methods

        # Find best scorable combination
        combos = game.find_scorable_combinations(state.current_dice)

        # Take the best combo
        best_combo, score = combos[0]

        # Convert tuple to list
        keep_dice = list(best_combo)

        # Simple strategy: bank if we have more than 500 points
        # or if we're close to winning
        bank_threshold = 500

        # If we're close to winning, lower the threshold
        if state.banked_score + state.turn_score + score >= WIN_SCORE:
            bank_threshold = 0

        # If opponent is close to winning, be more aggressive
        if state.opponent_score > state.banked_score and state.opponent_score > 7000:
            bank_threshold = 300

        roll_again = (state.turn_score + score < bank_threshold)

        return BotDecision(keep_dice, roll_again)
