# ui/candidate_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from logger_setup import LOGGER
from ui.window_utils import center_toplevel
from validators import validate_candidate_payload

class CandidateManagement:
    def __init__(self, parent, api_client, main_window):
        self.parent = parent
        self.api_client = api_client
        self.main_window = main_window
        self.students = []
        self.positions = []
        self.partylists = []
        self.elections = []
        self.setup_ui()
        self.load_candidates()
    
    def setup_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.parent)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(
            toolbar, text="➕ Add Candidate", command=self.add_candidate,
            bg="#4CAF50", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar, text="🔄 Refresh", command=self.load_candidates,
            bg="#FF9800", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        # Treeview
        columns = ("ID", "Name", "Position", "Partylist", "Election ID")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=20)
        
        widths = [50, 150, 150, 150, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        v_scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Status bar
        self.status_bar = tk.Label(self.parent, text="Ready", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def load_candidates(self):
        """Load candidates from API"""
        self.status_bar.config(text="Loading candidates...")
        
        def load():
            candidates = self.api_client.get_candidates()
            self.parent.after(0, lambda: self.display_candidates(candidates))
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_candidates(self, candidates):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if candidates:
            for candidate in candidates:
                position = candidate.get('position', {})
                if isinstance(position, dict):
                    position = position.get('title', '')
                
                partylist = candidate.get('partylist', {})
                if isinstance(partylist, dict):
                    partylist = partylist.get('name', '')
                
                self.tree.insert('', 'end', values=(
                    candidate.get('id', ''),
                    self._candidate_name(candidate),
                    position,
                    partylist,
                    candidate.get('election', '')
                ))
            
            self.status_bar.config(text=f"Loaded {len(candidates)} candidates")
        else:
            self.status_bar.config(text="No candidates found")
    
    def add_candidate(self):
        """Add candidate dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Candidate")
        dialog.geometry("400x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        center_toplevel(dialog, self.parent)
        
        fields = {}
        
        # Student
        tk.Label(dialog, text="Student:", font=("Arial", 10)).pack(pady=(10, 0))
        student_combo = ttk.Combobox(dialog, width=37, state="readonly")
        student_combo.pack(pady=5)
        fields['student_id'] = student_combo

        # Description
        tk.Label(dialog, text="Description:", font=("Arial", 10)).pack(pady=(10, 0))
        desc_text = tk.Text(dialog, height=4, width=40)
        desc_text.pack(pady=5)
        fields['description'] = desc_text

        # Link
        tk.Label(dialog, text="Link:", font=("Arial", 10)).pack(pady=(10, 0))
        link_entry = tk.Entry(dialog, width=40)
        link_entry.pack(pady=5)
        fields['link'] = link_entry
        
        # Position
        tk.Label(dialog, text="Position:", font=("Arial", 10)).pack(pady=(10, 0))
        position_combo = ttk.Combobox(dialog, width=37, state="readonly")
        position_combo.pack(pady=5)
        fields['position'] = position_combo
        
        # Partylist
        tk.Label(dialog, text="Partylist:", font=("Arial", 10)).pack(pady=(10, 0))
        partylist_combo = ttk.Combobox(dialog, width=37, state="readonly")
        partylist_combo.pack(pady=5)
        fields['partylist'] = partylist_combo
        
        # Election
        tk.Label(dialog, text="Election:", font=("Arial", 10)).pack(pady=(10, 0))
        election_combo = ttk.Combobox(dialog, width=37, state="readonly")
        election_combo.pack(pady=5)
        fields['election'] = election_combo
        
        # Load data
        def load_data():
            students = self.api_client.get_students() or []
            positions = self.api_client.get_positions() or []
            partylists = self.api_client.get_partylists() or []
            elections = self.api_client.get_elections() or []

            self.students = students
            self.positions = positions
            self.partylists = partylists
            self.elections = elections

            def apply_values():
                student_combo['values'] = [
                    f"{student.get('id')} - {student.get('student_school_id')} - {student.get('first_name')} {student.get('last_name')}"
                    for student in students
                ]
                position_combo['values'] = [
                    f"{position.get('id')} - {position.get('title', '')}"
                    for position in positions
                ]
                partylist_combo['values'] = [
                    f"{partylist.get('id')} - {partylist.get('name', '')}"
                    for partylist in partylists
                ]
                election_combo['values'] = [
                    f"{election.get('id', '')} - {election.get('title', '')}"
                    for election in elections
                ]

            self.parent.after(0, apply_values)
        
        threading.Thread(target=load_data, daemon=True).start()
        
        def save():
            data = {
                'student_id': self._extract_id(fields['student_id'].get()),
                'description': fields['description'].get('1.0', 'end-1c'),
                'link': fields['link'].get().strip(),
                'position': self._extract_id(fields['position'].get()),
                'partylist': self._extract_id(fields['partylist'].get()),
                'election': self._extract_id(fields['election'].get()),
            }

            if not data['partylist']:
                data['partylist'] = None

            validation_error = validate_candidate_payload(data)
            if validation_error:
                messagebox.showerror("Error", validation_error)
                return
            
            self.status_bar.config(text="Adding candidate...")
            
            def add():
                result = self.api_client.create_candidate(data)
                self.parent.after(0, lambda: self.on_add_complete(result, dialog, data))
            
            threading.Thread(target=add, daemon=True).start()
        
        tk.Button(
            dialog, text="Add Candidate", command=save,
            bg="#4CAF50", fg="white", padx=20, pady=10, font=("Arial", 10, "bold")
        ).pack(pady=20)
    
    def on_add_complete(self, result, dialog, data):
        if result:
            LOGGER.info(
                "Candidate synced user=%s student_id=%s election=%s candidate_id=%s",
                self.api_client.current_user,
                data.get('student_id'),
                data.get('election'),
                result.get('id'),
            )
            messagebox.showinfo("Success", "Candidate added successfully!")
            dialog.destroy()
            self.load_candidates()
        else:
            LOGGER.error(
                "Candidate sync failed user=%s student_id=%s election=%s",
                self.api_client.current_user,
                data.get('student_id'),
                data.get('election'),
            )
            self.status_bar.config(text="Failed to add candidate")
            messagebox.showerror("Error", "Failed to add candidate")

    def _extract_id(self, value):
        if not value:
            return None
        return int(value.split(' - ')[0].strip())

    def _candidate_name(self, candidate):
        student = candidate.get('student_id')
        if isinstance(student, dict):
            first_name = student.get('first_name', '')
            last_name = student.get('last_name', '')
            full_name = f"{first_name} {last_name}".strip()
            if full_name:
                return full_name
            return student.get('student_school_id', '')
        return candidate.get('name', '') or str(student or '')
