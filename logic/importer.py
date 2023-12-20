import numpy as np
import GUI.import_dialog as dial

class Figure_import():

    def __init__(self):
        self.file_name = None
        self.laser_symmetry = None
        self.laser_length = None
        self.number_layers = None
        self.coordinates = None
        self.temperature = None
        
    def load_data(self):
        """
        Return True if loading was successful, False if not.
        """
        file_path = dial.import_dialog()
        if not file_path:
            print("File selection cancelled.")
            return False

        try:
            self.process_file(file_path)
            print("Data loaded successfully.")
            return True
        except ValueError as e:
            print(f"Error loading data: {e}")
            return False

    def process_file(self, file_path):
        """
        Loads the data about the figure checking if the input is correct and saves it to self.data.
        """
        self.file_name = file_path.split("_")[-1]
        print(self.file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extracting values from the third line
        try:
            third_line_values = lines[2].split()
        except IndexError:
            raise ValueError(f"The file does not contain figure data.")
        try:
            self.laser_symmetry = int(third_line_values[0])
        except ValueError:
            raise ValueError(f"Laser symmetry needs to be an integer value, but '{third_line_values[0]}' is not an int.")
        print("Symmetry:", self.laser_symmetry)

        try:
            self.laser_length = float(third_line_values[1])
        except ValueError:
            raise ValueError(f"Length of the laser needs to be an integer value, but '{third_line_values[1]}' is not an int.")
        print("Length:", self.laser_length)

        # Extracting the number of layers from the fifth line
        fifth_line_values = lines[4].split()
        try:
            self.number_layers = int(fifth_line_values[0])
        except ValueError:
            raise ValueError(f"Number of layers needs to be an integer value, but '{fifth_line_values[0]}' cannot be converted to int.")
        print('Layers:', self.number_layers)

        # Skipping the empty line
        current_line = 6

        # Iterating through each layer
        coordinates = []
        end = False

        while end == False:
            layer_values = lines[current_line].split()

            if int(layer_values[0]) > 0:
                try:
                    float_value = float(layer_values[1])
                except ValueError:
                    end = True
                    break
                else:
                    end = False

                layer_values = lines[current_line].split()[:6]
                print('layer_values', layer_values)
                if len(layer_values) != 6:
                    raise ValueError(f"Expected 6 values, but found {len(layer_values)} values in line {current_line + 1}")

                try:
                    # Check types for each value in the layer_values list
                    int_value = int(layer_values[0])
                    float_values = [float(val) for val in layer_values[1:5]]
                    for val in layer_values[1:5]:
                        try:
                            float_val = float(val)
                            float_values.append(float_val)
                        except (ValueError, TypeError): #error when the coordinates cannot be converted to floats
                            raise ValueError(f"Invalid types in line {current_line + 1}. Coordinates must be floats.")
                    string_value = layer_values[5]

                    coordinates.append([int_value] + float_values + [string_value])
                except ValueError:
                    raise ValueError(f"Invalid types in line {current_line + 1}. First value must be an integer, coordinates must be floats, and the last must be a string.")

                current_line += 6
            else:
                try:
                    float_value = float(layer_values[1])
                except ValueError:
                    end = True
                    break
                else:
                    end = False
                layer_values = lines[current_line].split()[:3]
                print('layer_values', layer_values)
                if len(layer_values) != 3:
                    raise ValueError(f"Expected 3 values, but found {len(layer_values)} values in line {current_line + 1}")

                try:
                    # Check types for each value in the layer_values list
                    int_value = int(layer_values[0])
                    float_values = [float(val) for val in layer_values[1:2]]
                    for val in layer_values[1:2]:
                        try:
                            float_val = float(val)
                            float_values.append(float_val)
                        except (ValueError, TypeError): #error when the coordinates cannot be converted to floats
                            raise ValueError(f"Invalid types in line {current_line + 1}. Coordinates must be floats.")

                    coordinates.append([int_value] + float_values)
                except ValueError:
                    raise ValueError(f"Invalid types in line {current_line + 1}. First value must be an integer and the coordinates must be floats.")

                current_line += 2

        self.coordinates = np.array(coordinates, dtype=object)

        # Extracting temperature data
        end2 = False
        if 'temp' in self.file_name: 
            while end2 == False:
                layer_values = lines[current_line].split()
                if int(float(layer_values[0])) == 1:
                    current_line += 1
                    temperature_values = lines[current_line].split()[:5]
                    if len(temperature_values) != 5:
                        raise ValueError(f"Expected 5 values, but found {len(temperature_values)} values in this line.")
                    try:
                        self.temperature = np.array([float(value) for value in temperature_values])
                        break
                    except ValueError:
                        raise ValueError("Not all values in the temperature line are floats or some values are missing.")
                    
                else:
                    current_line += 1
            print("Temperature:", self.temperature)
        
"""figure_importer = Figure_import()
if figure_importer.load_data():
    print(figure_importer.data)"""
