"""
School Management System - GUI
This module contains the graphical user interface for the school management system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Student, Teacher, Staff, Course, Classroom, School


class SchoolManagementGUI:
    """Main GUI class for the School Management System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize school
        self.school = School("My School", "123 Education Street")
        
        # Initialize stats labels list
        self.stat_labels = []
        
        # Setup the GUI
        self.setup_styles()
        self.create_widgets()
        self.load_sample_data()
    
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background="#f0f0f0")
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background="#f0f0f0")
        style.configure('TNotebook', tabposition='n')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        style.configure('Treeview', font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x")
        
        title_label = tk.Label(title_frame, text="🏫 School Management System", 
                               font=("Arial", 24, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_students_tab()
        self.create_teachers_tab()
        self.create_staff_tab()
        self.create_courses_tab()
        self.create_classrooms_tab()
    
    def create_dashboard_tab(self):
        """Create the dashboard tab"""
        dashboard_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Dashboard title
        tk.Label(dashboard_frame, text="School Overview", 
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(dashboard_frame, bg="#f0f0f0")
        stats_frame.pack(pady=20)
        
        # Create stat cards
        self.create_stat_card(stats_frame, "Total Students", "👨‍🎓", "0", 0, 0)
        self.create_stat_card(stats_frame, "Total Teachers", "👨‍🏫", "0", 0, 1)
        self.create_stat_card(stats_frame, "Total Staff", "👥", "0", 0, 2)
        self.create_stat_card(stats_frame, "Total Courses", "📚", "0", 0, 3)
        
        # Recent activity frame
        activity_frame = tk.LabelFrame(dashboard_frame, text="Quick Actions", 
                                       font=("Arial", 12, "bold"), bg="#f0f0f0")
        activity_frame.pack(pady=20, padx=20, fill="x")
        
        # Quick action buttons
        btn_frame = tk.Frame(activity_frame, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="➕ Add Student", font=("Arial", 12), 
                 bg="#3498db", fg="white", width=15, command=self.show_add_student).pack(side="left", padx=10)
        tk.Button(btn_frame, text="➕ Add Teacher", font=("Arial", 12), 
                 bg="#2ecc71", fg="white", width=15, command=self.show_add_teacher).pack(side="left", padx=10)
        tk.Button(btn_frame, text="➕ Add Course", font=("Arial", 12), 
                 bg="#9b59b6", fg="white", width=15, command=self.show_add_course).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🔄 Refresh", font=("Arial", 12), 
                 bg="#e74c3c", fg="white", width=15, command=self.refresh_dashboard).pack(side="left", padx=10)
        
        # Store stat labels for updating
        self.stat_labels = []
    
    def create_stat_card(self, parent, title, icon, value, row, col):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="white", relief="raised", bd=2)
        card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        
        tk.Label(card, text=icon, font=("Arial", 30), bg="white").pack(pady=(15, 5))
        tk.Label(card, text=title, font=("Arial", 12), bg="white").pack()
        value_label = tk.Label(card, text=value, font=("Arial", 24, "bold"), bg="white", fg="#2c3e50")
        value_label.pack(pady=(5, 15))
        
        self.stat_labels.append(value_label)
    
    def create_students_tab(self):
        """Create the students management tab"""
        students_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(students_frame, text="👨‍🎓 Students")
        
        # Toolbar
        toolbar = tk.Frame(students_frame, bg="#3498db", height=50)
        toolbar.pack(fill="x")
        
        tk.Label(toolbar, text="Students Management", font=("Arial", 14, "bold"), 
                bg="#3498db", fg="white").pack(side="left", padx=10)
        
        tk.Button(toolbar, text="➕ Add Student", font=("Arial", 10), 
                 bg="white", fg="#3498db", command=self.show_add_student).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Edit Student", font=("Arial", 10), 
                 bg="white", fg="#3498db", command=self.edit_student).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Delete Student", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.delete_student).pack(side="right", padx=5, pady=8)
        
        # Main content
        content = tk.Frame(students_frame, bg="#f0f0f0")
        content.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Name", "Email", "Phone", "Grade", "Courses", "GPA")
        self.students_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
    
    def create_teachers_tab(self):
        """Create the teachers management tab"""
        teachers_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(teachers_frame, text="👨‍🏫 Teachers")
        
        # Toolbar
        toolbar = tk.Frame(teachers_frame, bg="#2ecc71", height=50)
        toolbar.pack(fill="x")
        
        tk.Label(toolbar, text="Teachers Management", font=("Arial", 14, "bold"), 
                bg="#2ecc71", fg="white").pack(side="left", padx=10)
        
        tk.Button(toolbar, text="➕ Add Teacher", font=("Arial", 10), 
                 bg="white", fg="#2ecc71", command=self.show_add_teacher).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Edit Teacher", font=("Arial", 10), 
                 bg="white", fg="#2ecc71", command=self.edit_teacher).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Delete Teacher", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.delete_teacher).pack(side="right", padx=5, pady=8)
        
        # Main content
        content = tk.Frame(teachers_frame, bg="#f0f0f0")
        content.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Name", "Email", "Phone", "Subject", "Salary", "Courses")
        self.teachers_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.teachers_tree.heading(col, text=col)
            self.teachers_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.teachers_tree.yview)
        self.teachers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.teachers_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
    
    def create_staff_tab(self):
        """Create the staff management tab"""
        staff_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(staff_frame, text="👥 Staff")
        
        # Toolbar
        toolbar = tk.Frame(staff_frame, bg="#9b59b6", height=50)
        toolbar.pack(fill="x")
        
        tk.Label(toolbar, text="Staff Management", font=("Arial", 14, "bold"), 
                bg="#9b59b6", fg="white").pack(side="left", padx=10)
        
        tk.Button(toolbar, text="➕ Add Staff", font=("Arial", 10), 
                 bg="white", fg="#9b59b6", command=self.show_add_staff).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Edit Staff", font=("Arial", 10), 
                 bg="white", fg="#9b59b6", command=self.edit_staff).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Delete Staff", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.delete_staff).pack(side="right", padx=5, pady=8)
        
        # Main content
        content = tk.Frame(staff_frame, bg="#f0f0f0")
        content.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Name", "Email", "Phone", "Department", "Position", "Salary")
        self.staff_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.staff_tree.yview)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)
        
        self.staff_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
    
    def create_courses_tab(self):
        """Create the courses management tab"""
        courses_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(courses_frame, text="📚 Courses")
        
        # Toolbar
        toolbar = tk.Frame(courses_frame, bg="#e74c3c", height=50)
        toolbar.pack(fill="x")
        
        tk.Label(toolbar, text="Courses Management", font=("Arial", 14, "bold"), 
                bg="#e74c3c", fg="white").pack(side="left", padx=10)
        
        tk.Button(toolbar, text="➕ Add Course", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.show_add_course).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Edit Course", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.edit_course).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Delete Course", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.delete_course).pack(side="right", padx=5, pady=8)
        
        # Main content
        content = tk.Frame(courses_frame, bg="#f0f0f0")
        content.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Name", "Code", "Description", "Credits", "Teacher", "Students")
        self.courses_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.courses_tree.heading(col, text=col)
            self.courses_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.courses_tree.yview)
        self.courses_tree.configure(yscrollcommand=scrollbar.set)
        
        self.courses_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
    
    def create_classrooms_tab(self):
        """Create the classrooms management tab"""
        classrooms_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(classrooms_frame, text="🏫 Classrooms")
        
        # Toolbar
        toolbar = tk.Frame(classrooms_frame, bg="#f39c12", height=50)
        toolbar.pack(fill="x")
        
        tk.Label(toolbar, text="Classrooms Management", font=("Arial", 14, "bold"), 
                bg="#f39c12", fg="white").pack(side="left", padx=10)
        
        tk.Button(toolbar, text="➕ Add Classroom", font=("Arial", 10), 
                 bg="white", fg="#f39c12", command=self.show_add_classroom).pack(side="right", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Delete Classroom", font=("Arial", 10), 
                 bg="white", fg="#e74c3c", command=self.delete_classroom).pack(side="right", padx=5, pady=8)
        
        # Main content
        content = tk.Frame(classrooms_frame, bg="#f0f0f0")
        content.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Room", "Building", "Capacity", "Schedule")
        self.classrooms_tree = ttk.Treeview(content, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.classrooms_tree.heading(col, text=col)
            self.classrooms_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.classrooms_tree.yview)
        self.classrooms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.classrooms_tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
    
    # CRUD operations for students
    def show_add_student(self):
        """Show dialog to add a new student"""
        self.show_entity_form("Add Student", Student, self.add_student_to_school)
    
    def add_student_to_school(self, data):
        """Add a student to the school"""
        student = Student(**data)
        self.school.add_student(student)
        self.refresh_all_tabs()
        messagebox.showinfo("Success", f"Student {student.name} added successfully!")
    
    def edit_student(self):
        """Edit selected student"""
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        item = self.students_tree.item(selected[0])
        student_id = item['values'][0]
        student = self.school.get_student(student_id)
        
        if student:
            self.show_entity_form("Edit Student", Student, 
                                 lambda data: self.update_student(student, data),
                                 existing_data={
                                     'name': student.name,
                                     'email': student.email,
                                     'phone': student.phone,
                                     'address': student.address,
                                     'grade': student.grade,
                                     'enrollment_date': student.enrollment_date
                                 })
    
    def update_student(self, student, data):
        """Update student information"""
        student.update_info(**{k: v for k, v in data.items() if k not in ['grade', 'enrollment_date']})
        if 'grade' in data:
            student.grade = data['grade']
        self.refresh_all_tabs()
        messagebox.showinfo("Success", "Student updated successfully!")
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        item = self.students_tree.item(selected[0])
        student_id = item['values'][0]
        student = self.school.get_student(student_id)
        
        if student:
            confirm = messagebox.askyesno("Confirm", f"Delete student {student.name}?")
            if confirm:
                self.school.remove_student(student_id)
                self.refresh_all_tabs()
                messagebox.showinfo("Success", "Student deleted successfully!")
    
    # CRUD operations for teachers
    def show_add_teacher(self):
        """Show dialog to add a new teacher"""
        self.show_entity_form("Add Teacher", Teacher, self.add_teacher_to_school)
    
    def add_teacher_to_school(self, data):
        """Add a teacher to the school"""
        teacher = Teacher(**data)
        self.school.add_teacher(teacher)
        self.refresh_all_tabs()
        messagebox.showinfo("Success", f"Teacher {teacher.name} added successfully!")
    
    def edit_teacher(self):
        """Edit selected teacher"""
        selected = self.teachers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a teacher to edit")
            return
        
        item = self.teachers_tree.item(selected[0])
        teacher_id = item['values'][0]
        teacher = self.school.get_teacher(teacher_id)
        
        if teacher:
            self.show_entity_form("Edit Teacher", Teacher,
                                 lambda data: self.update_teacher(teacher, data),
                                 existing_data={
                                     'name': teacher.name,
                                     'email': teacher.email,
                                     'phone': teacher.phone,
                                     'address': teacher.address,
                                     'subject': teacher.subject,
                                     'salary': str(teacher.salary)
                                 })
    
    def update_teacher(self, teacher, data):
        """Update teacher information"""
        teacher.update_info(**{k: v for k, v in data.items() if k not in ['subject', 'salary']})
        if 'subject' in data:
            teacher.subject = data['subject']
        if 'salary' in data:
            teacher.salary = float(data['salary'])
        self.refresh_all_tabs()
        messagebox.showinfo("Success", "Teacher updated successfully!")
    
    def delete_teacher(self):
        """Delete selected teacher"""
        selected = self.teachers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a teacher to delete")
            return
        
        item = self.teachers_tree.item(selected[0])
        teacher_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Delete this teacher?")
        if confirm:
            self.school.remove_teacher(teacher_id)
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Teacher deleted successfully!")
    
    # CRUD operations for staff
    def show_add_staff(self):
        """Show dialog to add a new staff member"""
        self.show_entity_form("Add Staff", Staff, self.add_staff_to_school)
    
    def add_staff_to_school(self, data):
        """Add a staff member to the school"""
        staff = Staff(**data)
        self.school.add_staff(staff)
        self.refresh_all_tabs()
        messagebox.showinfo("Success", f"Staff {staff.name} added successfully!")
    
    def edit_staff(self):
        """Edit selected staff"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to edit")
            return
        
        item = self.staff_tree.item(selected[0])
        staff_id = item['values'][0]
        
        self.show_entity_form("Edit Staff", Staff,
                             lambda data: self.update_staff(staff_id, data),
                             existing_data={
                                 'name': 'Sample',
                                 'email': 'sample@school.com',
                                 'phone': '1234567890',
                                 'address': '123 School St',
                                 'department': 'Administration',
                                 'position': 'Secretary',
                                 'salary': '30000'
                             })
    
    def update_staff(self, staff_id, data):
        """Update staff information"""
        staff = next((s for s in self.school.staff if s.id == staff_id), None)
        if staff:
            staff.update_info(**{k: v for k, v in data.items() 
                               if k not in ['department', 'position', 'salary']})
            if 'department' in data:
                staff.department = data['department']
            if 'position' in data:
                staff.position = data['position']
            if 'salary' in data:
                staff.salary = float(data['salary'])
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Staff updated successfully!")
    
    def delete_staff(self):
        """Delete selected staff"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return
        
        item = self.staff_tree.item(selected[0])
        staff_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Delete this staff member?")
        if confirm:
            self.school.remove_staff(staff_id)
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Staff deleted successfully!")
    
    # CRUD operations for courses
    def show_add_course(self):
        """Show dialog to add a new course"""
        self.show_course_form()
    
    def show_course_form(self):
        """Show form for adding/editing courses"""
        form = tk.Toplevel(self.root)
        form.title("Add Course")
        form.geometry("500x400")
        form.configure(bg="#f0f0f0")
        
        fields = [
            ("Name:", "name", "text"),
            ("Code:", "code", "text"),
            ("Description:", "description", "text"),
            ("Credits:", "credits", "text")
        ]
        
        entries = {}
        for i, (label, field_name, field_type) in enumerate(fields):
            tk.Label(form, text=label, font=("Arial", 11), bg="#f0f0f0").grid(row=i, column=0, padx=10, pady=8, sticky="w")
            entry = tk.Entry(form, font=("Arial", 11))
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
            entries[field_name] = entry
        
        # Teacher selection
        tk.Label(form, text="Teacher:", font=("Arial", 11), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=8, sticky="w")
        teacher_var = tk.StringVar()
        teacher_combo = ttk.Combobox(form, textvariable=teacher_var, font=("Arial", 11))
        teacher_combo['values'] = [t.name for t in self.school.teachers]
        teacher_combo.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        
        def submit():
            data = {field: entry.get() for field, entry in entries.items()}
            data['credits'] = int(data.get('credits', 0))
            
            # Find selected teacher
            selected_teacher = None
            for teacher in self.school.teachers:
                if teacher.name == teacher_var.get():
                    selected_teacher = teacher
                    break
            
            course = Course(**data, teacher=selected_teacher)
            if selected_teacher:
                selected_teacher.add_course(course)
            
            self.school.add_course(course)
            self.refresh_all_tabs()
            form.destroy()
            messagebox.showinfo("Success", f"Course {course.name} added successfully!")
        
        tk.Button(form, text="Add Course", font=("Arial", 12), bg="#2ecc71", fg="white",
                 command=submit).grid(row=5, column=0, columnspan=2, pady=20)
        
        form.grid_columnconfigure(1, weight=1)
    
    def edit_course(self):
        """Edit selected course"""
        messagebox.showinfo("Info", "Course editing feature - implement based on requirements")
    
    def delete_course(self):
        """Delete selected course"""
        selected = self.courses_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to delete")
            return
        
        item = self.courses_tree.item(selected[0])
        course_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Delete this course?")
        if confirm:
            self.school.remove_course(course_id)
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Course deleted successfully!")
    
    # CRUD operations for classrooms
    def show_add_classroom(self):
        """Show dialog to add a new classroom"""
        self.show_entity_form("Add Classroom", Classroom, self.add_classroom_to_school)
    
    def add_classroom_to_school(self, data):
        """Add a classroom to the school"""
        classroom = Classroom(**data)
        self.school.add_classroom(classroom)
        self.refresh_all_tabs()
        messagebox.showinfo("Success", f"Classroom {classroom.room_number} added successfully!")
    
    def delete_classroom(self):
        """Delete selected classroom"""
        selected = self.classrooms_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a classroom to delete")
            return
        
        item = self.classrooms_tree.item(selected[0])
        classroom_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Delete this classroom?")
        if confirm:
            self.school.classrooms = [c for c in self.school.classrooms if c.id != classroom_id]
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Classroom deleted successfully!")
    
    def show_entity_form(self, title, entity_class, submit_callback, existing_data=None):
        """Generic form for adding/editing entities"""
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("450x500")
        form.configure(bg="#f0f0f0")
        
        # Define fields based on entity class
        if entity_class == Student:
            fields = [
                ("Name:", "name"),
                ("Email:", "email"),
                ("Phone:", "phone"),
                ("Address:", "address"),
                ("Grade:", "grade"),
                ("Enrollment Date:", "enrollment_date")
            ]
        elif entity_class == Teacher:
            fields = [
                ("Name:", "name"),
                ("Email:", "email"),
                ("Phone:", "phone"),
                ("Address:", "address"),
                ("Subject:", "subject"),
                ("Salary:", "salary")
            ]
        elif entity_class == Staff:
            fields = [
                ("Name:", "name"),
                ("Email:", "email"),
                ("Phone:", "phone"),
                ("Address:", "address"),
                ("Department:", "department"),
                ("Position:", "position"),
                ("Salary:", "salary")
            ]
        elif entity_class == Classroom:
            fields = [
                ("Room Number:", "room_number"),
                ("Capacity:", "capacity"),
                ("Building:", "building")
            ]
        else:
            fields = []
        
        entries = {}
        for i, (label, field_name) in enumerate(fields):
            tk.Label(form, text=label, font=("Arial", 11), bg="#f0f0f0").grid(row=i, column=0, padx=10, pady=8, sticky="w")
            entry = tk.Entry(form, font=("Arial", 11))
            if existing_data and field_name in existing_data:
                entry.insert(0, existing_data[field_name])
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
            entries[field_name] = entry
        
        def submit():
            data = {}
            for field_name, entry in entries.items():
                value = entry.get()
                if field_name in ['salary', 'capacity']:
                    value = float(value) if '.' in value else int(value)
                data[field_name] = value
            submit_callback(data)
            form.destroy()
        
        tk.Button(form, text="Submit", font=("Arial", 12), bg="#2ecc71", fg="white",
                 command=submit).grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        form.grid_columnconfigure(1, weight=1)
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        if self.stat_labels:
            self.stat_labels[0].config(text=str(self.school.get_total_students()))
            self.stat_labels[1].config(text=str(self.school.get_total_teachers()))
            self.stat_labels[2].config(text=str(self.school.get_total_staff()))
            self.stat_labels[3].config(text=str(self.school.get_total_courses()))
    
    def refresh_all_tabs(self):
        """Refresh all tabs with current data"""
        # Refresh dashboard
        self.refresh_dashboard()
        
        # Refresh students
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        for student in self.school.get_all_students():
            courses = ", ".join([c.name for c in student.courses])
            self.students_tree.insert("", "end", values=(
                student.id, student.name, student.email, student.phone,
                student.grade, courses, student.get_gpa()
            ))
        
        # Refresh teachers
        for item in self.teachers_tree.get_children():
            self.teachers_tree.delete(item)
        for teacher in self.school.get_all_teachers():
            courses = ", ".join([c.name for c in teacher.courses])
            self.teachers_tree.insert("", "end", values=(
                teacher.id, teacher.name, teacher.email, teacher.phone,
                teacher.subject, teacher.salary, courses
            ))
        
        # Refresh staff
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
        for staff in self.school.get_all_staff():
            self.staff_tree.insert("", "end", values=(
                staff.id, staff.name, staff.email, staff.phone,
                staff.department, staff.position, staff.salary
            ))
        
        # Refresh courses
        for item in self.courses_tree.get_children():
            self.courses_tree.delete(item)
        for course in self.school.get_all_courses():
            self.courses_tree.insert("", "end", values=(
                course.id, course.name, course.code, course.description,
                course.credits, course.teacher.name if course.teacher else "TBD",
                course.get_student_count()
            ))
        
        # Refresh classrooms
        for item in self.classrooms_tree.get_children():
            self.classrooms_tree.delete(item)
        for classroom in self.school.get_all_classrooms():
            schedule = ", ".join([f"{s['course'].name} ({s['time_slot']})" for s in classroom.schedule])
            self.classrooms_tree.insert("", "end", values=(
                classroom.id, classroom.room_number, classroom.building,
                classroom.capacity, schedule if schedule else "No classes"
            ))
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Sample students
        students = [
            Student("John Doe", "john@school.com", "555-0101", "123 Main St", "10A", "2024-01-15"),
            Student("Jane Smith", "jane@school.com", "555-0102", "456 Oak Ave", "10A", "2024-01-15"),
            Student("Bob Johnson", "bob@school.com", "555-0103", "789 Pine Rd", "11B", "2023-09-01"),
            Student("Alice Brown", "alice@school.com", "555-0104", "321 Elm St", "10A", "2024-01-15"),
            Student("Charlie Wilson", "charlie@school.com", "555-0105", "654 Maple Dr", "12C", "2022-09-01")
        ]
        
        for student in students:
            self.school.add_student(student)
        
        # Sample teachers
        teachers = [
            Teacher("Dr. Emily White", "emily@school.com", "555-0201", "111 Teacher Ln", "Mathematics", 60000),
            Teacher("Prof. Michael Brown", "michael@school.com", "555-0202", "222 Professor St", "Physics", 65000),
            Teacher("Ms. Sarah Davis", "sarah@school.com", "555-0203", "333 Educator Ave", "English", 55000),
            Teacher("Mr. James Miller", "james@school.com", "555-0204", "444 Instructor Rd", "History", 58000)
        ]
        
        for teacher in teachers:
            self.school.add_teacher(teacher)
        
        # Sample staff
        staff_members = [
            Staff("Mrs. Barbara Wilson", "barbara@school.com", "555-0301", "555 Admin Blvd", 
                 "Administration", "Principal", 80000),
            Staff("Mr. Robert Taylor", "robert@school.com", "555-0302", "666 Office Park", 
                 "Administration", "Vice Principal", 70000),
            Staff("Ms. Patricia Moore", "patricia@school.com", "555-0303", "777 Support St", 
                 "Support", "Secretary", 40000)
        ]
        
        for staff in staff_members:
            self.school.add_staff(staff)
        
        # Sample courses
        courses = [
            Course("Mathematics 101", "MATH101", "Basic Mathematics", 3, teachers[0]),
            Course("Physics 101", "PHYS101", "Introduction to Physics", 4, teachers[1]),
            Course("English Literature", "ENG201", "English Literature Basics", 3, teachers[2]),
            Course("World History", "HIST101", "World History Overview", 3, teachers[3])
        ]
        
        for course in courses:
            self.school.add_course(course)
        
        # Sample classrooms
        classrooms = [
            Classroom("101", 30, "Main Building"),
            Classroom("102", 25, "Main Building"),
            Classroom("201", 35, "Science Wing"),
            Classroom("301", 40, "Arts Building")
        ]
        
        for classroom in classrooms:
            self.school.add_classroom(classroom)
        
        # Enroll students in courses
        students[0].add_course(courses[0])
        students[0].add_course(courses[1])
        students[1].add_course(courses[0])
        students[1].add_course(courses[2])
        students[2].add_course(courses[1])
        students[2].add_course(courses[3])
        
        # Set some grades
        students[0].set_grade(courses[0], 'A')
        students[0].set_grade(courses[1], 'B')
        students[1].set_grade(courses[0], 'A')
        students[1].set_grade(courses[2], 'B')
        
        # Refresh all tabs with sample data
        self.refresh_all_tabs()
