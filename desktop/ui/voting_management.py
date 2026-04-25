import tkinter as tk
from tkinter import ttk, messagebox
import threading

from logger_setup import LOGGER
from validators import validate_vote_payload


class VotingManagement:
    def __init__(self, parent, api_client, main_window):
        self.parent = parent
        self.api_client = api_client
        self.main_window = main_window
        self.students = []
        self.elections = []
        self.setup_ui()
        self.load_reference_data()

    def setup_ui(self):
        form = tk.Frame(self.parent)
        form.pack(fill='x', padx=10, pady=10)

        tk.Label(form, text="Student:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.student_combo = ttk.Combobox(form, width=45, state="readonly")
        self.student_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        tk.Label(form, text="Election:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.election_combo = ttk.Combobox(form, width=45, state="readonly")
        self.election_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        tk.Button(
            form, text="Submit Vote", command=self.submit_vote,
            bg="#4CAF50", fg="white", padx=20, pady=8, cursor="hand2"
        ).grid(row=2, column=1, sticky='w', padx=5, pady=10)

        tk.Button(
            form, text="Refresh", command=self.load_reference_data,
            bg="#FF9800", fg="white", padx=20, pady=8, cursor="hand2"
        ).grid(row=2, column=1, sticky='e', padx=5, pady=10)

        form.grid_columnconfigure(1, weight=1)

        columns = ("Vote ID", "Student", "Election", "Timestamp")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.status_bar = tk.Label(self.parent, text="Ready", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

    def load_reference_data(self):
        self.status_bar.config(text="Loading voting data...")

        def load():
            students = self.api_client.get_students() or []
            elections = self.api_client.get_elections() or []
            votes = self.api_client.get_votes() or []
            self.parent.after(0, lambda: self._apply_reference_data(students, elections, votes))

        threading.Thread(target=load, daemon=True).start()

    def _apply_reference_data(self, students, elections, votes):
        self.students = students
        self.elections = elections

        self.student_combo['values'] = [
            f"{student.get('id')} - {student.get('student_school_id')} - {student.get('first_name')} {student.get('last_name')}"
            for student in students
        ]
        self.election_combo['values'] = [
            f"{election.get('id')} - {election.get('title')}"
            for election in elections
        ]

        for item in self.tree.get_children():
            self.tree.delete(item)

        student_map = {
            student.get('id'): f"{student.get('student_school_id')} - {student.get('first_name')} {student.get('last_name')}"
            for student in students
        }
        election_map = {
            election.get('id'): election.get('title', '')
            for election in elections
        }

        for vote in votes:
            self.tree.insert('', 'end', values=(
                vote.get('id', ''),
                student_map.get(vote.get('student_id'), vote.get('student_id', '')),
                election_map.get(vote.get('election'), vote.get('election', '')),
                str(vote.get('datetime', ''))[:19],
            ))

        self.status_bar.config(text="Voting data loaded")

    def submit_vote(self):
        student_selection = self.student_combo.get()
        election_selection = self.election_combo.get()

        student_id = student_selection.split(' - ')[0] if student_selection else ''
        election_id = election_selection.split(' - ')[0] if election_selection else ''

        validation_error = validate_vote_payload(student_id, election_id)
        if validation_error:
            messagebox.showerror("Error", validation_error)
            return

        self.status_bar.config(text="Submitting vote...")

        def create_vote():
            payload = {
                'student_id': int(student_id),
                'election': int(election_id),
            }
            result = self.api_client.create_vote(payload)
            self.parent.after(0, lambda: self._on_vote_complete(result, payload))

        threading.Thread(target=create_vote, daemon=True).start()

    def _on_vote_complete(self, result, payload):
        if result:
            LOGGER.info(
                "Voting action synced user=%s student_id=%s election=%s vote_id=%s",
                self.api_client.current_user,
                payload['student_id'],
                payload['election'],
                result.get('id'),
            )
            messagebox.showinfo("Success", "Vote submitted and synced with backend.")
            self.load_reference_data()
            return

        LOGGER.error(
            "Voting action failed user=%s student_id=%s election=%s",
            self.api_client.current_user,
            payload['student_id'],
            payload['election'],
        )
        self.status_bar.config(text="Failed to submit vote")
        messagebox.showerror("Error", "Vote submission failed.")
