import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def calculate_correlation(symbol1, symbol2, start_date, end_date):
    try:
        # Download historical data
        stock1 = yf.download(symbol1, start=start_date, end=end_date)['Close']
        stock2 = yf.download(symbol2, start=start_date, end=end_date)['Close']

        # Drop missing values
        stock1 = stock1.dropna()
        stock2 = stock2.dropna()

        # Combine data into a DataFrame
        df = pd.concat([stock1, stock2], axis=1)
        df.columns = [symbol1, symbol2]

        # Calculate correlation
        correlation = df[symbol1].corr(df[symbol2])

        return df, correlation
    except Exception as e:
        return None, str(e)

class CorrelationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Correlation Analysis")

        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input fields
        self.symbol1_label = ttk.Label(self.frame, text="Stock Symbol 1:")
        self.symbol1_label.grid(column=0, row=0, sticky=tk.W)
        self.symbol1_entry = ttk.Entry(self.frame)
        self.symbol1_entry.grid(column=1, row=0, sticky=tk.W)

        self.symbol2_label = ttk.Label(self.frame, text="Stock Symbol 2:")
        self.symbol2_label.grid(column=0, row=1, sticky=tk.W)
        self.symbol2_entry = ttk.Entry(self.frame)
        self.symbol2_entry.grid(column=1, row=1, sticky=tk.W)

        self.start_date_label = ttk.Label(self.frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(column=0, row=2, sticky=tk.W)
        self.start_date_entry = ttk.Entry(self.frame)
        self.start_date_entry.grid(column=1, row=2, sticky=tk.W)

        self.end_date_label = ttk.Label(self.frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(column=0, row=3, sticky=tk.W)
        self.end_date_entry = ttk.Entry(self.frame)
        self.end_date_entry.grid(column=1, row=3, sticky=tk.W)

        # Analysis button
        self.analyze_button = ttk.Button(self.frame, text="Analyze", command=self.run_analysis)
        self.analyze_button.grid(column=0, row=4, columnspan=2, sticky=tk.W)

        # Plot
        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.grid(column=1, row=0, rowspan=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def run_analysis(self):
        # Get input values
        symbol1 = self.symbol1_entry.get().upper()
        symbol2 = self.symbol2_entry.get().upper()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Check for empty input fields
        if not symbol1 or not symbol2 or not start_date or not end_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Calculate correlation
        data, result = calculate_correlation(symbol1, symbol2, start_date, end_date)

        if data is not None:
            # Plot the data
            self.ax.clear()
            data.plot(ax=self.ax)
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Close Price')

            # Move the correlation text to the upper-middle of the graph
            if result is not None:
                correlation_text = f"Correlation: {result:.2f}"
                self.ax.text(0.5, 1.05, correlation_text, transform=self.ax.transAxes, ha="center", va="center", fontsize=10, fontweight="bold")

            self.canvas.draw()
        else:
            messagebox.showerror("Error", result)

def main():
    root = tk.Tk()
    app = CorrelationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()