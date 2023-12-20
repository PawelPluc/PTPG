import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from logic.figure import Figure
# import other necessary modules

class Program():
    def __init__(self):
        self.run = True
        self.figure_loaded = False
        self.figure = None
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

        # Load button with style
        load_button = tk.Button(frame, text="Load Structure", command=self.load_figure,
                                padx=15, pady=10, font=button_font,
                                bg='#4CAF50', fg='white', borderwidth=2, relief="raised")
        load_button.pack(pady=10)

        # Exit button with style
        exit_button = tk.Button(frame, text="Exit", command=self.terminate_program,
                                padx=15, pady=10, font=button_font,
                                bg='#f44336', fg='white', borderwidth=2, relief="raised")
        exit_button.pack(pady=10)

    def run_program(self):
        print("Program loaded")
        self.root.mainloop()

    def load_figure(self):
        file_path = filedialog.askopenfilename()  # Open file dialog to choose file
        if file_path:
            self.figure = Figure()  # Assuming Figure() can take a file path as an argument
            self.figure.create_figure(file_path)
            self.figure_loaded = True
            # Call any other methods necessary to process the file

    def terminate_program(self):
        # Add any cleanup or confirmation here if necessary
        self.run = False
        self.root.destroy()

# Rest of your code
def main():
    app = Program()
    app.run_program()

if __name__ == "__main__":
    main()


# from logic.figure import Figure
# import GUI.plotting.figure as fig_plot 
# from GUI.plotting import cross_section

# class Program():

#     def __init__(self):
#         self.run = True
#         self.figure_loaded = False
#         self.figure = None

#     def run_program(self):
#         """
#         Used by the main function to start the execution of the program and keeps the program running.
#         """
        
#         print("Program loaded")

#         while(self.run):
#             # The program is running, check for inputs i.e. button clicks

#             if (True): # TO DO Some button for loading a figure
#                 self.figure = Figure()
#                 self.figure.create_figure()
#                 self.figure_loaded = True

#             if (self.figure_loaded): # TO DO if figure is loaded call plotting of a figure and display options for loading distribution data
#                 pass

#             if (True): # TO DO Closing (x) clicked (or some exit button idk)
#                 self.terminate_program()
        

#     def terminate_program(self):
#         """
#         Should display the prompt asking for closing and finish program execution if yes.
#         """
#         #prompt

#         self.run = False