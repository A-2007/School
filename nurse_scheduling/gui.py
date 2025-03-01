import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_schedule_to_pdf(schedule):
    """
    Exports the current schedule to a PDF file.
    """
    try:
        pdf_file = "nurse_schedule.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 50, "Nurse Scheduling System - Final Schedule")

        # Table headers
        headers = ["Shift ID", "Date", "Shift Type", "Assigned Nurse"]
        for col, header in enumerate(headers):
            c.drawString(100 + col * 150, height - 100, header)

        # Sort shifts in order (1 to 42)
        all_shifts = []
        for nurse_id, shifts in schedule.assignments.items():
            for shift in shifts:
                all_shifts.append((shift.shift_id, shift.date, shift.shift_type, nurse_id))

        all_shifts.sort(key=lambda x: int(x[0]))  # Sort by Shift ID (1 to 42)

        # Add shift data to the PDF
        y_position = height - 120
        for shift_id, date, shift_type, nurse_id in all_shifts:
            c.drawString(100, y_position, str(shift_id))
            c.drawString(250, y_position, date)
            c.drawString(400, y_position, shift_type)
            c.drawString(550, y_position, f"Nurse {nurse_id}")
            y_position -= 20  # Move to the next row

        c.save()  # Save the PDF
        messagebox.showinfo("Success", f"Schedule exported as {pdf_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export schedule: {str(e)}")

def display_schedule(schedule):
    """
    Displays the final optimized schedule in a scrollable timetable format.
    """

    # Create main window
    root = tk.Tk()
    root.title("Nurse Scheduling - Timetable View")

    # Configure window size
    root.geometry("800x600")

    # Add an opening screen (splash screen)
    splash_frame = tk.Frame(root)
    splash_frame.pack(fill=tk.BOTH, expand=True)

    splash_label = tk.Label(splash_frame, text="Welcome to Nurse Scheduling System", font=("Arial", 18, "bold"))
    splash_label.pack(pady=50)

    def close_splash():
        splash_frame.destroy()
        display_schedule_table()  # Proceed to the main schedule

    # Set splash screen duration (3 seconds)
    root.after(3000, close_splash)

    def display_schedule_table():
        # Create a frame for the table with a scrollbar
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create table headers
        headers = ["Shift ID", "Date", "Shift Type", "Assigned Nurse"]
        for col, header in enumerate(headers):
            ttk.Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), borderwidth=2, relief="solid", padding=5).grid(row=0, column=col, sticky="nsew")

        # Sort shifts in order (1 to 42)
        all_shifts = []
        for nurse_id, shifts in schedule.assignments.items():
            for shift in shifts:
                all_shifts.append((shift.shift_id, shift.date, shift.shift_type, nurse_id))

        all_shifts.sort(key=lambda x: int(x[0]))  # Sort by Shift ID (1 to 42)

        # Add shift data to the table
        for row, (shift_id, date, shift_type, nurse_id) in enumerate(all_shifts, start=1):
            color = "lightgray" if row % 2 == 0 else "white"  # Alternate row colors
            ttk.Label(scrollable_frame, text=shift_id, background=color, padding=5).grid(row=row, column=0)
            ttk.Label(scrollable_frame, text=date, background=color, padding=5).grid(row=row, column=1)
            ttk.Label(scrollable_frame, text=shift_type, background=color, padding=5).grid(row=row, column=2)
            ttk.Label(scrollable_frame, text=f"Nurse {nurse_id}", background=color, padding=5).grid(row=row, column=3)

        # Add "Export to PDF" button
        export_button = ttk.Button(root, text="Export Schedule to PDF", command=lambda: export_schedule_to_pdf(schedule))
        export_button.pack(pady=20)

        # Pack everything
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Start the Tkinter event loop
    root.mainloop()
