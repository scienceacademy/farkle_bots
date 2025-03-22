from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame, WIN_SCORE


class StudentBot(FarkleBot):
    """
    A template for students to create their own Farkle bot.

    This bot should implement a strategy for playing Farkle by deciding
    which dice to keep and when to end a turn.
    """

    def __init__(self, name="StudentBot"):
        super().__init__(name)
        # You can initialize any strategy parameters here

    def make_decision(self, state: TurnState) -> BotDecision:
        """
        Make a decision based on the current game state

        Parameters:
        - state: TurnState object containing:
            - current_dice: List of current dice values [1-6]
            - remaining_dice: Number of dice left to roll
            - turn_score: Score accumulated this turn
            - banked_score: Your current banked score
            - opponent_score: Opponent's banked score

        Returns:
        - BotDecision object with:
            - dice_to_keep: List of dice values to keep
            - roll_again: Boolean indicating whether to roll again (True) or end turn (False)
        """
        # Create a FarkleGame instance to use its helper methods
        game = FarkleGame(None, None)

        # Find scorable combinations from the current dice
        # This returns a list of tuples: (dice_combo, score)
        # Sorted by dice count and score (highest first)
        combos = game.find_scorable_combinations(state.current_dice)

        # No scorable combinations (should never happen as farkle is checked earlier)
        if not combos:
            return BotDecision([], False)

        # Select the best combination (most dice used, highest score)
        best_combo, score = combos[0]
        keep_dice = list(best_combo)

        # IMPLEMENT YOUR STRATEGY HERE:
        # Decide whether to roll again or end your turn

        # Example strategy (replace with your own):
        # Bank if we have accumulated at least 1000 points this turn
        # or if we're close to winning
        if (
            state.turn_score + score >= 1000
            or state.banked_score + state.turn_score + score >= WIN_SCORE
        ):
            roll_again = False
        else:
            roll_again = True

        return BotDecision(keep_dice, roll_again)


# You can add additional methods to your bot to make more sophisticated strategies
# For example:
"""
def calculate_risk(self, remaining_dice, turn_score):
    # Calculate the probability of farkling with the remaining dice
    # and weigh it against the current turn score

    pass

def should_play_safe(self, my_score, opponent_score):
    # Determine if we should play conservatively based on score difference

    pass
"""
