# Farkle Bot Framework

## Framework Structure

This framework consists of:

1. `farkle_framework.py` - The main framework file containing:
   - `FarkleBot` - Base class for student bots
   - `FarkleGame` - Game logic for a single Farkle game
   - `FarkleTournament` - Tournament manager to run multiple games between bots
   - Example bots and utility functions

2. `bot_template.py` - A template for students to create their own bots

3. `run_tournament.py` - Script to run tournaments

## Getting Started

### Installation

1. Clone or download this repository
2. Make sure you have Python 3.6+ installed
3. No additional libraries are required

### Creating Your Bot

1. Copy the `bot_template.py` file to the `bots` directory and rename it (e.g., `my_awesome_bot.py`)
2. Edit the file to implement your strategy in the `make_decision` method
3. Customize the class name and add any helper methods you need

Example:

```python
from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame

class MyAwesomeBot(FarkleBot):

    def make_decision(self, state: TurnState) -> BotDecision:
        game = FarkleGame(None, None)
        combos = game.find_scorable_combinations(state.current_dice)

        # Your strategy here
        # ...

        return BotDecision(dice_to_keep, roll_again)
```

### Running Tournaments

To run a tournament with all bots in the `bots` directory:

```
python run_tournament.py tournament [games_per_match]
```

The optional `games_per_match` parameter specifies how many games to play between each pair of bots.

### Testing your bot

To see how your bot is behaving, you can run a test game against SimpleBot:

```
python test.py bots/my_awesome_bot.py [n]
```

This will run `n` games between the bots and display a detailed game log.

## Understanding the Framework

### Important Classes and Methods

#### `FarkleBot` (Abstract Base Class)

Your bot must extend this class and implement the `make_decision` method:

```python
def make_decision(self, state: TurnState) -> BotDecision:
    """
    Make a decision based on the current game state

    Args:
        state: The current turn state

    Returns:
        A BotDecision object with which dice to keep and whether to roll again
    """
```

#### `TurnState` (Class)

This class contains all the information your bot needs to make a decision:

- `current_dice` - List of current dice values [1-6]
- `remaining_dice` - Number of dice left to roll
- `turn_score` - Score accumulated in this turn
- `banked_score` - Your bot's current banked score
- `opponent_score` - Opponent's banked score

#### `BotDecision` (Class)

Your bot must return a `BotDecision` object with:

- `dice_to_keep` - List of dice values to keep (must be scorable)
- `roll_again` - Boolean indicating whether to roll again (True) or end turn (False)

#### Useful Helper Methods

- `FarkleGame.find_scorable_combinations(dice)` - Returns all valid scoring combinations for a set of dice
- `FarkleGame.calculate_score(dice)` - Calculates the score for a set of dice

## Example Bots

The framework includes two example bots:

1. `SimpleBot` - Makes basic decisions using a fixed bank threshold
2. `ConservativeBot` - Plays very conservatively, banking after any score

Study these bots to understand how to implement your own strategy.

## Tips for Success

1. Test your bot thoroughly against different opponents
2. Implement probability calculations for risk assessment
3. Create helper methods for different aspects of your strategy
4. Document your strategy decisions in code comments
5. Balance aggression with security based on game state
6. Consider the opponent's score and position when making decisions

Good luck, and may the best bot win!
