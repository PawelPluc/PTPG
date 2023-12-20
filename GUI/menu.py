import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font

# import other necessary modules
from logic.figure import Figure
from logic.data_importer import Data_import
# import GUI.plotting.figure as fig_plot 
# from GUI.plotting import cross_section


class Program():
    def __init__(self):
        self.run = True
        self.figure_loaded = False
        self.figure = None
        self.data_loaded = False
        self.data = None
        self.root = tk.Tk()
        self.root.title("Structure Analysis")
        self.root.geometry("400x400")
        self.root.configure(bg='#333333')  # Dark background for the window

        self.setup_gui()

    def setup_gui(self):
        # Stylish font
        button_font = Font(family="Arial", size=12, weight="bold")

        # Frame for better layout
        frame = tk.Frame(self.root, bg='#333333')
        frame.pack(pady=20)

        # Load figure button with style
        load_button = tk.Button(frame, text="Load Structure", command=self.load_figure,
                                padx=15, pady=10, font=button_font,
                                bg='#4CAF50', fg='white', borderwidth=2, relief="raised")
        load_button.pack(pady=10)

        # Make those buttons appear only after the figure is loaded i.e. self.figure_loaded == True

        # Load potential button 


        # Exit button with style
        exit_button = tk.Button(frame, text="Exit", command=self.terminate_program,
                                padx=15, pady=10, font=button_font,
                                bg='#f44336', fg='white', borderwidth=2, relief="raised")
        exit_button.pack(pady=10)

    def run_program(self):
        print("Program loaded")
        self.root.mainloop()

    def load_figure(self):
        self.figure = Figure()
        try:
            self.figure.create_figure()
        except ValueError as error:
            self.error_message(error)   # Call some GUI display of error message
        else:
            self.figure_loaded = True

    def load_distribution(self):
        self.data = Data_import()
        if not self.data.load_data():
            self.error_message("Distribution data failed to load.")
        else:
            self.data_loaded = True
        
        print(self.data.data)

    def terminate_program(self):
        # Add any cleanup or confirmation here if necessary
        print("Terminating program")
        self.run = False
        self.root.destroy()

    def error_message(self, error):
        """
        Displays a window with an error message. Maybe add some buttons for recovery options idk.
        error - error message
        """
        print(f"A following error has occured:\n{error}")   # Replace print with some window, you can change the error message, but leave the {error} variable inside as this is the info about actual error
