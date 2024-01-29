import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math

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
        self.data = []
        self.data_unit = 'V'
        self.root = tk.Tk()
        self.root.title("Structure Analysis")
        self.cross_section_ui_frame = None
  
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

        # self.setup_cross_section_ui()
        # self.cross_section_ui_frame.pack_forget()


        # Exit button with style
        exit_button = tk.Button(self.controls_frame, text="Exit", command=self.terminate_program,
                                padx=15, pady=10, font=button_font,
                                bg='#f44336', fg='white', borderwidth=2, relief="raised")
        exit_button.pack(pady=10)

        self.cross_section_ui_frame = tk.Frame(self.controls_frame)  # Create the frame
        self.cross_section_ui_frame.pack()  # Pack the frame, but it will be empty initially

        self.load_distribution_button = tk.Button(self.controls_frame, text="Load Distribution Data", command=self.load_distribution)


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
            self.error_message("Input data failed to load for the following reason:\n"+str(error))
        else:
            self.figure_loaded = True
            self.figure_symmetry = self.figure.laser_symmetry
            self.clear_and_setup_cross_section_ui()
            self.setup_cross_section_ui()
            self.display_plot(fig)
            # Hide the load distribution button as new structure is loaded
            self.load_distribution_button.pack_forget()

            # Reset data and unit
            self.data = []
            self.data_unit = 'V'
            # self.cross_section_ui_frame.pack(side=tk.RIGHT, fill='both', expand=True)  # Adjust packing here



    def load_crosssection(self, point1, point2, point3):
        """
        Creates crosssection and plots it on the screen.
        """
        try:
            if not self.figure_loaded:
                raise ValueError("Trying to display crosssection without a figure!")
            self.data = []
            self.data_unit = 'V'
            self.current_cross_section_points = (point1, point2, point3)  # Store the current points
            self.reload_cross_section_with_distribution()
            self.load_distribution_button.pack_forget()
            self.load_distribution_button.pack(pady=10)
        except Exception as error:
            self.error_message("Crosssection couldn't be created for the reason below:\n"+str(error))   

    def load_distribution(self):
        """
        Calls the necessary function to load distribution data
        """
        dist = Data_import()
        if not dist.load_data():
            self.error_message("Distribution data failed to load.")
        else:
            self.data_loaded = True
            self.data = dist.data

            if dist.type == 'temperature':
                self.data_unit = "K"
            else:
                self.data_unit = "V"
            self.reload_cross_section_with_distribution()
            
    def reload_cross_section_with_distribution(self):
        """
        Redraws the cross section plot with the distribution data.
        """
        if self.figure_loaded and self.current_cross_section_points:
            point1, point2, point3 = self.current_cross_section_points
            fig = self.figure.plot_cross_section(point1, point2, point3, dist=self.data, unit=self.data_unit)
            self.display_plot(fig)

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
        if self.cross_section_ui_frame is not None:
            for widget in self.cross_section_ui_frame.winfo_children():
                widget.destroy()
        else:
            # If the frame doesn't exist, create it
            self.cross_section_ui_frame = tk.Frame(self.controls_frame)
            self.cross_section_ui_frame.pack()

        # Setup the UI based on the symmetry
        if self.figure_symmetry == 0:  # Cartesian coordinates
            self.setup_cartesian_cross_section_ui()
        elif self.figure_symmetry == 1:  # Cylindrical coordinates
            self.setup_cylindrical_cross_section_ui()

        self.cross_section_ui_frame.pack()

    def setup_cartesian_cross_section_ui(self):
        # laser_symmetry = self.figure.laser_symmetry

        self.cross_section_ui_frame = tk.Frame(self.controls_frame)

        self.cross_section_button = tk.Button(self.cross_section_ui_frame, text="Confirm Cross Section", 
                                              command=self.confirm_cross_section)
        
        cross_section_label = tk.Label(self.cross_section_ui_frame, text="Select the type of cross section:")
        cross_section_label.pack(pady=5)  # Added some padding for visual spacing

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

        # Initially call on_plane_selected to set up the correct UI
        self.on_plane_selected()

        # Confirm button
        self.cross_section_button.pack()

    def setup_cylindrical_cross_section_ui(self):
        # Setup for cylindrical coordinates
        angle_label = tk.Label(self.cross_section_ui_frame, text="Angle:")
        angle_label.pack()
        self.angle_entry = tk.Entry(self.cross_section_ui_frame)
        self.angle_entry.pack()

        distance_label = tk.Label(self.cross_section_ui_frame, text="Distance of the intersection point from the axis:", wraplength=200)
        distance_label.pack()
        self.distance_entry = tk.Entry(self.cross_section_ui_frame)
        self.distance_entry.pack()

        height_label = tk.Label(self.cross_section_ui_frame, text="Height of the intersection point:", wraplength=200)
        height_label.pack()
        self.height_entry = tk.Entry(self.cross_section_ui_frame)
        self.height_entry.pack()

        confirm_button = tk.Button(self.cross_section_ui_frame, text="Confirm Cross Section", command=self.confirm_cylindrical_cross_section)
        confirm_button.pack()

    def confirm_cylindrical_cross_section(self):
        try:
            # Retrieve user inputs
            angle = float(self.angle_entry.get())  # Angle in degrees
            radius = float(self.distance_entry.get())  # Distance to Z-axis
            height = float(self.height_entry.get())  # Height (Z coordinate)

            # Calculate three points on the cross section
            points = self.get_cross_section_points(radius, angle, height)

            # Use these points in your load_crosssection function
            # Check for colinearity
            if self.collinear(points):
                raise ValueError("Chosen points are collinear, the plane cannot be determined.")

            self.load_crosssection(*points)
        except Exception as error:
            self.error_message(str(error))


    def on_plane_selected(self):
        # Hide all frames
        for frame in self.coord_frames.values():
            frame.pack_forget()

        # Show the relevant frame
        selected_plane = self.plane_var.get()
        self.coord_frames[selected_plane].pack()

        # Repack the confirm button to ensure it is always at the bottom
        self.cross_section_button.pack_forget()  # Remove the button from its current location
        self.cross_section_button.pack(pady=10)  # Repack it to make sure it is at the bottom

    def clear_and_setup_cross_section_ui(self):
        if self.cross_section_ui_frame is not None:
            self.cross_section_ui_frame.destroy()  # Destroy the entire frame

        self.cross_section_ui_frame = tk.Frame(self.controls_frame)  # Recreate the frame
        self.cross_section_ui_frame.pack(pady=10)  # Pack the frame in the desired location

        self.setup_cross_section_ui()

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
            # Check for colinearity
            if self.collinear(points):
                raise ValueError("Choosen points are coolinear, the plane cannot be determined.")
            
            self.load_crosssection(*points)
        except Exception as error:
            self.error_message(str(error))

    def collinear(self, points):
        """
        Checks if given 3 3d points are coolinear.
        Return True if yes, False otherwise.
        """
        p1, p2, p3 = points
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x3, y3, z3 = p3
        vector1 = ((x2 - x1), (y2 - y1), (z2 - z1))
        vector2 = ((x3 - x1), (y3 - y1), (z3 - z1))

        # Calculate cross product
        cross_product = (
            vector1[1] * vector2[2] - vector1[2] * vector2[1],
            vector1[2] * vector2[0] - vector1[0] * vector2[2],
            vector1[0] * vector2[1] - vector1[1] * vector2[0]
        )

        # Check if the cross product is zero (collinear points)
        return all(coord == 0 for coord in cross_product)

    def get_cross_section_points(self, r, theta, z, delta=2):
        # Three points at theta, theta + delta, and theta - delta
        theta = math.radians(theta)
        point1 = (r, 0, z)
        point2 = (r, r, z)
        point3 = (r + delta*math.cos(theta), 0, z - delta*math.sin(theta))
        return point1, point2, point3

    def terminate_program(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            print("Terminating program")
            self.root.quit()
            self.root.destroy()
        else:
            print("Exit canceled")

    def error_message(self, error):
        messagebox.showerror("Error", f"A following error has occured:\n{error}")
