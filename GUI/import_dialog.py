from tkinter import Tk, filedialog

def import_dialog(data_type = "figure"):
    """
    Displays an input dialog to allow the user to choose the file.
    Should be the same for all types of data, with the only difference being suggesting different names of files by default.
    Return path to a file
    """
    Tk().withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path


if __name__ == "__main__":
    x = import_dialog("figure")
    print(x)



