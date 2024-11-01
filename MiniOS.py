import tkinter as tk
from tkinter import filedialog, messagebox, Text
import os
import shutil
import subprocess
import zipfile

class MiniOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Operating System")
        self.root.geometry("800x600")
        self.current_file_path = None

        # Menus
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Text Editor", command=self.open_text_editor)
        tools_menu.add_command(label="Calculator", command=self.open_calculator)
        tools_menu.add_command(label="Terminal", command=self.open_terminal)
        tools_menu.add_command(label="Backup", command=self.backup_file)
        tools_menu.add_command(label="Delete File", command=self.delete_file)
        tools_menu.add_command(label="Compress Folder", command=self.compress_folder)
        tools_menu.add_command(label="Create Text File", command=self.create_file)

        # Main window layout
        self.main_frame = tk.Frame(self.root, bg="#dfe3ee")
        self.main_frame.pack(fill="both", expand=True)
        self.display_label = tk.Label(self.main_frame, text="Welcome to Subhan's Mini Operating System", font=("Helvetica", 16))
        self.display_label.pack(pady=20)

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'r') as file:
                content = file.read()
            self.display_content(content, "File Explorer")

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            content = self.display_label.cget("text")
            with open(filepath, 'w') as file:
                file.write(content)
            messagebox.showinfo("Save", "File saved successfully!")

    def display_content(self, content, title=""):
        self.display_label.config(text=content, font=("Helvetica", 12))
        self.root.title(f"Mini OS - {title}")

    def open_text_editor(self):
        editor = tk.Toplevel(self.root)
        editor.title("Text Editor")
        editor.geometry("400x300")

        self.current_file_path = None  # Reset current file path when editor is opened

        text_area = Text(editor, wrap="word")
        text_area.pack(fill="both", expand=True)

        def load_file():
            filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if filepath:
                self.current_file_path = filepath
                with open(filepath, 'r') as file:
                    content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, content)
                editor.title(f"Text Editor - {os.path.basename(filepath)}")

        def save_file():
            if self.current_file_path:
                with open(self.current_file_path, 'w') as file:
                    file.write(text_area.get("1.0", tk.END))
                messagebox.showinfo("Text Editor", "File saved successfully!")
            else:
                save_file_as()

        def save_file_as():
            filepath = filedialog.asksaveasfilename(defaultextension=".txt")
            if filepath:
                self.current_file_path = filepath
                with open(filepath, 'w') as file:
                    file.write(text_area.get("1.0", tk.END))
                editor.title(f"Text Editor - {os.path.basename(filepath)}")
                messagebox.showinfo("Text Editor", "File saved successfully!")

        editor_menu = tk.Menu(editor)
        editor.config(menu=editor_menu)
        editor_menu.add_command(label="Open", command=load_file)
        editor_menu.add_command(label="Save", command=save_file)
        editor_menu.add_command(label="Save As", command=save_file_as)

    def backup_file(self):
        file_to_backup = filedialog.askopenfilename(title="Select a file to backup")
        if not file_to_backup:
            return

        backup_directory = filedialog.askdirectory(title="Select Backup Directory")
        if not backup_directory:
            return

        try:
            backup_path = os.path.join(backup_directory, os.path.basename(file_to_backup))
            shutil.copy(file_to_backup, backup_path)
            messagebox.showinfo("Backup", f"Backup of {os.path.basename(file_to_backup)} saved in {backup_directory}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup file: {str(e)}")

    def open_calculator(self):
        calculator = tk.Toplevel(self.root)
        calculator.title("Calculator")
        calculator.geometry("300x400")
        
        expression = tk.StringVar()
        input_field = tk.Entry(calculator, textvariable=expression, font=("Helvetica", 16), borderwidth=5)
        input_field.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(calculator, text=text, width=10, height=3,
                               command=lambda txt=text: self.on_calculator_button_click(txt, expression))
            button.grid(row=row, column=col)

    def on_calculator_button_click(self, char, expression):
        if char == '=':
            try:
                result = eval(expression.get())
                expression.set(str(result))
            except:
                expression.set("Error")
        else:
            expression.set(expression.get() + char)

    def open_terminal(self):
        terminal = tk.Toplevel(self.root)
        terminal.title("Terminal")
        terminal.geometry("500x300")

        command_label = tk.Label(terminal, text="Enter Command:")
        command_label.pack()

        command_entry = tk.Entry(terminal, width=50)
        command_entry.pack()

        output_area = Text(terminal, wrap="word")
        output_area.pack(fill="both", expand=True)

        def execute_command(event=None):
            command = command_entry.get()
            command_entry.delete(0, tk.END)
            try:
                result = subprocess.check_output(command, shell=True, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                result = str(e)
            output_area.insert(tk.END, result + "\n")

        command_entry.bind("<Return>", execute_command)  # Bind Enter key to execute command
        execute_button = tk.Button(terminal, text="Execute", command=execute_command)
        execute_button.pack()

    def delete_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Delete")
        if not file_path:
            return

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                messagebox.showinfo("Delete File", f"File {os.path.basename(file_path)} has been deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
        else:
            messagebox.showerror("Error", "Selected item is not a file. Only files can be deleted.")

    def compress_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Compress")
        if not folder_path:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip files", "*.zip")])
        if not save_path:
            return
        try:
            with zipfile.ZipFile(save_path, 'w') as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))
            messagebox.showinfo("Compression", f"Folder {folder_path} has been compressed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress folder: {str(e)}")

    def create_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")],
                                                title="Create New Text File")
        if filepath:
            try:
                with open(filepath, 'w') as new_file:
                    new_file.write("")
                messagebox.showinfo("Create File", f"File {os.path.basename(filepath)} created successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    MiniOS(root)
    root.mainloop()
