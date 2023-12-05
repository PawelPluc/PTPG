from logic.figure import Figure
import GUI.plotting.figure as fig_plot 
from GUI.plotting import cross_section

class Program():

    def __init__(self):
        self.run = True
        self.figure_loaded = False
        self.figure = None

    def run_program(self):
        """
        Used by the main function to start the execution of the program and keeps the program running.
        """
        
        print("Program loaded")

        while(self.run):
            # The program is running, check for inputs i.e. button clicks

            if (True): # TO DO Some button for loading a figure
                self.figure = Figure()
                self.figure.create_figure()
                self.figure_loaded = True

            if (self.figure_loaded): # TO DO if figure is loaded call plotting of a figure and display options for loading distribution data
                pass

            if (True): # TO DO Closing (x) clicked (or some exit button idk)
                self.terminate_program()
        

    def terminate_program(self):
        """
        Should display the prompt asking for closing and finish program execution if yes.
        """
        #prompt

        self.run = False

