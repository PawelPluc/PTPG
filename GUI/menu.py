import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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

        # Frame for controls
        self.controls_frame = tk.Frame(self.root, padx=5, pady=5, width=200)
        self.controls_frame.pack_propagate(False)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame for plots
        self.plot_frame = tk.Frame(self.root, padx=5, pady=5, bg='#333333')
        self.plot_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        # Stylish font
        button_font = Font(family="Arial", size=12, weight="bold")

        # Frame for better layout
        frame = tk.Frame(self.root, bg='#333333')
        frame.pack(pady=20)

        # Load figure button with style
        load_button = tk.Button(self.controls_frame, text="Load Structure", command=self.load_figure,
                                padx=15, pady=10, font=button_font,
                                bg='#4CAF50', fg='white', borderwidth=2, relief="raised")
        load_button.pack(pady=10)

        self.setup_cross_section_ui()
        # self.cross_section_ui_frame.pack_forget()


        # Exit button with style
        exit_button = tk.Button(self.controls_frame, text="Exit", command=self.terminate_program,
                                padx=15, pady=10, font=button_font,
                                bg='#f44336', fg='white', borderwidth=2, relief="raised")
        exit_button.pack(pady=10)

    def update_cross_section_availability(self):
        if self.figure_loaded:
            self.cross_section_button.pack(pady=10)

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
        except Exception as error:
            self.error_message(error)
        else:
            self.figure_loaded = True
            self.display_plot(fig)
            self.cross_section_ui_frame.pack(side=tk.RIGHT, fill='both', expand=True)  # Adjust packing here



    def load_crosssection(self, point1, point2, point3):
        """
        Creates crosssection and plots it on the screen.
        """

        try:
            if not self.figure_loaded:
                raise ValueError("Trying to display crosssection without a figure!")
            fig = self.figure.plot_cross_section(point1, point2, point3)
        except Exception as error:
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
        # canvas.get_tk_widget().pack(fill='both', expand=True)
        # Add toolbar i.e. save buttons etc.
        tooprimaryar = NavigationToolbar2Tk(canvas, self.plot_frame)
        tooprimaryar.update()

    def setup_cross_section_ui(self):
        self.cross_section_ui_frame = tk.Frame(self.controls_frame)

        self.plane_var = tk.StringVar(value='XY plane')
        possible_crossSections = ['XY plane', 'XZ plane', 'YZ plane', 'diagonal']

        for plane in possible_crossSections:
            radio_button = tk.Radiobutton(self.cross_section_ui_frame, text=plane, variable=self.plane_var, 
                                          value=plane, command=self.on_plane_selected)
            radio_button.pack(anchor=tk.W)

        # Coordinate input frames
        self.coord_frames = {}
        for plane in possible_crossSections:
            frame = tk.Frame(self.cross_section_ui_frame)
            self.coord_frames[plane] = frame
            if plane == 'XY plane':
                tk.Label(frame, text="Z coordinate:").pack(side=tk.LEFT)
                tk.Entry(frame).pack(side=tk.LEFT)
            elif plane == 'XZ plane':
                tk.Label(frame, text="Y coordinate:").pack(side=tk.LEFT)
                tk.Entry(frame).pack(side=tk.LEFT)
            elif plane == 'YZ plane':
                tk.Label(frame, text="X coordinate:").pack(side=tk.LEFT)
                tk.Entry(frame).pack(side=tk.LEFT)
            elif plane == 'diagonal':
                for i in range(3):
                    tk.Label(frame, text=f"Point {i+1} (x, y, z):").pack()
                    tk.Entry(frame).pack()  # X
                    tk.Entry(frame).pack()  # Y
                    tk.Entry(frame).pack()  # Z

        # Confirm button
        self.cross_section_button = tk.Button(self.cross_section_ui_frame, text="Confirm Cross Section", 
                                              command=self.confirm_cross_section)
        self.cross_section_button.pack()

        # Initially call on_plane_selected to set up the correct UI
        self.on_plane_selected()

    def on_plane_selected(self):
        # Hide all frames
        for frame in self.coord_frames.values():
            frame.pack_forget()

        # Show the relevant frame
        selected_plane = self.plane_var.get()
        self.coord_frames[selected_plane].pack()

    def confirm_cross_section(self):
        selected_plane = self.plane_var.get()
        points = []

        if selected_plane == 'diagonal':
            # Extract three points for the diagonal plane
            entries = self.coord_frames[selected_plane].winfo_children()
            for i in range(0, len(entries), 4):  # Assuming each point has 3 entries (x, y, z) and one label
                point = [float(entries[i + 1].get()),  # x
                        float(entries[i + 2].get()),  # y
                        float(entries[i + 3].get())]  # z
                points.append(point)
                print(points)
        else:
            # For XY, XZ, YZ planes, create points based on the single coordinate
            coord_value = float(self.coord_frames[selected_plane].winfo_children()[1].get())
            if selected_plane == 'XY plane':
                # Create points for XY plane at given Z
                z = coord_value
                points = [[0, 0, z], [1, 0, z], [0, 1, z]]
            elif selected_plane == 'XZ plane':
                # Create points for XZ plane at given Y
                y = coord_value
                points = [[0, y, 0], [1, y, 0], [0, y, 1]]
            elif selected_plane == 'YZ plane':
                # Create points for YZ plane at given X
                x = coord_value
                points = [[x, 0, 0], [x, 1, 0], [x, 0, 1]]

        # Now use these points in your load_crosssection function
        try:
            self.load_crosssection(*points)
        except Exception as error:
            self.error_message(str(error))

    def terminate_program(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            print("Terminating program")
            self.root.quit()
            self.root.destroy()
        else:
            print("Exit canceled")

    def error_message(self, error):
        """
        Displays a window with an error message. Maybe add some buttons for recovery options idk.
        error - error message
        """
        print(f"A following error has occured:\n{error}")   
        # TO DO Add some window with error message, you can change the error message, but leave the {error} variable inside as this is the info about actual error
