import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph_manager import GraphManager
from bellman_ford import bellman_ford, reconstruct_path

class FlightOptimizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flight Ticket Price Optimization")
        self.root.geometry("1000x720")
        self.root.configure(bg="#1e1e1e")

        self.graph_manager = GraphManager()
        self.current_canvas = None

        self.start_city_var = tk.StringVar()
        self.end_city_var = tk.StringVar()

        self.setup_frames()
        self.setup_widgets()
        self.mode_selection()

    def setup_frames(self):
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def setup_widgets(self):
        # Left controls
        tk.Label(self.left_frame, text="Find Cheapest Route", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

        tk.Label(self.left_frame, text="Starting City:", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        self.start_city_dropdown = ttk.Combobox(self.left_frame, textvariable=self.start_city_var, state="readonly", font=("Helvetica", 12))
        self.start_city_dropdown.pack(pady=5)

        tk.Label(self.left_frame, text="Destination City:", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        self.end_city_dropdown = ttk.Combobox(self.left_frame, textvariable=self.end_city_var, state="readonly", font=("Helvetica", 12))
        self.end_city_dropdown.pack(pady=5)

        tk.Button(self.left_frame, text="Find Cheapest Route", command=self.find_cheapest_route, font=("Helvetica", 12, "bold"),
                  bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black").pack(pady=10)

        self.result_label = tk.Label(self.left_frame, text="", justify="left", font=("Helvetica", 12), bg="#1e1e1e", fg="white")
        self.result_label.pack(pady=10)

        tk.Label(self.left_frame, text="Modify Flight Routes", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)

        tk.Label(self.left_frame, text="From City (IATA code):", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        self.from_entry = tk.Entry(self.left_frame, font=("Helvetica", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        self.from_entry.pack(pady=5)

        tk.Label(self.left_frame, text="To City:", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        self.to_entry = tk.Entry(self.left_frame, font=("Helvetica", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        self.to_entry.pack(pady=5)

        tk.Label(self.left_frame, text="Price ($):", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack()
        self.price_entry = tk.Entry(self.left_frame, font=("Helvetica", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        self.price_entry.pack(pady=5)

        tk.Button(self.left_frame, text="Add Flight", command=self.add_flight, font=("Helvetica", 12, "bold"),
                  bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black").pack(pady=5)

        tk.Button(self.left_frame, text="Remove Flight", command=self.remove_flight, font=("Helvetica", 12, "bold"),
                  bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black").pack(pady=5)

        tk.Button(self.left_frame, text="Show Graph", command=self.show_graph, font=("Helvetica", 12, "bold"),
                  bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black").pack(pady=15)

    def mode_selection(self):
        mode_window = tk.Toplevel(self.root)
        mode_window.title("Select Mode")
        mode_window.geometry("350x200")
        mode_window.configure(bg="#1e1e1e")
        mode_window.resizable(False, False)

        tk.Label(mode_window, text="Choose Startup Mode:", font=("Helvetica", 14, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)

        tk.Button(
            mode_window,
            text="Demo Mode",
            font=("Helvetica", 12, "bold"),
            bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black",
            command=lambda: [self.graph_manager.load_demo_graph(), self.update_dropdown_options(), self.show_graph(), mode_window.destroy()]
        ).pack(pady=10)

        tk.Button(
            mode_window,
            text="Live Mode",
            font=("Helvetica", 12, "bold"),
            bg="#d9d9d9", fg="black", activebackground="#bfbfbf", activeforeground="black",
            command=lambda: [self.graph_manager.load_live_graph(), self.update_dropdown_options(), self.show_graph(), mode_window.destroy()]
        ).pack(pady=10)

        mode_window.grab_set()

    def find_cheapest_route(self):
        start_city = self.start_city_var.get()
        end_city = self.end_city_var.get()

        if start_city not in self.graph_manager.flight_graph or end_city not in self.graph_manager.flight_graph:
            messagebox.showerror("Invalid City", "One or both cities are invalid.")
            return

        try:
            distances, predecessors = bellman_ford(self.graph_manager.flight_graph, start_city)
            if end_city in distances:
                route = reconstruct_path(predecessors, start_city, end_city)
                total_cost = distances[end_city]
                self.result_label.config(
                    text=f"Cheapest price from {start_city} to {end_city}: ${total_cost}\nRoute: {' → '.join(route)}"
                )

                self.graph_manager.highlighted_nodes = route
                self.graph_manager.highlighted_edges = [(route[i], route[i+1]) for i in range(len(route)-1)]

                self.show_graph()
            else:
                messagebox.showerror("No Path", "No path found between the cities.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_flight(self):
        from_city = self.from_entry.get().upper()
        to_city = self.to_entry.get().upper()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a valid number for price.")
            return

        self.graph_manager.add_flight(from_city, to_city, price)
        self.update_dropdown_options()
        self.show_graph()

    def remove_flight(self):
        from_city = self.from_entry.get().upper()
        to_city = self.to_entry.get().upper()

        self.graph_manager.remove_flight(from_city, to_city)
        self.update_dropdown_options()
        self.show_graph()

    def show_graph(self):
        if self.current_canvas is not None:
            self.current_canvas.get_tk_widget().destroy()

        fig = self.graph_manager.draw_graph()

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_dropdown_options(self):
        cities = sorted(self.graph_manager.flight_graph.keys())
        self.start_city_dropdown['values'] = cities
        self.end_city_dropdown['values'] = cities

        if cities:
            self.start_city_var.set(cities[0])
            self.end_city_var.set(cities[0])

    def run(self):
        self.root.mainloop()