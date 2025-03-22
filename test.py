import os
import sys
import importlib.util
from farkle_framework import FarkleGame, SimpleBot


def print_colored(text, color_code):
    """Print text in color"""
    print(f"\033[{color_code}m{text}\033[0m")


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print_colored(f" {text} ", "1;36")
    print("=" * 60)


def load_student_bot(bot_file_path):
    """
    Load a student's bot from a Python file

    Args:
        bot_file_path: Path to the bot Python file

    Returns:
        An instance of the bot, or None if loading failed
    """
    try:
        # Get the filename without extension to use as the module name
        module_name = os.path.basename(bot_file_path)
        if module_name.endswith(".py"):
            module_name = module_name[:-3]

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, bot_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find bot classes (subclasses of FarkleBot)
        from farkle_framework import FarkleBot

        bot_class = None

        for item_name in dir(module):
            item = getattr(module, item_name)
            if (
                isinstance(item, type)
                and issubclass(item, FarkleBot)
                and item is not FarkleBot
                and item.__module__ == module_name
            ):
                bot_class = item
                break

        if bot_class is None:
            print_colored(f"No bot class found in {bot_file_path}", "1;31")
            return None

        # Create an instance of the bot
        bot = bot_class()
        print_colored(f"Successfully loaded bot: {bot.name}", "1;32")
        return bot

    except Exception as e:
        print_colored(f"Error loading bot from {bot_file_path}: {e}", "1;31")
        import traceback

        traceback.print_exc()
        return None


def play_test_games(student_bot, num_games=10):
    """
    Play a series of games between the student bot and SimpleBot

    Args:
        student_bot: The student's bot instance
        num_games: Number of games to play
    """
    opponent = SimpleBot("SimpleBot")
    student_wins = 0
    opponent_wins = 0
    student_total_score = 0
    opponent_total_score = 0
    verbose_game = None  # Store one game for detailed output

    print_header(f"Playing {num_games} games: {student_bot.name} vs {opponent.name}")

    # Play the games
    for game_num in range(num_games):
        # Alternate who goes first
        if game_num % 2 == 0:
            game = FarkleGame(student_bot, opponent)
            bot_idx = 0
            opp_idx = 1
        else:
            game = FarkleGame(opponent, student_bot)
            bot_idx = 1
            opp_idx = 0

        # For the first game, we'll keep the detailed log
        if game_num == 0:
            verbose_game = game

        # Play the game
        winner_idx = game.play_game()

        # Record the results
        if (winner_idx == 0 and game_num % 2 == 0) or (
            winner_idx == 1 and game_num % 2 == 1
        ):
            student_wins += 1
        else:
            opponent_wins += 1

        # Track scores
        if game_num % 2 == 0:  # Student was first
            student_total_score += game.scores[0]
            opponent_total_score += game.scores[1]
        else:  # Opponent was first
            student_total_score += game.scores[1]
            opponent_total_score += game.scores[0]

        # Print a simple progress indicator
        if (game_num + 1) % 5 == 0 or game_num == num_games - 1:
            print(f"Completed {game_num + 1}/{num_games} games...")

    # Print summary results
    print_header("Results Summary")
    print(
        f"{student_bot.name} wins: {student_wins} ({student_wins/num_games*100:.1f}%)"
    )
    print(f"{opponent.name} wins: {opponent_wins} ({opponent_wins/num_games*100:.1f}%)")
    print(f"\nAverage scores:")
    print(f"{student_bot.name}: {student_total_score/num_games:.1f}")
    print(f"{opponent.name}: {opponent_total_score/num_games:.1f}")

    # Print detailed log of the first game
    print_header("Detailed Log of First Game")
    for line in verbose_game.game_log:
        print(line)


def main():
    """Main function to handle the test script execution"""
    print_header("Farkle Bot Test Script")
    print("This script lets you test your bot against SimpleBot")

    # Check for command line arguments
    if len(sys.argv) > 1:
        bot_file = sys.argv[1]
        num_games = 10  # Default

        # Check for custom number of games
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            num_games = int(sys.argv[2])

        student_bot = load_student_bot(bot_file)
        if student_bot:
            play_test_games(student_bot, num_games)

    else:
        # Interactive mode
        print("\nNo bot file specified. Enter the path to your bot file:")
        bot_file = input("> ").strip()

        student_bot = load_student_bot(bot_file)
        if student_bot:
            print("\nHow many games would you like to play? (default: 10)")
            games_input = input("> ").strip()
            num_games = int(games_input) if games_input.isdigit() else 10

            play_test_games(student_bot, num_games)

    print("\nTest complete!")


if __name__ == "__main__":
    main()
