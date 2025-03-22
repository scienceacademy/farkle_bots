import sys
import os
from farkle_framework import FarkleTournament, FarkleGame

def run_tournament(games_per_match=50):
    """Run a tournament with all bots in the 'bots' directory"""
    tournament = FarkleTournament()
    if len(tournament.bots) > 0:
        results = tournament.run_tournament(games_per_match=games_per_match)
        return results
    else:
        print(
            "No bots found. Please create bot implementations in the 'bots' directory."
        )
        print("Example bots have been created to help you get started.")
        return None


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "tournament":
            games = 100
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                games = int(sys.argv[2])
            run_tournament(games)
        elif command == "help":
            print("Usage:")
            print(
                "  python example_run.py tournament [games] - Run a tournament with all bots"
            )
            print(
                "                                   [games] is optional number of games per match"
            )
            print("  python example_run.py help      - Show this help message")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python example_run.py help' for usage information")
    else:
        # Default: run the tournament
        print("Running a tournament with 10 games per match")
        run_tournament(10)
