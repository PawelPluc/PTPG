import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# import other necessary modules
from GUI.plotting.figure import FigurePlot
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
  
        self.root.protocol("WM_DELETE_WINDOW", self.terminate_program)
        # self.root.iconbitmap('logo.ico')
        self.root.minsize(1400, 700)
        # self.root.geometry("400x400")
        # self.root.state('zoomed')
        self.root.configure(bg='#333333')  # Dark background for the window
        # TO DO Experiment with sizes, zooms, colors etc. Most of the possible functions you have here in comments

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



        # Make those elements appear only after the figure is loaded i.e. self.figure_loaded == True
        if self.figure_loaded:

            # TO DO Some space to display the plot using display_figure fun
            # Musisz tu stworzyć self.plot_frame !!!! 
            # W plot_frame pojawią się wykresy, kod już do tego zrobiłem tylko potrzeba tego self.plot_frame

            # Cross section button
            possible_crossSections = ['XY plane', 'XZ plane', 'YZ plane', 'diagonal']
            # TO DO Drop down list to choose plane
            plane = possible_crossSections[3]

            if plane == 'diagonal':
                # TO DO buttons for 3 points, 3 coordinates
    
                point1 = [3, 7, 3]
                point2 = [4, 6, 1]
                point3 = [3.5, 5, 2]

            elif plane == 'XY plane':
                # TO DO Button for z of the plane
                z = 3
            
            elif plane == 'XZ plane':
                # TO DO Button for y of the plane
                y = 3

            elif plane == 'YZ plane':
                # TO DO Button for x of the plane
                x = 3

            # TO DO Some button to generate crossSection
            # Wywołaj nim tę funckję -> self.load_crosssection(point1, point2, point3) dla niediagonalnych plaszczyzn musze pomyslec jak policzyc te 3 punkty


        # Exit button with style
        exit_button = tk.Button(frame, text="Exit", command=self.terminate_program,
                                padx=15, pady=10, font=button_font,
                                bg='#f44336', fg='white', borderwidth=2, relief="raised")
        exit_button.pack(pady=10)

    def run_program(self):
        print("Program loaded")
        self.root.mainloop()

    def load_figure(self):
        """
        Loads the figure and plots it on the screen.
        """
        try:
            self.figure = FigurePlot()
            fig = self.figure.plot()
        except ValueError as error:
            self.error_message(error)
        else:
            self.figure_loaded = True
            self.display_plot(fig)

    def load_crosssection(self, point1, point2, point3):
        """
        Creates crosssection and plots it on the screen.
        """
        # 1
        # point1 = [3, 7, 3]
        # point2 = [4, 6, 1]
        # point3 = [3.5, 5, 2]
        
        # # 2x
        # point1 = [1, 7, 3]
        # point2 = [1, 6, 1]
        # point3 = [1, 6, 2]
        
        # # 2y
        # point1 = [7, 1, 3]
        # point2 = [6, 1, 1]
        # point3 = [6, 1, 2]
        
        # # 2z
        # point1 = [7, 3, 1]
        # point2 = [6, 1, 1]
        # point3 = [6, 2, 1]

        try:
            if not self.figure_loaded:
                raise ValueError("Trying to display crosssection without a figure!")
            fig = self.figure.plot_cross_section(point1, point2, point3)
        except ValueError as error:
            self.error_message(error)   
        else:
            self.display_plot(fig)

    def load_distribution(self):
        """
        Calls the necessary function to load distribution data
        """
        self.data = Data_import()
        if not self.data.load_data():
            self.error_message("Distribution data failed to load.")
        else:
            self.data_loaded = True
        
        print(self.data.data)   # Delete later, leave for now for testing

    def display_plot(self, fig):
        """
        Calls the necessary plotting functions to display figure or/and its crossection on the screen.
        """
        # Clean any previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Plot a new plot
        canvas = FigureCanvasTkAgg(fig, master = self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().place( relwidth = 0.94, relheight = 0.9, relx = 0.03, rely = 0.03)
        # Add toolbar i.e. save buttons etc.
        tooprimaryar = NavigationToolbar2Tk(canvas, self.plot_frame)
        tooprimaryar.update()

    def terminate_program(self):
        # TO DO add a message if user is sure to quit
        print("Terminating program")
        self.run = False
        self.root.quit()
        self.root.destroy()

    def error_message(self, error):
        """
        Displays a window with an error message. Maybe add some buttons for recovery options idk.
        error - error message
        """
        print(f"A following error has occured:\n{error}")   
        # TO DO Add some window with error message, you can change the error message, but leave the {error} variable inside as this is the info about actual error
