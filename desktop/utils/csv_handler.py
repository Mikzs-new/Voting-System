# utils/csv_handler.py
import pandas as pd
import os
from config import ALLOWED_CSV_COLUMNS, MAX_CSV_SIZE

class CSVHandler:
    @staticmethod
    def validate_and_parse_csv(file_path):
        """Validate and parse CSV file"""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > MAX_CSV_SIZE:
                return False, f"File too large. Maximum size: {MAX_CSV_SIZE // (1024*1024)}MB", []
            
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Add missing expected columns so desktop import can use defaults later.
            expected_columns = ALLOWED_CSV_COLUMNS
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""
            
            # Convert to list of dicts
            students = []
            for _, row in df.iterrows():
                student = {
                    'first_name': CSVHandler._clean_value(row.get('first_name', '')),
                    'last_name': CSVHandler._clean_value(row.get('last_name', '')),
                    'student_school_id': CSVHandler._clean_value(row.get('student_id', '')),
                    'year_level': CSVHandler._clean_value(row.get('year', '')),
                    'email': CSVHandler._clean_value(row.get('email', '')),
                    'course': CSVHandler._clean_value(row.get('course', ''))
                }
                students.append(student)
            
            return True, f"Successfully parsed {len(students)} students", students
            
        except Exception as e:
            return False, f"Error parsing CSV: {str(e)}", []

    @staticmethod
    def _clean_value(value):
        if pd.isna(value):
            return ""
        text = str(value).strip()
        if text.lower() == "nan":
            return ""
        return text
