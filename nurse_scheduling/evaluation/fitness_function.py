# evaluation/fitness_function.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constraints.constraints import (
    SHIFT_HOURS, 
    check_max_hours, 
    check_consecutive_shifts, 
    check_rest_period, 
    check_shift_coverage, 
    check_nurse_preferences
)
from evaluation.workload_analysis import calculate_nurse_workload
from models.schedule import Schedule

def evaluate_schedule(schedule: Schedule) -> float:
    """
    Calculates the fitness score of a given schedule.
    Higher score means a better schedule based on fairness, efficiency, and constraint compliance.
    """
    total_score = 0

    # ✅ Count unique assigned shifts
    assigned_shifts = set()
    for shifts in schedule.assignments.values():
        assigned_shifts.update(shifts)

    # ✅ 🔥 Adjusted Unassigned Shift Penalty 🔥
    unassigned_shifts = len(schedule.shifts) - len(assigned_shifts)
    total_score -= unassigned_shifts * 30  # Reduced penalty so evolution is possible

    # ✅ 🔥 Adjusted Constraint Penalties 🔥
    for nurse in schedule.nurses:
        if not check_max_hours(nurse, schedule):
            total_score -= 25  # Less severe penalty
        if not check_consecutive_shifts(nurse, schedule):
            total_score -= 20
        if not check_rest_period(nurse, schedule):
            total_score -= 20  

    # ✅ 🔥 Stronger Shift Coverage Reward 🔥
    if check_shift_coverage(schedule):
        total_score += 200  # Big reward for full shift coverage

    # ✅ 🔥 Nurse Preference Reward 🔥
    for nurse in schedule.nurses:
        for shift in schedule.assignments.get(nurse.nurse_id, []):
            if check_nurse_preferences(nurse, shift):
                total_score += 15  # Increased preference match reward

    # ✅ 🔥 Improved Workload Balancing Reward 🔥
    workload_score = calculate_nurse_workload(schedule)
    total_score += workload_score * 1.5  # Boosted impact of fair workload

    return total_score
