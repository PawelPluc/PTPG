from tkinter import Tk, filedialog

def import_dialog(data_type = "figure"):
    """
    Displays an input dialog to allow the user to choose the file.
    Should be the same for all types of data, with the only difference being suggesting different names of files by default.
    Return path to a file
    """
    if data_type == "figure":
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
    elif data_type == "potential":
        filetypes=[(".wyn files", "*.wyn"), ("All files", "*.*")]

    Tk().withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=filetypes
    )
    return file_path


if __name__ == "__main__":
    x = import_dialog("figure")
    print(x)



