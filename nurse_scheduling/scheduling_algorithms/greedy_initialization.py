# scheduling_algorithms/greedy_initialization.py

import random
from datetime import datetime
import sys
import os

# Add the path to the 'data_handling' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_handling')))

# Now you can import fetch_nurses and fetch_shifts
from data_loader import fetch_nurses, fetch_shifts
from models.shift import Shift  # Import the Shift class

# Fetch the data from the database
nurses = fetch_nurses()  # List of nurses from the database
shifts = fetch_shifts()  # List of shifts from the database

def is_day_in_range(day, day_range):
    """
    Checks if a given day falls within a day range (e.g., "Mon-Fri").
    :param day: The day to check (e.g., "2025-02-19").
    :param day_range: The day range (e.g., "Mon-Fri").
    :return: True if the day falls within the range, False otherwise.
    """
    # Convert the day to a weekday (e.g., "Mon")
    weekday = datetime.strptime(day, "%Y-%m-%d").strftime("%a")

    # Handle single day (e.g., "Mon")
    if "-" not in day_range:
        return weekday == day_range.strip()

    # Handle day range (e.g., "Mon-Fri")
    start_day, end_day = day_range.split("-")
    start_day = start_day.strip()
    end_day = end_day.strip()

    # Map weekdays to numbers (Mon=0, Tue=1, ..., Sun=6)
    weekday_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    weekday_num = weekday_map.get(weekday, -1)
    start_num = weekday_map.get(start_day, -1)
    end_num = weekday_map.get(end_day, -1)

    if weekday_num == -1 or start_num == -1 or end_num == -1:
        return False

    # Check if the weekday falls within the range
    return start_num <= weekday_num <= end_num

def get_available_shifts_for_day(nurse, day):
    """
    Returns a list of shift types (morning, afternoon, night) available to the nurse for the given day.
    If the nurse is not available on the day, return an empty list.
    """
    available_shifts = []
    availability = nurse['availability']

    # Debugging: Print nurse availability
    print(f"Nurse {nurse['nurse_id']} Availability: {availability}")

    # Parse the availability string to extract available days and shifts
    availability_slots = availability.split(", ")
    for slot in availability_slots:
        # Extract the day range and shift type from the slot
        if "(" in slot and ")" in slot:
            day_range = slot.split("(")[0].strip()  # Extract the day range (e.g., "Mon-Fri")
            shift_type = slot.split("(")[1].replace(")", "").strip()  # Extract the shift type (e.g., "Morning")

            # Check if the shift date falls within the day range
            if is_day_in_range(day, day_range):
                # If the nurse prefers this shift type, add it to available_shifts
                if shift_type in nurse['preferred_shifts']:
                    available_shifts.append(shift_type)

    # Debugging: Print available shifts for the day
    print(f"Nurse {nurse['nurse_id']} Available Shifts on {day}: {available_shifts}")

    return available_shifts

def greedy_initialization(nurses, shifts):
    """
    Performs a greedy initialization of the nurse scheduling by assigning shifts to nurses
    based on their availability and preferences.
    """
    # Initialize the schedule with empty lists for each nurse
    schedule = {nurse["nurse_id"]: [] for nurse in nurses}

    # Sort nurses by the number of preferred shifts (more specific preferences are prioritized)
    nurses_sorted = sorted(nurses, key=lambda nurse: len(nurse['preferred_shifts']), reverse=True)

    # Assign shifts to nurses based on their availability and preferences
    for nurse in nurses_sorted:
        for shift_data in shifts:
            # Get the available shift types for the nurse on this shift date
            available_shifts = get_available_shifts_for_day(nurse, shift_data["date"])

            # Debugging: Print nurse availability and shift data
            print(f"Nurse {nurse['nurse_id']} - Available Shifts on {shift_data['date']}: {available_shifts}")
            print(f"Shift Data: {shift_data}")

            # If the nurse is available and prefers this shift type, assign them the shift
            if shift_data["shift_type"] in available_shifts:
                # Create a Shift object
                shift = Shift(
                    shift_id=shift_data["shift_id"],
                    date=shift_data["date"],
                    shift_type=shift_data["shift_type"],
                    assigned_nurse=nurse["nurse_id"]
                )
                schedule[nurse["nurse_id"]].append(shift)
                print(f"Assigned Shift {shift_data['shift_id']} to Nurse {nurse['nurse_id']}")

    # Fill remaining shifts with any available nurse (if not assigned already)
    for nurse in nurses:
        for shift_data in shifts:
            # Check if the shift is already assigned
            shift_assigned = any(shift_data["shift_id"] == shift.shift_id for shift in schedule[nurse["nurse_id"]])
            if not shift_assigned and shift_data["date"] in nurse["availability"]:
                # Create a Shift object
                shift = Shift(
                    shift_id=shift_data["shift_id"],
                    date=shift_data["date"],
                    shift_type=shift_data["shift_type"],
                    assigned_nurse=nurse["nurse_id"]
                )
                schedule[nurse["nurse_id"]].append(shift)
                print(f"Assigned Shift {shift_data['shift_id']} to Nurse {nurse['nurse_id']} (Fallback)")

    return schedule

# Print the generated schedule for review
def print_schedule(schedule):
    """
    Prints the nurse schedule in a readable format.
    :param schedule: A dictionary containing the nurse schedule (nurse_id -> [Shift objects])
    """
    for nurse_id, shifts in schedule.items():
        nurse_name = next(nurse['name'] for nurse in nurses if nurse['nurse_id'] == nurse_id)
        print(f"{nurse_name} - Assigned Shifts:")
        for shift in shifts:
            print(f"  Shift ID: {shift.shift_id}, Date: {shift.date}, Type: {shift.shift_type}")

if __name__ == "__main__":
    # Generate the schedule using Greedy Initialization
    schedule = greedy_initialization(nurses, shifts)

    # Print the schedule
    print_schedule(schedule)