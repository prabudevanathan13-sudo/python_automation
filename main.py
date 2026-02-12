"""
School Management System - Main Application
This is the entry point for the School Management System application.
"""

import tkinter as tk
from gui import SchoolManagementGUI


def main():
    """Main function to start the School Management System"""
    # Create the main tkinter window
    root = tk.Tk()
    
    # Prevent the window from being too small
    root.minsize(800, 600)
    
    # Center the window on the screen
    window_width = 1200
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    # Create the application
    app = SchoolManagementGUI(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
