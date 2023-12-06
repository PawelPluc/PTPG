from tkinter import Tk, filedialog

def import_dialog(data_type = "figure"):
    """
    Displays an input dialog to allow the user to choose the file.
    Should be the same for all types of data, with the only difference being suggesting different names of files by default.
    """
    print("Choose a file to be loaded")
    Tk().withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path
