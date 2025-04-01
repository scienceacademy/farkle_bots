import random
import importlib.util
import os
# import sys
import csv
import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from dataclasses import dataclass
from collections import Counter, defaultdict

# === FARKLE GAME CONSTANTS ===
POINTS = {
    (1,): 100,  # Single 1
    (5,): 50,  # Single 5
    (1, 1, 1): 300,  # Three 1s
    (2, 2, 2): 200,  # Three 2s
    (3, 3, 3): 300,  # Three 3s
    (4, 4, 4): 400,  # Three 4s
    (5, 5, 5): 500,  # Three 5s
    (6, 6, 6): 600,  # Three 6s
    # Four of a kind
    (1, 1, 1, 1): 1000,
    (2, 2, 2, 2): 1000,
    (3, 3, 3, 3): 1000,
    (4, 4, 4, 4): 1000,
    (5, 5, 5, 5): 1000,
    (6, 6, 6, 6): 1000,
    # Five of a kind
    (1, 1, 1, 1, 1): 2000,
    (2, 2, 2, 2, 2): 2000,
    (3, 3, 3, 3, 3): 2000,
    (4, 4, 4, 4, 4): 2000,
    (5, 5, 5, 5, 5): 2000,
    (6, 6, 6, 6, 6): 2000,
    # Six of a kind
    (1, 1, 1, 1, 1, 1): 3000,
    (2, 2, 2, 2, 2, 2): 3000,
    (3, 3, 3, 3, 3, 3): 3000,
    (4, 4, 4, 4, 4, 4): 3000,
    (5, 5, 5, 5, 5, 5): 3000,
    (6, 6, 6, 6, 6, 6): 3000,
    # Straight
    (1, 2, 3, 4, 5, 6): 1500,
    # Three pairs
    (1, 1, 2, 2, 3, 3): 1500,
    (1, 1, 2, 2, 4, 4): 1500,
    (1, 1, 2, 2, 5, 5): 1500,
    (1, 1, 2, 2, 6, 6): 1500,
    (1, 1, 3, 3, 4, 4): 1500,
    (1, 1, 3, 3, 5, 5): 1500,
    (1, 1, 3, 3, 6, 6): 1500,
    (1, 1, 4, 4, 5, 5): 1500,
    (1, 1, 4, 4, 6, 6): 1500,
    (1, 1, 5, 5, 6, 6): 1500,
    (2, 2, 3, 3, 4, 4): 1500,
    (2, 2, 3, 3, 5, 5): 1500,
    (2, 2, 3, 3, 6, 6): 1500,
    (2, 2, 4, 4, 5, 5): 1500,
    (2, 2, 4, 4, 6, 6): 1500,
    (2, 2, 5, 5, 6, 6): 1500,
    (3, 3, 4, 4, 5, 5): 1500,
    (3, 3, 4, 4, 6, 6): 1500,
    (3, 3, 5, 5, 6, 6): 1500,
    (4, 4, 5, 5, 6, 6): 1500,
    # Two triplets
    (1, 1, 1, 2, 2, 2): 2500,
    (1, 1, 1, 3, 3, 3): 2500,
    (1, 1, 1, 4, 4, 4): 2500,
    (1, 1, 1, 5, 5, 5): 2500,
    (1, 1, 1, 6, 6, 6): 2500,
    (2, 2, 2, 3, 3, 3): 2500,
    (2, 2, 2, 4, 4, 4): 2500,
    (2, 2, 2, 5, 5, 5): 2500,
    (2, 2, 2, 6, 6, 6): 2500,
    (3, 3, 3, 4, 4, 4): 2500,
    (3, 3, 3, 5, 5, 5): 2500,
    (3, 3, 3, 6, 6, 6): 2500,
    (4, 4, 4, 5, 5, 5): 2500,
    (4, 4, 4, 6, 6, 6): 2500,
    (5, 5, 5, 6, 6, 6): 2500,
    # Four of a kind with pair
    (1, 1, 1, 1, 2, 2): 1500,
    (1, 1, 1, 1, 3, 3): 1500,
    (1, 1, 1, 1, 4, 4): 1500,
    (1, 1, 1, 1, 5, 5): 1500,
    (1, 1, 1, 1, 6, 6): 1500,
    (1, 1, 2, 2, 2, 2): 1500,
    (2, 2, 2, 2, 3, 3): 1500,
    (2, 2, 2, 2, 4, 4): 1500,
    (2, 2, 2, 2, 5, 5): 1500,
    (2, 2, 2, 2, 6, 6): 1500,
    (1, 1, 3, 3, 3, 3): 1500,
    (2, 2, 3, 3, 3, 3): 1500,
    (3, 3, 3, 3, 4, 4): 1500,
    (3, 3, 3, 3, 5, 5): 1500,
    (3, 3, 3, 3, 6, 6): 1500,
    (1, 1, 4, 4, 4, 4): 1500,
    (2, 2, 4, 4, 4, 4): 1500,
    (3, 3, 4, 4, 4, 4): 1500,
    (4, 4, 4, 4, 5, 5): 1500,
    (4, 4, 4, 4, 6, 6): 1500,
    (1, 1, 5, 5, 5, 5): 1500,
    (2, 2, 5, 5, 5, 5): 1500,
    (3, 3, 5, 5, 5, 5): 1500,
    (4, 4, 5, 5, 5, 5): 1500,
    (5, 5, 5, 5, 6, 6): 1500,
    (1, 1, 6, 6, 6, 6): 1500,
    (2, 2, 6, 6, 6, 6): 1500,
    (3, 3, 6, 6, 6, 6): 1500,
    (4, 4, 6, 6, 6, 6): 1500,
    (5, 5, 6, 6, 6, 6): 1500,
}

