# scheduling_algorithms/genetic_algorithm.py

import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scheduling_algorithms.greedy_initialization import greedy_initialization
from evaluation.fitness_function import evaluate_schedule
from constraints.constraints import validate_schedule
from models.shift import Shift
from models.schedule import Schedule

try:
    from data_loader import fetch_nurses, fetch_shifts
except ImportError:
    print("⚠️ WARNING: data_loader module not found. Make sure it exists!")

# Genetic Algorithm Parameters
POPULATION_SIZE = 20
MUTATION_RATE = 0.2
GENERATIONS = 100
FITNESS_THRESHOLD = 500
STAGNANT_LIMIT = 15


def initialize_population():
    """Creates an initial population of schedules using both greedy and random methods."""
    nurses = fetch_nurses()
    shifts = fetch_shifts()
    population = []

    for _ in range(POPULATION_SIZE // 2):
        schedule = Schedule()
        schedule.assignments = greedy_initialization(nurses, shifts)
        population.append(schedule)

    for _ in range(POPULATION_SIZE // 2):
        schedule = Schedule()
        random_schedule = {nurse["nurse_id"]: [] for nurse in nurses}

        for shift in shifts:
            available_nurses = [nurse for nurse in nurses if shift["date"] in nurse["availability"]]
            nurse = random.choice(available_nurses) if available_nurses else random.choice(nurses)

            shift_obj = Shift(shift["shift_id"], shift["date"], shift["shift_type"], nurse["nurse_id"])
            random_schedule[nurse["nurse_id"]].append(shift_obj)

        schedule.assignments = random_schedule
        population.append(schedule)

    return population


def evaluate_population(population):
    """Evaluates each schedule and returns a list of (schedule, fitness score)."""
    return [(schedule, evaluate_schedule(schedule)) for schedule in population]


def selection(population_scores):
    """Selects two parents using tournament selection."""
    tournament_size = 3
    return [
        max(random.sample(population_scores, tournament_size), key=lambda x: x[1])[0]
        for _ in range(2)
    ]


def crossover(parent1, parent2):
    """Creates a child schedule by merging shifts from both parents while ensuring uniqueness."""
    child = Schedule()
    assigned_shifts = set()

    for nurse_id in parent1.assignments:
        child.assignments[nurse_id] = []

    for nurse_id, shifts in parent1.assignments.items():
        for shift in shifts:
            if shift.shift_id not in assigned_shifts:
                child.assignments[nurse_id].append(shift)
                assigned_shifts.add(shift.shift_id)

    for nurse_id, shifts in parent2.assignments.items():
        for shift in shifts:
            if shift.shift_id not in assigned_shifts:
                child.assignments[nurse_id].append(shift)
                assigned_shifts.add(shift.shift_id)

    all_shifts = {shift["shift_id"] for shift in fetch_shifts()}
    missing_shifts = list(all_shifts - assigned_shifts)

    nurse_ids = list(child.assignments.keys())
    for shift_id in missing_shifts:
        shift_data = next(shift for shift in fetch_shifts() if shift["shift_id"] == shift_id)
        random_nurse = random.choice(nurse_ids)
        shift_obj = Shift(shift_data["shift_id"], shift_data["date"], shift_data["shift_type"], random_nurse)
        child.assignments[random_nurse].append(shift_obj)

    return child


def mutate(schedule):
    """Mutates the schedule by swapping shifts between nurses."""
    nurse_list = list(schedule.assignments.keys())

    for _ in range(int(len(nurse_list) * MUTATION_RATE)):
        if len(nurse_list) < 2:
            break

        nurse1, nurse2 = random.sample(nurse_list, 2)

        if schedule.assignments[nurse1] and schedule.assignments[nurse2]:
            shift1 = random.choice(schedule.assignments[nurse1])
            shift2 = random.choice(schedule.assignments[nurse2])

            schedule.assignments[nurse1].remove(shift1)
            schedule.assignments[nurse2].remove(shift2)

            schedule.assignments[nurse1].append(shift2)
            schedule.assignments[nurse2].append(shift1)

    return schedule


def deduplicate_schedule(schedule):
    """Ensures the final schedule has 42 unique shifts."""
    all_shifts = set()
    for nurse_id in schedule.assignments:
        unique_shifts = []
        for shift in schedule.assignments[nurse_id]:
            if shift.shift_id not in all_shifts:
                unique_shifts.append(shift)
                all_shifts.add(shift.shift_id)
        schedule.assignments[nurse_id] = unique_shifts

    return schedule


def genetic_algorithm():
    """Runs the genetic algorithm to find the best nurse schedule."""
    print("🚀 Running Genetic Algorithm...")

    population = initialize_population()
    population_scores = evaluate_population(population)

    best_schedule = None
    best_fitness = float('-inf')
    stagnant_generations = 0

    for generation in range(GENERATIONS):
        print(f"⚡ Generation {generation + 1}/{GENERATIONS}")

        population_scores = evaluate_population(population)

        parent1, parent2 = selection(population_scores)
        child = mutate(crossover(parent1, parent2))

        population_scores.sort(key=lambda x: x[1], reverse=True)
        population_scores[-1] = (child, evaluate_schedule(child))

        population = [schedule for schedule, _ in population_scores]

        current_best_fitness = max(population_scores, key=lambda x: x[1])[1]
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_schedule = max(population_scores, key=lambda x: x[1])[0]
            stagnant_generations = 0
        else:
            stagnant_generations += 1

        print(f"✅ Best Fitness So Far: {best_fitness}")

        if stagnant_generations >= STAGNANT_LIMIT:
            print("🚀 Stopping early: No improvement in recent generations.")
            break

        if best_fitness >= FITNESS_THRESHOLD and generation >= 5:
            print("🚀 Stopping early: Fitness threshold met!")
            break

    best_schedule = deduplicate_schedule(best_schedule)
    return best_schedule


if __name__ == "__main__":
    final_schedule = genetic_algorithm()
    print("✅ Genetic Algorithm Finished!")
    final_schedule.display_schedule()
