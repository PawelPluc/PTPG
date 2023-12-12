from logic.importer import Figure_import

class Figure():

    def __init__(self):
        self.data = None
    
    def load_data(self):
        """
        Loads the data about the figure.
        """
        data = Figure_import()
        if not data.load_data():
            raise ValueError("Data failed to load.")

    def create_symetry(self):
        """
        Perform all necessary calculation to create a full 3D object from the data.
        Save it to self.data or some new variable.
        """
        pass

    def create_figure(self):
        """
        Main function used from outside, should load the data, create symetry and do all things needed for plotting
        """
        self.load_data()
        self.create_symetry()
