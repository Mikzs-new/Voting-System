# ui/candidate_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class CandidateManagement:
    def __init__(self, parent, api_client, main_window):
        self.parent = parent
        self.api_client = api_client
        self.main_window = main_window
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
                    candidate.get('name', ''),
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
        
        dialog.eval('tk::PlaceWindow . center')
        
        fields = {}
        
        # Name
        tk.Label(dialog, text="Name:", font=("Arial", 10)).pack(pady=(10, 0))
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        fields['name'] = name_entry
        
        # Description
        tk.Label(dialog, text="Description:", font=("Arial", 10)).pack(pady=(10, 0))
        desc_text = tk.Text(dialog, height=4, width=40)
        desc_text.pack(pady=5)
        fields['description'] = desc_text
        
        # Position
        tk.Label(dialog, text="Position:", font=("Arial", 10)).pack(pady=(10, 0))
        position_combo = ttk.Combobox(dialog, width=37)
        position_combo.pack(pady=5)
        fields['position'] = position_combo
        
        # Partylist
        tk.Label(dialog, text="Partylist:", font=("Arial", 10)).pack(pady=(10, 0))
        partylist_combo = ttk.Combobox(dialog, width=37)
        partylist_combo.pack(pady=5)
        fields['partylist'] = partylist_combo
        
        # Election
        tk.Label(dialog, text="Election:", font=("Arial", 10)).pack(pady=(10, 0))
        election_combo = ttk.Combobox(dialog, width=37)
        election_combo.pack(pady=5)
        fields['election'] = election_combo
        
        # Load data
        def load_data():
            positions = self.api_client.get_positions()
            if positions:
                position_combo['values'] = [p.get('title', '') for p in positions]
            
            partylists = self.api_client.get_partylists()
            if partylists:
                partylist_combo['values'] = [p.get('name', '') for p in partylists]
            
            elections = self.api_client.get_elections()
            if elections:
                election_combo['values'] = [f"{e.get('id', '')} - {e.get('title', '')}" for e in elections]
        
        threading.Thread(target=load_data, daemon=True).start()
        
        def save():
            data = {
                'name': fields['name'].get(),
                'description': fields['description'].get('1.0', 'end-1c'),
                'position': fields['position'].get(),
                'partylist': fields['partylist'].get(),
                'election': fields['election'].get().split(' - ')[0] if fields['election'].get() else None
            }
            
            if not data['name']:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            self.status_bar.config(text="Adding candidate...")
            
            def add():
                result = self.api_client.create_candidate(data)
                self.parent.after(0, lambda: self.onAddComplete(result, dialog))
            
            threading.Thread(target=add, daemon=True).start()
        
        tk.Button(
            dialog, text="Add Candidate", command=save,
            bg="#4CAF50", fg="white", padx=20, pady=10, font=("Arial", 10, "bold")
        ).pack(pady=20)
    
    def onAddComplete(self, result, dialog):
        if result:
            messagebox.showinfo("Success", "Candidate added successfully!")
            dialog.destroy()
            self.load_candidates()
        else:
            self.status_bar.config(text="Failed to add candidate")
            messagebox.showerror("Error", "Failed to add candidate")