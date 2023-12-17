import numpy as np
# from ..GUI.import_dialog import import_dialog

# TO BE MOVED TO GUI WHEN WE KNOW WHY IMPORT DOESN'T WORK
from tkinter import Tk, filedialog

def import_dialog(data_type = "figure"):
    """
    Displays an input dialog to allow the user to choose the file.
    Should be the same for all types of data, with the only difference being suggesting different names of files by default.
    """
    Tk().withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[(".wyn files", "*.wyn"), ("All files", "*.*")]
    )
    return file_path
# TILL HERE


class Data_import():

    def __init__(self):
        self.file_name = None
        self.type = None
        self.data = None
        self.degrees_type = None


    def load_data(self):
        """
        Return True if loading was successful, False if not.
        """
        file_path = import_dialog(data_type="figure")
        if not file_path:
            print("File selection cancelled.")
            return False

        try:
            self.process_file(file_path)
            print("Temperature data loaded successfully.")
            return True
        except ValueError as e:
            print(f"Error loading temperature data: {e}")
            return False

    def process_file(self, file_path):
        """
        Loads the temperature data checking if the input is correct and saves it to self.data.
        """
        self.file_name = file_path.split("_")[-1]
        print(self.file_name)

        # Determine type based on the file name
        if self.file_name == "pote.wyn":
            self.type = 'potential'
        elif self.file_name == "temp.wyn":
            self.type = 'temperature'
        else:
            raise ValueError(f"Unsupported file type. Expected 'pote.wyn' or 'temp.wyn', but got '{self.file_name}'.")

        print("Type:", self.type)

        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Reading the third value of the second line for degrees_type
        degrees_type_value = lines[1].split()[2]
        if self.type == 'temperature':
            if degrees_type_value == "T[K]":
                self.degrees_type = "K"
            elif degrees_type_value == "T[C]":
                self.degrees_type = "C"
            else:
                raise ValueError("Temperature must be specified in Kelvins (T[K]) or Celsius (T[C]).")
        elif self.type == 'potential':
            self.degrees_type = "V"
            
        print("Degrees Type:", self.degrees_type)
        
        # Skipping the first two lines
        current_line = 2

        data = []
        for line in lines[2:]:
            if not line.strip():  # Check if the line is empty
                break
            values = lines[current_line].split()[:4]
            if len(values) != 4:
                raise ValueError(f"Expected 4 values, but found {len(values)} values in line {current_line + 1}")

            try:
                node_number = int(values[0])
                temperature = float(values[1])
                x_coordinate = float(values[2])
                y_coordinate = float(values[3])

                data.append([node_number, temperature, x_coordinate, y_coordinate])
            except ValueError:
                raise ValueError(f"Invalid types in line {current_line + 1}. Node number must be an integer, temperature must be a float, X and Y coordinates must be floats.")

            current_line += 1

        self.data = np.array(data, dtype=object)


figure_importer = Data_import()
if figure_importer.load_data():
    print(figure_importer.data)