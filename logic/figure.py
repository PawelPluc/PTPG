from logic.importer import Figure_import

class Figure():

    def __init__(self):
        self.data = None
    
    def load_data(self):
        """
        Loads the data about the figure.
        """
        importer = Figure_import()
        if not importer.load_data():
            raise Exception("Data failed to load")
        self.data = importer.get_data() # TO DO discuss with Kasia and Ola how the data will look like 
    
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
