import tkinter as tk
from tkinter import ttk
import threading


class ElectionManagement:
    def __init__(self, parent, api_client, main_window):
        self.parent = parent
        self.api_client = api_client
        self.main_window = main_window
        self.setup_ui()
        self.load_elections()

    def setup_ui(self):
        toolbar = tk.Frame(self.parent)
        toolbar.pack(fill='x', padx=5, pady=5)

        tk.Button(
            toolbar, text="Refresh", command=self.load_elections,
            bg="#FF9800", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)

        columns = ("ID", "Title", "Available", "Start", "End")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=170)

        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.status_bar = tk.Label(self.parent, text="Ready", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

    def load_elections(self):
        self.status_bar.config(text="Loading elections...")

        def load():
            elections = self.api_client.get_elections()
            self.parent.after(0, lambda: self.display_elections(elections))

        threading.Thread(target=load, daemon=True).start()

    def display_elections(self, elections):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if elections:
            for election in elections:
                self.tree.insert('', 'end', values=(
                    election.get('id', ''),
                    election.get('title', ''),
                    "Yes" if election.get('available') else "No",
                    str(election.get('start_voting_date', ''))[:19],
                    str(election.get('end_voting_date', ''))[:19],
                ))
            self.status_bar.config(text=f"Loaded {len(elections)} elections")
        else:
            self.status_bar.config(text="No elections found")
