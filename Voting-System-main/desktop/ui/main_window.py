# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox

from ui.analytics_window import AnalyticsWindow
from ui.candidate_management import CandidateManagement
from ui.election_management import ElectionManagement
from ui.student_management import StudentManagement


class MainWindow:
    def __init__(self, root, api_client):
        self.root = root
        self.api_client = api_client
        self.root.title("School Voting System - Staff Desktop")
        self.root.geometry("1280x720")

        self.setup_menu()
        self.setup_ui()
        self.load_dashboard()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh", command=self.refresh_current_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.root.quit)

        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Management", menu=manage_menu)
        manage_menu.add_command(label="Student Management", command=self.show_students)
        manage_menu.add_command(label="Election Management", command=self.show_elections)
        manage_menu.add_command(label="Candidate Management", command=self.show_candidates)
        manage_menu.add_command(label="Position Management", command=self.show_positions)

        analytics_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analytics", menu=analytics_menu)
        analytics_menu.add_command(label="Voting Statistics", command=self.show_statistics)
        analytics_menu.add_command(label="Election Results", command=self.show_results)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.dashboard_tab = tk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")

    def load_dashboard(self):
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(self.dashboard_tab)
        header_frame.pack(fill='x', padx=20, pady=20)

        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome back, {self.api_client.current_user or 'Staff'}!",
            font=("Arial", 18, "bold")
        )
        welcome_label.pack(anchor='w')

        date_label = tk.Label(
            header_frame,
            text=f"Today's Date: {__import__('datetime').datetime.now().strftime('%B %d, %Y')}",
            font=("Arial", 10),
            fg="#666"
        )
        date_label.pack(anchor='w', pady=(5, 0))

        stats_frame = tk.Frame(self.dashboard_tab)
        stats_frame.pack(fill='x', padx=20, pady=20)

        stats = self.api_client.get_statistics()
        cards = [
            ("Total Students", stats.get('total_students', 0), "#4CAF50"),
            ("Total Elections", stats.get('total_elections', 0), "#2196F3"),
            ("Total Votes Cast", stats.get('total_votes', 0), "#FF9800"),
            ("Voter Turnout", f"{stats.get('turnout_percentage', 0):.1f}%", "#9C27B0"),
        ]

        for i, (title, value, color) in enumerate(cards):
            card = tk.Frame(stats_frame, relief='ridge', bd=1, bg='white')
            card.grid(row=0, column=i, padx=10, sticky='nsew')

            tk.Label(card, text=title, font=("Arial", 12), bg='white').pack(pady=(15, 5))
            tk.Label(card, text=str(value), font=("Arial", 28, "bold"), fg=color, bg='white').pack(pady=(0, 15))

            stats_frame.grid_columnconfigure(i, weight=1)

        actions_frame = tk.LabelFrame(self.dashboard_tab, text="Quick Actions", font=("Arial", 12, "bold"))
        actions_frame.pack(fill='x', padx=20, pady=20)

        actions = [
            ("Add Student", self.show_students),
            ("Create Election", self.show_elections),
            ("Add Candidate", self.show_candidates),
            ("View Results", self.show_results),
            ("Sync Data", self.refresh_current_tab),
        ]

        for i, (text, command) in enumerate(actions):
            btn = tk.Button(
                actions_frame,
                text=text,
                command=command,
                bg="#f0f0f0",
                font=("Arial", 10),
                padx=15,
                pady=8,
                cursor="hand2"
            )
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky='ew')
            actions_frame.grid_columnconfigure(i % 3, weight=1)

        recent_frame = tk.LabelFrame(self.dashboard_tab, text="Recent Elections", font=("Arial", 12, "bold"))
        recent_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Title", "Start Date", "End Date", "Status")
        tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=8)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')

        elections = self.api_client.get_elections()
        if elections:
            for election in elections[:5]:
                tree.insert('', 'end', values=(
                    election.get('id', ''),
                    election.get('title', ''),
                    election.get('start_voting_date', '')[:10] if election.get('start_voting_date') else '',
                    election.get('end_voting_date', '')[:10] if election.get('end_voting_date') else '',
                    "Active" if election.get('available') else "Inactive",
                ))

    def show_students(self):
        for i in range(self.notebook.index('end')):
            if self.notebook.tab(i, "text") == "Students":
                self.notebook.select(i)
                return

        student_tab = tk.Frame(self.notebook)
        self.notebook.add(student_tab, text="Students")
        StudentManagement(student_tab, self.api_client, self)
        self.notebook.select(student_tab)

    def show_elections(self):
        for i in range(self.notebook.index('end')):
            if self.notebook.tab(i, "text") == "Elections":
                self.notebook.select(i)
                return

        election_tab = tk.Frame(self.notebook)
        self.notebook.add(election_tab, text="Elections")
        ElectionManagement(election_tab, self.api_client, self)
        self.notebook.select(election_tab)

    def show_candidates(self):
        for i in range(self.notebook.index('end')):
            if self.notebook.tab(i, "text") == "Candidates":
                self.notebook.select(i)
                return

        candidate_tab = tk.Frame(self.notebook)
        self.notebook.add(candidate_tab, text="Candidates")
        CandidateManagement(candidate_tab, self.api_client, self)
        self.notebook.select(candidate_tab)

    def show_positions(self):
        messagebox.showinfo("Info", "Position Management - Coming soon!")

    def show_statistics(self):
        AnalyticsWindow(self.root, self.api_client, "stats")

    def show_results(self):
        AnalyticsWindow(self.root, self.api_client, "results")

    def refresh_current_tab(self):
        current_tab = self.notebook.select()
        if current_tab and self.notebook.tab(current_tab, "text") == "Dashboard":
            self.load_dashboard()

    def show_about(self):
        about_text = """
        School Voting System - Staff Desktop Application
        Version 1.0.0

        A staff and facilitator desktop client for the school voting system.

        Features:
        - Student Management
        - Election Management
        - Candidate Management
        - Real-time Analytics

        © 2024 School Voting System
        """
        messagebox.showinfo("About", about_text)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.api_client.logout()
            self.root.destroy()
            import subprocess
            import sys
            subprocess.Popen([sys.executable, 'main.py'])
            sys.exit()
