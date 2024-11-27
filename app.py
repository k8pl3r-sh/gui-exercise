import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer")

        # File selection
        self.file_label = tk.Label(root, text="No file selected", anchor="w")
        self.file_label.pack(fill="x", padx=10, pady=5)

        self.browse_button = tk.Button(root, text="Browse File", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Data preview : need to fix if too much colunms
        self.data_preview = tk.Text(root, height=10, state="disabled")
        self.data_preview.pack(fill="both", padx=10, pady=5)

        # Plot options
        options_frame = tk.Frame(root)
        options_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(options_frame, text="X-Axis:").grid(row=0, column=0, padx=5)
        self.x_axis = ttk.Combobox(options_frame, state="readonly")
        self.x_axis.grid(row=0, column=1, padx=5)

        tk.Label(options_frame, text="Y-Axis:").grid(row=0, column=2, padx=5)
        self.y_axis = ttk.Combobox(options_frame, state="readonly")
        self.y_axis.grid(row=0, column=3, padx=5)

        tk.Label(options_frame, text="Plot Type:").grid(row=0, column=4, padx=5)
        self.plot_type = ttk.Combobox(options_frame, state="readonly",
                                      values=["Line", "Scatter", "Bar"])
        self.plot_type.grid(row=0, column=5, padx=5)
        self.plot_type.current(0)

        self.plot_button = tk.Button(root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack(pady=10)

        # Plot display
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

        self.data = None

    def browse_file(self):
        # BUG: fix mouse must be pressed continuously
        # Add JSON extension also and compressed like for datascience ?
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")]
        )
        if not file_path:
            return

        self.file_label.config(text=file_path)
        try:
            if file_path.endswith(".csv"):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith(".txt"):
                self.data = pd.read_csv(file_path, delimiter="\t")
            else:
                raise ValueError("Unsupported file format")

            self.update_preview()
            self.update_column_options()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def update_preview(self):
        self.data_preview.config(state="normal")
        self.data_preview.delete("1.0", tk.END)
        self.data_preview.insert(tk.END, self.data.head().to_string())
        self.data_preview.config(state="disabled")

    def update_column_options(self):
        columns = self.data.columns.tolist()
        self.x_axis.config(values=columns)
        self.y_axis.config(values=columns)

    def plot_data(self):
        # TODO : method to create and save the plot (cf mw_classifier)
        x_col = self.x_axis.get()
        y_col = self.y_axis.get()
        plot_type = self.plot_type.get().lower()

        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select columns for both X and Y axes.")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        try:
            # Add more plot types (like cloud or so on ?)
            if plot_type == "line":
                ax.plot(self.data[x_col], self.data[y_col])
            elif plot_type == "scatter":
                ax.scatter(self.data[x_col], self.data[y_col])
            elif plot_type == "bar":
                ax.bar(self.data[x_col], self.data[y_col])
            ax.set_title(f"{plot_type.capitalize()} Plot")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotApp(root)
    root.mainloop()
