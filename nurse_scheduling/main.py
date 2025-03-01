import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
from data_handling.database_setup import setup_database
from scheduling_algorithms.genetic_algorithm import genetic_algorithm
from models.schedule import Schedule
from gui import display_schedule  # Import the GUI function

def main():
    # Step 1: Initialize the database (if not already done)
    print("🚀 Setting up the database...")
    setup_database()

    # Step 2: Run the genetic algorithm
    print("🚀 Running the genetic algorithm...")
    final_schedule = genetic_algorithm()

    # Step 3: Display the final optimized schedule
    if final_schedule:
        print("✅ Genetic Algorithm Finished!")
        print("📅 Final Optimized Schedule:")
        final_schedule.display_schedule()  # Keep CLI output

        # Step 4: Launch GUI to visualize the schedule
        print("🖥️ Launching GUI...")
        display_schedule(final_schedule)  # Show the schedule in a GUI
    else:
        print("❌ Schedule generation failed. Please check for errors.")

if __name__ == "__main__":
    main()
