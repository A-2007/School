# models/schedule.py

from .shift import Shift
from .nurse import Nurse

class Schedule:
    def __init__(self):
        """Initializes the schedule by fetching nurses and shifts from the database."""
        self.nurses = Nurse.fetch_all_nurses()
        self.shifts = Shift.fetch_all_shifts()
        self.all_shifts = set(self.shifts)  # Track all shifts
        self.assignments = {}  # Dictionary to store shift assignments by nurse_id

    def __repr__(self):
        return f"Schedule with {len(self.nurses)} nurses and {len(self.shifts)} shifts"

    def get_unassigned_shifts(self):
        """Returns a list of unassigned shifts."""
        return [shift for shift in self.shifts if shift.assigned_nurse is None]

    def assign_nurse_to_shift(self, shift, nurse):
        """
        Assigns a nurse to a shift if they are available and ensures fairness.
        :param shift: The shift to assign.
        :param nurse: The nurse to assign.
        :return: True if successful, False otherwise.
        """
        if nurse.is_available(shift.date, shift.shift_type):
            shift.assigned_nurse = nurse.nurse_id

            # Ensure assignments dictionary is correctly structured
            if nurse.nurse_id not in self.assignments:
                self.assignments[nurse.nurse_id] = []

            # Add the shift to the nurse's assigned shifts
            self.assignments[nurse.nurse_id].append(shift)
            return True
        return False

    def generate_initial_schedule(self):
        """
        Assigns nurses to shifts fairly while ensuring constraints are met.
        Ensures shifts are evenly distributed among available nurses.
        """
        unassigned_shifts = self.get_unassigned_shifts()
        nurses_sorted = sorted(self.nurses, key=lambda n: len(self.assignments.get(n.nurse_id, [])))

        for shift in unassigned_shifts:
            for nurse in nurses_sorted:
                if self.assign_nurse_to_shift(shift, nurse):
                    nurses_sorted = sorted(self.nurses, key=lambda n: len(self.assignments.get(n.nurse_id, [])))
                    break  # Move to the next shift after assigning one nurse

        # Check if all shifts are assigned
        remaining_unassigned = self.get_unassigned_shifts()
        if remaining_unassigned:
            print(f"⚠️ Warning: {len(remaining_unassigned)} shifts remain unassigned.")

    def display_schedule(self):
        """Prints the final schedule with assigned nurses in a readable format."""
        print("\n📅 Final Schedule:")

        if not self.shifts:
            print("⚠️ No shifts scheduled.")
            return

        for shift in self.shifts:
            assigned_nurse_id = shift.assigned_nurse
            assigned_nurse = next((n for n in self.nurses if n.nurse_id == assigned_nurse_id), None)
            nurse_name = assigned_nurse.name if assigned_nurse else "Unassigned"

            print(f"Shift ID: {shift.shift_id}, Date: {shift.date}, Type: {shift.shift_type}, Assigned Nurse: {nurse_name} (ID: {assigned_nurse_id})")

    def add_shift(self, shift):
        """Adds a new shift to the schedule."""
        self.shifts.append(shift)
        self.all_shifts.add(shift)

    def remove_shift(self, shift):
        """Removes a shift from the schedule and updates assignments."""
        if shift in self.shifts:
            self.shifts.remove(shift)
            self.all_shifts.discard(shift)

        # Remove the shift from the assignments dictionary if assigned
        for nurse_id, assigned_shifts in self.assignments.items():
            if shift in assigned_shifts:
                assigned_shifts.remove(shift)

    def update_schedule_with_ga_results(self, best_solution):
        """Applies the genetic algorithm's optimized nurse assignments to the schedule."""
        for shift, nurse_id in best_solution:
            shift.assigned_nurse = nurse_id  # Update assignments in main schedule

        print("✅ Final schedule updated with optimized assignments.")

# Example usage:
if __name__ == "__main__":
    schedule = Schedule()
    schedule.generate_initial_schedule()
    schedule.display_schedule()
