# ui/student_management.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from utils.csv_handler import CSVHandler
import threading

from validators import validate_student_payload
from ui.window_utils import center_toplevel

class StudentManagement:
    def __init__(self, parent, api_client, main_window):
        self.parent = parent
        self.api_client = api_client
        self.main_window = main_window
        self.setup_ui()
        self.load_students()
    
    def setup_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.parent)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(
            toolbar, text="➕ Add Student", command=self.add_student,
            bg="#4CAF50", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar, text="📥 Import CSV", command=self.import_csv,
            bg="#2196F3", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar, text="🔄 Refresh", command=self.load_students,
            bg="#FF9800", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar, text="🗑️ Delete Selected", command=self.delete_selected,
            bg="#f44336", fg="white", padx=10, pady=5, cursor="hand2"
        ).pack(side='left', padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.parent)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(search_frame, text="🔍 Search:").pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_students())
        
        # Treeview
        columns = ("ID", "Student ID", "First Name", "Last Name", "Course", "Year Level", "Email")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.parent, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click to edit
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_student())
        
        # Status bar
        self.status_bar = tk.Label(self.parent, text="Ready", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def load_students(self):
        """Load students from API"""
        self.status_bar.config(text="Loading students...")
        
        def load():
            students = self.api_client.get_students()
            self.parent.after(0, lambda: self.display_students(students))
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_students(self, students):
        """Display students in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if students:
            for student in students:
                course_name = student.get('course', {})
                if isinstance(course_name, dict):
                    course_name = course_name.get('name', '')
                
                self.tree.insert('', 'end', values=(
                    student.get('id', ''),
                    student.get('student_school_id', ''),
                    student.get('first_name', ''),
                    student.get('last_name', ''),
                    course_name,
                    student.get('year_level', ''),
                    student.get('email', '')
                ))
            
            self.status_bar.config(text=f"Loaded {len(students)} students")
        else:
            self.status_bar.config(text="No students found")
    
    def search_students(self):
        """Search students by name or ID"""
        query = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if (query in str(values[2]).lower() or  # First name
                query in str(values[3]).lower() or  # Last name
                query in str(values[1]).lower()):   # Student ID
                self.tree.selection_set(item)
                self.tree.see(item)
                break
            else:
                self.tree.selection_remove(item)
    
    def add_student(self):
        """Add new student dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Student")
        dialog.geometry("400x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        center_toplevel(dialog, self.parent)
        
        fields = {}
        courses = []
        labels = ["First Name", "Last Name", "Student School ID", "Year Level", "Email"]
        
        for i, label in enumerate(labels):
            tk.Label(dialog, text=label, font=("Arial", 10)).pack(pady=(10, 0))
            entry = tk.Entry(dialog, width=40)
            entry.pack(pady=5)
            fields[label.lower().replace(' ', '_')] = entry
        
        # Course selection
        tk.Label(dialog, text="Course", font=("Arial", 10)).pack(pady=(10, 0))
        course_combo = ttk.Combobox(dialog, width=37)
        course_combo.pack(pady=5)
        
        # Load courses
        def load_courses():
            loaded_courses = self.api_client.get_courses() or []

            def apply_courses():
                nonlocal courses
                courses = loaded_courses
                course_combo['values'] = [
                    f"{course.get('id')} - {course.get('name', '')}"
                    for course in loaded_courses
                ]

            self.parent.after(0, apply_courses)
        
        threading.Thread(target=load_courses, daemon=True).start()
        
        def save():
            data = {
                'first_name': fields['first_name'].get(),
                'last_name': fields['last_name'].get(),
                'student_school_id': fields['student_school_id'].get(),
                'year_level': fields['year_level'].get(),
                'email': fields['email'].get(),
                'course': self._extract_id(course_combo.get())
            }
            
            validation_error = validate_student_payload(data)
            if validation_error:
                messagebox.showerror("Error", validation_error)
                return
            
            self.status_bar.config(text="Adding student...")
            
            def add():
                result = self.api_client.create_student(data)
                self.parent.after(0, lambda: self.on_add_complete(result, dialog))
            
            threading.Thread(target=add, daemon=True).start()
        
        tk.Button(
            dialog, text="Save", command=save,
            bg="#4CAF50", fg="white", padx=20, pady=5
        ).pack(pady=20)

    def _extract_id(self, value):
        if not value:
            return None
        return int(value.split(' - ')[0].strip())
    
    def on_add_complete(self, result, dialog):
        if result:
            messagebox.showinfo("Success", "Student added successfully!")
            dialog.destroy()
            self.load_students()
        else:
            self.status_bar.config(text="Failed to add student")
            messagebox.showerror("Error", "Failed to add student")
    
    def edit_student(self):
        """Edit selected student"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        values = self.tree.item(selection[0], 'values')
        messagebox.showinfo("Info", f"Edit student {values[2]} {values[3]} - Feature coming soon")
    
    def delete_selected(self):
        """Delete selected student"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            values = self.tree.item(selection[0], 'values')
            student_id = values[0]
            
            self.status_bar.config(text="Deleting student...")
            
            def delete():
                result = self.api_client.delete_student(student_id)
                self.parent.after(0, lambda: self.on_delete_complete(result))
            
            threading.Thread(target=delete, daemon=True).start()
    
    def on_delete_complete(self, result):
        if result:
            self.status_bar.config(text="Student deleted successfully")
            self.load_students()
        else:
            self.status_bar.config(text="Failed to delete student")
            messagebox.showerror("Error", "Failed to delete student")
    
    def import_csv(self):
        """Import students from CSV"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if not file_path:
            return
        
        self.status_bar.config(text="Processing CSV file...")
        
        def process():
            success, message, students = CSVHandler.validate_and_parse_csv(file_path)
            
            if not success:
                self.parent.after(0, lambda: messagebox.showerror("Error", message))
                return

            courses = self.api_client.get_courses() or []
            course_lookup = {}
            default_course_id = None
            for course in courses:
                course_id = course.get('id')
                course_name = str(course.get('name', '')).strip().lower()
                if course_id and course_name:
                    course_lookup[course_name] = course_id
                    course_lookup[str(course_id)] = course_id
                    if default_course_id is None:
                        default_course_id = course_id

            imported = 0
            skipped = []

            for index, student in enumerate(students, start=1):
                normalized_student = self._normalize_csv_student(student, index, course_lookup, default_course_id)

                result = self.api_client.create_student(normalized_student)
                if result:
                    imported += 1
                else:
                    skipped.append(
                        f"Row {index}: backend rejected student ID {normalized_student.get('student_school_id', '')}"
                    )

            self.parent.after(0, lambda: self.on_import_complete(imported, len(students), skipped))
        
        threading.Thread(target=process, daemon=True).start()
    
    def on_import_complete(self, imported, total, skipped=None):
        skipped = skipped or []
        self.status_bar.config(text=f"Imported {imported} out of {total} students")
        if skipped:
            skipped_preview = "\n".join(skipped[:5])
            if len(skipped) > 5:
                skipped_preview += f"\n...and {len(skipped) - 5} more"
            messagebox.showinfo(
                "Import Complete",
                f"Successfully imported {imported} out of {total} students.\n\nSkipped rows:\n{skipped_preview}"
            )
        else:
            messagebox.showinfo("Complete", f"Successfully imported {imported} students")
        self.load_students()

    def _normalize_csv_student(self, student, index, course_lookup, default_course_id):
        normalized_student = dict(student)

        student_id = str(normalized_student.get('student_school_id', '')).strip()
        if not student_id:
            timestamp = datetime.now().strftime("%H%M%S")
            student_id = f"CSV{datetime.now().strftime('%Y%m%d')}{timestamp}{index}"

        first_name = str(normalized_student.get('first_name', '')).strip() or "Unknown"
        last_name = str(normalized_student.get('last_name', '')).strip() or f"Student{index}"

        raw_year = str(normalized_student.get('year_level', '')).strip().lower()
        year_map = {
            "1st": "1",
            "2nd": "2",
            "3rd": "3",
            "4th": "4",
            "5th": "5",
            "6th": "6",
            "1st year": "1",
            "2nd year": "2",
            "3rd year": "3",
            "4th year": "4",
            "5th year": "5",
            "6th year": "6",
        }
        year_level = year_map.get(raw_year, raw_year) or "1"

        email = str(normalized_student.get('email', '')).strip()
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            email = f"{student_id.lower()}@desktop.local"

        raw_course = str(normalized_student.get('course', '')).strip()
        course_id = course_lookup.get(raw_course.lower()) or course_lookup.get(raw_course) or default_course_id

        normalized_student = {
            'first_name': first_name,
            'last_name': last_name,
            'student_school_id': student_id,
            'year_level': year_level,
            'email': email,
            'course': course_id,
        }

        validation_error = validate_student_payload(normalized_student)
        if validation_error and default_course_id and normalized_student['course'] is None:
            normalized_student['course'] = default_course_id

        return normalized_student
