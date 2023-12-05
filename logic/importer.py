import GUI.import_dialog as dial

class Figure_import():

    def __init__(self):
        self.data = None # TO DO discuss with Oskar and Oliwka how the data will look like 

    def load_data(self):
        """
        Loads the data about the figure and saves it to self.data
        Return True if loading was succefull, False if not.
        """
        dial.import_dialog(data_type = "figure")

        return False

    def get_data(self):
        """
        Return the loaded data.
        """
        if self.data == None:
            raise Exception("No data was loaded")
        return self.data