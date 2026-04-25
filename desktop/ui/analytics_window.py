# ui/analytics_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ui.window_utils import center_toplevel

class AnalyticsWindow:
    def __init__(self, parent, api_client, mode="stats"):
        self.window = tk.Toplevel(parent)
        self.api_client = api_client
        self.mode = mode
        
        if mode == "stats":
            self.window.title("Voting Statistics")
            self.setup_stats_ui()
        else:
            self.window.title("Election Results")
            self.setup_results_ui()
        
        self.window.geometry("800x600")
        self.window.transient(parent)
        self.window.grab_set()
        center_toplevel(self.window, parent)
    
    def setup_stats_ui(self):
        # Create notebook for different stats
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Overall stats tab
        overall_tab = tk.Frame(notebook)
        notebook.add(overall_tab, text="Overall Statistics")
        
        # Load and display stats
        def load_stats():
            stats = self.api_client.get_statistics()

            def render_stats():
                stats_frame = tk.Frame(overall_tab)
                stats_frame.pack(pady=50)

                stats_data = [
                    ("Total Students", stats.get('total_students', 0)),
                    ("Total Elections", stats.get('total_elections', 0)),
                    ("Total Votes Cast", stats.get('total_votes', 0)),
                    ("Total Candidates", stats.get('total_candidates', 0)),
                    ("Voter Turnout", f"{stats.get('turnout_percentage', 0):.1f}%")
                ]

                for label, value in stats_data:
                    frame = tk.Frame(stats_frame)
                    frame.pack(pady=10)
                    tk.Label(frame, text=f"{label}:", font=("Arial", 12, "bold")).pack(side='left', padx=10)
                    tk.Label(frame, text=str(value), font=("Arial", 12)).pack(side='left')

            self.window.after(0, render_stats)
        
        threading.Thread(target=load_stats, daemon=True).start()
    
    def setup_results_ui(self):
        # Election selector
        selection_frame = tk.Frame(self.window)
        selection_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(selection_frame, text="Select Election:", font=("Arial", 10, "bold")).pack(side='left')
        self.election_combo = ttk.Combobox(selection_frame, width=40)
        self.election_combo.pack(side='left', padx=10)
        
        tk.Button(
            selection_frame, text="Load Results", command=self.load_results,
            bg="#4CAF50", fg="white", padx=15, pady=5
        ).pack(side='left')
        
        # Results display
        self.results_text = tk.Text(self.window, height=25, width=80, font=("Courier", 10))
        self.results_text.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Load elections into combo
        def load_elections():
            elections = self.api_client.get_elections()
            if elections:
                self.election_combo['values'] = [f"{e.get('id', '')} - {e.get('title', '')}" for e in elections]
        
        threading.Thread(target=load_elections, daemon=True).start()
    
    def load_results(self):
        selection = self.election_combo.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select an election")
            return
        
        election_id = selection.split(' - ')[0]
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Loading results...\n")
        
        def load():
            votes = self.api_client.get_votes()
            candidates = self.api_client.get_candidates()
            
            if not votes or not candidates:
                self.window.after(0, lambda: self.results_text.delete(1.0, tk.END))
                self.window.after(0, lambda: self.results_text.insert(tk.END, "No data available"))
                return
            
            # Filter votes for this election
            election_votes = [v for v in votes if v.get('election') == int(election_id)]
            
            # Count votes per candidate
            vote_counts = {}
            for vote in election_votes:
                candidate_id = vote.get('candidate')
                if candidate_id:
                    vote_counts[candidate_id] = vote_counts.get(candidate_id, 0) + 1
            
            # Display results
            self.window.after(0, lambda: self.display_results(vote_counts, candidates, election_votes))
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_results(self, vote_counts, candidates, election_votes):
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "ELECTION RESULTS\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Create candidate name mapping
        candidate_names = {}
        for candidate in candidates:
            candidate_names[candidate.get('id')] = candidate.get('name', 'Unknown')
        
        # Sort by vote count
        sorted_counts = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)
        
        for candidate_id, count in sorted_counts:
            name = candidate_names.get(candidate_id, f"Candidate {candidate_id}")
            self.results_text.insert(tk.END, f"{name:<40} {count} votes\n")
        
        if not sorted_counts:
            self.results_text.insert(tk.END, "No votes cast yet\n")
        
        self.results_text.insert(tk.END, f"\n{'-' * 60}\n")
        self.results_text.insert(tk.END, f"Total Votes Cast: {len(election_votes)}\n")
