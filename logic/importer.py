import numpy as np
import GUI.import_dialog as dial

class Figure_import():

    def __init__(self):
        self.data = {
            'file_name': None,
            'laser_symmetry': None,
            'laser_length': None,
            'number_layers': None,
            'coordinates': None,
            'temperature': None
        }
        
    def load_data(self):
        """
        Return True if loading was successful, False if not.
        """
        file_path = import_dialog()
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
        file_name = file_path.split("_")[-1]
        print(file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extracting values from the third line
        third_line_values = lines[2].split()
        try:
            self.data['laser_symmetry'] = int(third_line_values[0])
        except ValueError:
            raise ValueError(f"Laser symmetry needs to be an integer value, but '{third_line_values[0]}' is not an int.")
        print("Symmetry:", self.data['laser_symmetry'])

        try:
            self.data['laser_length'] = int(third_line_values[1])
        except ValueError:
            raise ValueError(f"Length of the laser needs to be an integer value, but '{third_line_values[1]}' is not an int.")
        print("Length:", self.data['laser_length'])

        # Extracting the number of layers from the fifth line
        fifth_line_values = lines[4].split()
        try:
            self.data['number_layers'] = int(fifth_line_values[0])
        except ValueError:
            raise ValueError(f"Number of layers needs to be an integer value, but '{fifth_line_values[0]}' cannot be converted to int.")
        print('Layers:', self.data['number_layers'])

        # Skipping the empty line
        current_line = 6

        # Iterating through each layer
        coordinates = []
        for _ in range(self.data['number_layers']):
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
        self.data['coordinates'] = np.array(coordinates, dtype=object)

        # Extracting values from the 7th line from the bottom
        temperature_values = lines[-7].split()[:5]
        if len(temperature_values) != 5:
            raise ValueError(f"Expected 5 values, but found {len(temperature_values)} values in this line.")

        try:
            self.data['temperature'] = np.array([float(value) for value in temperature_values])
        except ValueError:
            raise ValueError("Not all values in the temperature line are floats or some values are missing.")

        print("Temperature:", self.data['temperature'])

        self.data['file_name'] = file_name
        