WIN_SCORE = 10000  # Score needed to win
MINIMUM_SCORE = 500  # Minimum score needed to bank


# === DATA STRUCTURES ===
@dataclass(frozen=True)
class TurnState:
    """Current state of a player's turn"""

    current_dice: List[int]  # Current dice values
    remaining_dice: int  # Number of dice remaining to roll
    turn_score: int  # Score accumulated this turn
    banked_score: int  # Player's banked score
    opponent_score: int  # Opponent's banked score


@dataclass
class BotDecision:
    """A bot's decision for its turn"""

    dice_to_keep: List[int]  # Which dice to keep (must be scorable)
    roll_again: bool  # Whether to roll again or end turn

    def __str__(self):
        action = "roll again" if self.roll_again else "end turn"
        return f"Keep dice {self.dice_to_keep} and {action}"


# === FARKLE BOT BASE CLASS ===
class FarkleBot(ABC):
    """Abstract base class for Farkle bots"""

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def make_decision(self, state: TurnState) -> BotDecision:
        """
        Make a decision based on the current game state

        Args:
            state: The current turn state

        Returns:
            A BotDecision object containing which dice to keep and whether to roll again
        """
        pass

    def __str__(self):
        return self.name


# === FARKLE GAME LOGIC ===
class FarkleGame:
    """Represents a single game of Farkle between two bots"""

    def __init__(self, bot1: FarkleBot, bot2: FarkleBot):
        self.bots = [bot1, bot2]
        self.scores = [0, 200]
        self.current_player = 0
        self.game_log = []
        self.max_turns = 100  # Safety to prevent infinite games
        self.turn_count = 0

    def roll_dice(self, num_dice: int) -> List[int]:
        """Roll the specified number of dice"""
        return [random.randint(1, 6) for _ in range(num_dice)]

    def find_scorable_combinations(
        self, dice: List[int]
    ) -> List[Tuple[Tuple[int, ...], int]]:
        """
        Find all valid scorable combinations from the dice

        Returns a list of (dice_combination, score) tuples
        """
        dice_sorted = sorted(dice)
        combinations = []

        # Check for special combinations (straight, three pairs)
        if len(dice) == 6:
            dice_tuple = tuple(dice_sorted)
            if dice_tuple in POINTS:
                combinations.append((dice_tuple, POINTS[dice_tuple]))

        # Check for N of a kind
        counts = Counter(dice)
        for num, count in counts.items():
            for i in range(min(count, 6), 0, -1):
                combo = tuple(num for _ in range(i))
                if combo in POINTS:
                    combinations.append((combo, POINTS[combo]))

        # Sort by number of dice used (descending) then by score (descending)
        combinations.sort(key=lambda x: (len(x[0]), x[1]), reverse=True)
        return combinations

    def calculate_score(self, dice_to_score: List[int]) -> int:
        """Calculate the score for the selected dice"""
        dice_sorted = sorted(dice_to_score)

        # Check if the combination exists in POINTS
        if tuple(dice_sorted) in POINTS:
            return POINTS[tuple(dice_sorted)]

        # If not a predefined combination, calculate score by breaking it down
        combinations = self.find_scorable_combinations(dice_sorted)
        if not combinations:
            return 0

        # Use the first (best) combination
        score = combinations[0][1]
        # remove the best combo and check for extra 1, 5 dice
        ds = dice_sorted.copy()
        for d in combinations[0][0]:
            ds.remove(d)
        r = []
        for d in ds:
            if d == 1:
                score += 100
                r.append(d)
            if d == 5:
                score += 50
                r.append(d)
        for d in r:
            ds.remove(d)
        if len(ds) > 0:
            return 0
        return score

    def validate_decision(self, decision: BotDecision, state: TurnState) -> bool:
        """Validate that a bot's decision is legal"""
        # Check that dice_to_keep is a subset of current_dice
        dice_counts = Counter(state.current_dice)
        keep_counts = Counter(decision.dice_to_keep)

        for die, count in keep_counts.items():
            if count > dice_counts[die]:
                return False

        # Check that dice_to_keep is scorable
        score = self.calculate_score(decision.dice_to_keep)
        if score == 0:
            return False

        return True

    def play_turn(self, bot_index: int) -> int:
        """
        Play a single turn for the given bot

        Returns the score earned in this turn
        """
        bot = self.bots[bot_index]
        opponent_index = 1 - bot_index
        turn_score = 0
        remaining_dice = 6

        while remaining_dice > 0:
            # Roll the dice
            current_dice = self.roll_dice(remaining_dice)
            self.game_log.append(f"{bot.name} rolled: {current_dice}")

            # Check for farkle (no scorable dice)
            if not self.find_scorable_combinations(current_dice):
                self.game_log.append(f"{bot.name} FARKLED! Turn score reset to 0.")
                return 0

            # Create the state object
            state = TurnState(
                current_dice=current_dice,
                remaining_dice=remaining_dice,
                turn_score=turn_score,
                banked_score=self.scores[bot_index],
                opponent_score=self.scores[opponent_index],
            )

            # Get the bot's decision
            # self.game_log.append(f"Sending {state} to {bot.name}")
            decision = bot.make_decision(state)
            self.game_log.append(f"{bot.name} decided to: {decision}")

            # Validate the decision
            if not self.validate_decision(decision, state):
                self.game_log.append(
                    f"INVALID DECISION from {bot.name}. Turn score reset to 0."
                )
                return 0

            # Update turn information
            decision_score = self.calculate_score(decision.dice_to_keep)
            turn_score += decision_score
            remaining_dice -= len(decision.dice_to_keep)

            # If all dice used, get a fresh set
            if remaining_dice == 0:
                remaining_dice = 6
                self.game_log.append(
                    f"{bot.name} used all dice! Gets to roll 6 new dice."
                )

            # Check if bot wants to roll again
            if not decision.roll_again:
                if turn_score < MINIMUM_SCORE and self.scores[bot_index] == 0:
                    self.game_log.append(
                        f"{bot.name} tried to bank less than {MINIMUM_SCORE} on first score. "
                        f"Must continue rolling."
                    )
                    continue

                self.game_log.append(f"{bot.name} ends turn with {turn_score} points.")
                return turn_score

        return turn_score

    def play_game(self) -> int:
        """
        Play a complete game of Farkle

        Returns the index of the winning bot
        """
        self.game_log.append(
            f"Game between {self.bots[0].name} and {self.bots[1].name}"
        )

        while max(self.scores) < WIN_SCORE and self.turn_count < self.max_turns:
            self.turn_count += 1
            self.game_log.append(
                f"\nTurn {self.turn_count}: {self.bots[self.current_player].name}'s turn"
            )
            self.game_log.append(
                f"Current scores: {self.bots[0].name}: {self.scores[0]}, "
                f"{self.bots[1].name}: {self.scores[1]}"
            )

            # Play the turn and add to score
            turn_score = self.play_turn(self.current_player)
            self.scores[self.current_player] += turn_score

            # Check for game end
            if self.scores[self.current_player] >= WIN_SCORE:
                self.game_log.append(
                    f"\n{self.bots[self.current_player].name} WINS with "
                    f"{self.scores[self.current_player]} points!"
                )
                return self.current_player

            # Switch to the other player
            self.current_player = 1 - self.current_player

        # If we hit max turns, whoever has the highest score wins
        if self.turn_count >= self.max_turns:
            winner = 0 if self.scores[0] >= self.scores[1] else 1
            self.game_log.append(
                f"\nMax turns reached. {self.bots[winner].name} WINS with "
                f"{self.scores[winner]} points!"
            )
            return winner

        return self.current_player  # In case of unexpected exit


