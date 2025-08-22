import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
import os
from PIL import Image, ImageTk

class PyToPngApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐍 PyToPNG - Code Screenshot Tool")
        self.geometry("950x650")
        self.configure(bg="#f0f0f0")
        
        self.font = "DejaVu Sans Mono"
        self.theme = "light"
        self.selected_files = []
        self.output_dir = "C:/Users/ddaar/OneDrive/Desktop/screenshots"
        os.makedirs(self.output_dir, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        # Top controls
        top_frame = tk.Frame(self, bg=self["bg"])
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="📂 Select .py Files", command=self.select_files).grid(row=0, column=0, padx=10)
        tk.Button(top_frame, text="📸 Convert to PNG", command=self.convert_files).grid(row=0, column=1, padx=10)
        tk.Button(top_frame, text="🌗 Toggle Theme", command=self.toggle_theme).grid(row=0, column=2, padx=10)
        tk.Button(top_frame, text="📁 Select Output Folder", command=self.select_output_dir).grid(row=0, column=3, padx=10)

        # Font picker
        tk.Label(top_frame, text="Font:", bg=self["bg"]).grid(row=0, column=4, padx=(20, 5))
        self.font_var = tk.StringVar(value=self.font)
        self.font_menu = ttk.Combobox(top_frame, textvariable=self.font_var, values=[
            "DejaVu Sans Mono", "Courier New", "Consolas", "Liberation Mono"
        ])
        self.font_menu.grid(row=0, column=5)

        # Display current output folder
        self.output_label = tk.Label(self, text=f"Output Folder: {self.output_dir}", bg=self["bg"], anchor="w")
        self.output_label.pack(fill="x", padx=20)

        # File list
        self.files_listbox = tk.Listbox(self, height=6)
        self.files_listbox.pack(padx=20, pady=10, fill="x")

        # Preview label
        self.preview_label = tk.Label(self, text="🖼️ PNG Preview will appear here", bg=self["bg"])
        self.preview_label.pack(pady=5)

        # Preview image canvas
        self.preview_canvas = tk.Label(self)
        self.preview_canvas.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        if files:
            self.selected_files = list(files)
            self.files_listbox.delete(0, tk.END)
            for f in self.selected_files:
                self.files_listbox.insert(tk.END, f)

    def select_output_dir(self):
        folder = filedialog.askdirectory(initialdir=self.output_dir)
        if folder:
            self.output_dir = folder
            self.output_label.config(text=f"Output Folder: {self.output_dir}")
            os.makedirs(self.output_dir, exist_ok=True)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.configure(bg="#2e2e2e" if self.theme == "dark" else "#f0f0f0")
        fg_color = "white" if self.theme == "dark" else "black"
        for widget in self.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Listbox)):
                widget.configure(bg=self["bg"], fg=fg_color)

    def convert_files(self):
        if not self.selected_files:
            messagebox.showerror("No files", "Please select one or more .py files.")
            return

        last_image_path = None

        for py_file in self.selected_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    code = f.read()

                formatter = ImageFormatter(
                    font_name=self.font_var.get(),
                    font_size=16,
                    line_numbers=True,
                    image_format="png",
                    style="monokai" if self.theme == "dark" else "default"
                )

                png_data = pygments.highlight(code, PythonLexer(), formatter)
                filename = os.path.basename(py_file)
                name, _ = os.path.splitext(filename)
                output_path = os.path.join(self.output_dir, f"{name}.png")

                with open(output_path, "wb") as img_out:
                    img_out.write(png_data)

                last_image_path = output_path  # Track for preview

            except Exception as e:
                messagebox.showerror("Error", f"Failed for {py_file}:\n{e}")

        if last_image_path:
            self.show_preview(last_image_path)

        messagebox.showinfo("Done", "✅ All selected Python files were converted to PNG!")

    def show_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((700, 500))
            preview_img = ImageTk.PhotoImage(img)
            self.preview_canvas.config(image=preview_img)
            self.preview_canvas.image = preview_img  # keep reference
            self.preview_label.config(text=f"🖼️ Preview: {os.path.basename(image_path)}")
        except Exception as e:
            self.preview_label.config(text=f"Preview failed: {e}")

if __name__ == "__main__":
    app = PyToPngApp()
    app.mainloop()