# === TOURNAMENT MANAGER ===
class FarkleTournament:
    """Manages a tournament of multiple Farkle bots"""

    def __init__(self, bot_directory: str = "bots"):
        self.bot_directory = bot_directory
        self.bots = []
        self.results = {}
        self.load_bots()

    def load_bots(self):
        """Load all bot classes from the bot directory"""
        # Create the directory if it doesn't exist
        if not os.path.exists(self.bot_directory):
            os.makedirs(self.bot_directory)

        # Get all Python files in the directory
        bot_files = [
            f
            for f in os.listdir(self.bot_directory)
            if f.endswith(".py") and f != "__init__.py"
        ]

        # Import each bot file
        for file in bot_files:
            module_name = file[:-3]  # Remove .py extension
            file_path = os.path.join(self.bot_directory, file)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find all FarkleBot subclasses in the module
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (
                        isinstance(item, type)
                        and issubclass(item, FarkleBot)
                        and item is not FarkleBot
                    ):
                        self.bots.append(item())
                        print(f"Loaded bot: {item.__name__}")
            except Exception as e:
                print(f"Error loading bot from {file}: {e}")

    def run_match(self, bot1: FarkleBot, bot2: FarkleBot, num_games: int) -> Dict:
        """Run a match of multiple games between two bots"""
        wins = [0, 0]
        total_scores = [0, 0]
        total_turns = 0

        print(f"Running match: {bot1.name} vs {bot2.name} ({num_games} games)")

        for game_num in range(num_games):
            # Alternate who goes first
            if game_num % 2 == 0:
                game = FarkleGame(bot1, bot2)
            else:
                game = FarkleGame(bot2, bot1)

            winner_idx = game.play_game()
            # Map the winner back to the original bot order
            winner = winner_idx if game_num % 2 == 0 else 1 - winner_idx

            # Update stats
            wins[winner] += 1

            # Map scores back to original bot order
            if game_num % 2 == 0:
                total_scores[0] += game.scores[0]
                total_scores[1] += game.scores[1]
            else:
                total_scores[0] += game.scores[1]
                total_scores[1] += game.scores[0]

            total_turns += game.turn_count

        # Calculate stats
        match_results = {
            "games": num_games,
            "wins": {bot1.name: wins[0], bot2.name: wins[1]},
            "win_percentage": {
                bot1.name: wins[0] / num_games * 100,
                bot2.name: wins[1] / num_games * 100,
            },
            "average_score": {
                bot1.name: total_scores[0] / num_games,
                bot2.name: total_scores[1] / num_games,
            },
            "average_turns": total_turns / num_games,
        }

        return match_results

    def run_tournament(self, games_per_match: int = 100) -> Dict:
        """Run a tournament with all loaded bots"""
        if len(self.bots) < 2:
            print("Not enough bots loaded for a tournament")
            return {}

        tournament_results = {}

        # Run matches between each pair of bots
        for i, bot1 in enumerate(self.bots):
            for j, bot2 in enumerate(self.bots):
                if i >= j:  # Skip duplicate matches and self-matches
                    continue

                match_key = f"{bot1.name}_vs_{bot2.name}"
                match_results = self.run_match(bot1, bot2, games_per_match)
                tournament_results[match_key] = match_results

                # Print match summary
                print(f"\nMatch summary: {bot1.name} vs {bot2.name}")
                print(
                    f"  {bot1.name} wins: {match_results['wins'][bot1.name]} "
                    f"({match_results['win_percentage'][bot1.name]:.1f}%)"
                )
                print(
                    f"  {bot2.name} wins: {match_results['wins'][bot2.name]} "
                    f"({match_results['win_percentage'][bot2.name]:.1f}%)"
                )
                print(
                    f"  Average scores: {bot1.name}: {match_results['average_score'][bot1.name]:.1f}, "
                    f"{bot2.name}: {match_results['average_score'][bot2.name]:.1f}"
                )

        # Calculate overall stats
        bot_stats = defaultdict(lambda: {"wins": 0, "games": 0, "total_score": 0})

        for match_key, results in tournament_results.items():
            bot1_name, bot2_name = match_key.split("_vs_")

            bot_stats[bot1_name]["wins"] += results["wins"][bot1_name]
            bot_stats[bot1_name]["games"] += results["games"]
            bot_stats[bot1_name]["total_score"] += (
                results["average_score"][bot1_name] * results["games"]
            )

            bot_stats[bot2_name]["wins"] += results["wins"][bot2_name]
            bot_stats[bot2_name]["games"] += results["games"]
            bot_stats[bot2_name]["total_score"] += (
                results["average_score"][bot2_name] * results["games"]
            )

        # Calculate win percentages and average scores
        for bot_name, stats in bot_stats.items():
            stats["win_percentage"] = (
                stats["wins"] / stats["games"] * 100 if stats["games"] > 0 else 0
            )
            stats["average_score"] = (
                stats["total_score"] / stats["games"] if stats["games"] > 0 else 0
            )

        # Sort bots by win percentage
        sorted_bots = sorted(
            bot_stats.items(), key=lambda x: x[1]["win_percentage"], reverse=True
        )

        # Print tournament summary
        print("\n=== Tournament Results ===")
        print(f"Bots: {len(self.bots)}, Games per match: {games_per_match}")
        print("\nRankings:")
        for rank, (bot_name, stats) in enumerate(sorted_bots, 1):
            print(
                f"{rank}. {bot_name}: {stats['win_percentage']:.1f}% wins, "
                f"Avg score: {stats['average_score']:.1f}"
            )

        # Store results
        self.results = {
            "matches": tournament_results,
            "bot_stats": bot_stats,
            "rankings": [
                {
                    "rank": i + 1,
                    "name": bot_name,
                    "win_percentage": stats["win_percentage"],
                    "average_score": stats["average_score"],
                    "wins": stats["wins"],
                    "games": stats["games"],
                }
                for i, (bot_name, stats) in enumerate(sorted_bots)
            ],
        }

        # Generate and save tournament results tables
        self.save_tournament_results(games_per_match)

        return self.results

    def save_tournament_results(self, games_per_match):
        """Save tournament results in CSV and Markdown formats"""
        if not self.results or not self.results.get("rankings"):
            print("No tournament results to save")
            return

        # Create results directory if it doesn't exist
        results_dir = "tournament_results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Generate timestamp for filenames
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate CSV file
        csv_filename = os.path.join(results_dir, f"tournament_results_{timestamp}.csv")
        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = [
                "Rank",
                "Bot Name",
                "Win %",
                "Wins",
                "Games Played",
                "Avg Score",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for bot in self.results["rankings"]:
                writer.writerow(
                    {
                        "Rank": bot["rank"],
                        "Bot Name": bot["name"],
                        "Win %": f"{bot['win_percentage']:.1f}%",
                        "Wins": bot["wins"],
                        "Games Played": bot["games"],
                        "Avg Score": f"{bot['average_score']:.1f}",
                    }
                )

        # Generate Markdown file
        md_filename = os.path.join(results_dir, f"tournament_results_{timestamp}.md")
        with open(md_filename, "w") as mdfile:
            mdfile.write(f"# Farkle Tournament Results\n\n")
            mdfile.write(
                f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            mdfile.write(f"**Bots:** {len(self.bots)}\n\n")
            mdfile.write(f"**Games per match:** {games_per_match}\n\n")

            # Rankings table
            mdfile.write("## Rankings\n\n")
            mdfile.write(
                "| Rank | Bot Name | Win % | Wins | Games Played | Avg Score |\n"
            )
            mdfile.write(
                "|------|---------|-------|------|--------------|----------|\n"
            )

            for bot in self.results["rankings"]:
                mdfile.write(
                    f"| {bot['rank']} | {bot['name']} | {bot['win_percentage']:.1f}% | "
                )
                mdfile.write(
                    f"{bot['wins']} | {bot['games']} | {bot['average_score']:.1f} |\n"
                )

            # Match results
            mdfile.write("\n## Match Results\n\n")
            mdfile.write(
                "| Bot 1 | Bot 2 | Bot 1 Wins | Bot 2 Wins | Bot 1 Win % | Bot 2 Win % |\n"
            )
            mdfile.write(
                "|-------|-------|------------|------------|-------------|-------------|\n"
            )

            for match_key, results in self.results["matches"].items():
                bot1_name, bot2_name = match_key.split("_vs_")
                mdfile.write(f"| {bot1_name} | {bot2_name} | ")
                mdfile.write(
                    f"{results['wins'][bot1_name]} | {results['wins'][bot2_name]} | "
                )
                mdfile.write(f"{results['win_percentage'][bot1_name]:.1f}% | ")
                mdfile.write(f"{results['win_percentage'][bot2_name]:.1f}% |\n")

        print(f"\nResults saved to:")
        print(f"  CSV: {csv_filename}")
        print(f"  Markdown: {md_filename}")


# === EXAMPLE BOTS ===
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

        roll_again = state.turn_score + score < bank_threshold

        return BotDecision(keep_dice, roll_again)


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


# === MAIN FUNCTION ===
def main():
    # Create the bots directory if it doesn't exist
    if not os.path.exists("bots"):
        os.makedirs("bots")

        # Create example bot files
        with open("bots/simple_bot.py", "w") as f:
            f.write(
                """
from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame, WIN_SCORE

class SimpleBot(FarkleBot):
    \"\"\"A simple bot that makes basic decisions\"\"\"

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
"""
            )

        with open("bots/conservative_bot.py", "w") as f:
            f.write(
                """
from farkle_framework import FarkleBot, BotDecision, TurnState, FarkleGame, MINIMUM_SCORE

class ConservativeBot(FarkleBot):
    \"\"\"A bot that plays very conservatively\"\"\"

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
"""
            )

    # Run a test tournament with example bots
    tournament = FarkleTournament()
    if len(tournament.bots) > 0:
        tournament.run_tournament(games_per_match=50)
    else:
        print(
            "No bots found. Please create bot implementations in the 'bots' directory."
        )
        print("Example bots have been created to help you get started.")


if __name__ == "__main__":
    main()
