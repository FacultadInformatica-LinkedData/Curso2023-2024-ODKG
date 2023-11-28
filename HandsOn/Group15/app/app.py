import tkinter as tk

import matplotlib.pyplot as plt
import tkintermapview
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

from knowledge_graph import cabins_which_measure_contaminants, cabins_in_neighbourhoods_with_populations_bigger_than, \
    temperature_data, trees_of_species
from map import add_markers

root = tk.Tk()
width, height = 1200, 1000
root.geometry(f"{width}x{height}")
root.title("Barcelona Environmental Monitoring")
root.config(bg="skyblue")


def main():
    map_widget = create_map_widget()

    management_bar = tk.Frame(root, width=width, height=200, bg='grey')
    contaminant_frame(management_bar, map_widget)
    population_frame(management_bar, map_widget)
    tree_frame(management_bar, map_widget)
    temperature_frame(management_bar)

    management_bar.grid(row=0, column=0, padx=5, pady=5)

    # run the GUI
    root.mainloop()


def contaminant_frame(management_bar: tk.Frame, map_widget: tkintermapview.TkinterMapView):
    def button_click():
        map_widget.delete_all_marker()
        latitudes, longitudes, texts, info = cabins_which_measure_contaminants(contaminant_text_entry.get())
        add_markers(map_widget, latitudes, longitudes, texts)
        tk.messagebox.showinfo("Contaminant Info", info)

    # Make the top frame cover the whole width of the root
    outer_frame = tk.Frame(management_bar, width=width // 4, height=200, bg='grey')
    outer_frame.grid(row=0, column=0, padx=5, pady=5)

    contaminant_title = tk.Label(outer_frame, text="Cabins by contaminant name (e.g. ozone)",
                                 font=("Arial", 14))
    contaminant_title.pack()
    contaminant_text_entry = tk.Entry(outer_frame)
    contaminant_text_entry.pack()
    contaminant_search_button = tk.Button(outer_frame, text="Display", command=button_click)
    contaminant_search_button.pack()


def population_frame(management_bar: tk.Frame, map_widget: tkintermapview.TkinterMapView):
    def button_click():
        map_widget.delete_all_marker()
        latitudes, longitudes, texts = cabins_in_neighbourhoods_with_populations_bigger_than(
            int(population_text_entry.get()))
        add_markers(map_widget, latitudes, longitudes, texts)

    # Make the top frame cover the whole width of the root
    outer_frame = tk.Frame(management_bar, width=width // 4, height=200, bg='grey')
    outer_frame.grid(row=0, column=1, padx=5, pady=5)

    population_title = tk.Label(outer_frame, text="Cabins by population threshold (e.g. 50000)", font=("Arial", 14))
    population_title.pack()
    population_text_entry = tk.Entry(outer_frame)
    population_text_entry.pack()
    population_search_button = tk.Button(outer_frame, text="Display", command=button_click)
    population_search_button.pack()


def tree_frame(management_bar: tk.Frame, map_widget: tkintermapview.TkinterMapView):
    def button_click():
        map_widget.delete_all_marker()
        latitudes, longitudes = trees_of_species(tree_text_entry.get())
        add_markers(map_widget, latitudes, longitudes, [""] * len(latitudes), icon_filename="tree.png")

    # Make the top frame cover the whole width of the root
    outer_frame = tk.Frame(management_bar, width=width // 4, height=200, bg='grey')
    outer_frame.grid(row=0, column=2, padx=5, pady=5)

    tree_title = tk.Label(outer_frame, text="Trees by species (e.g. Yucca gigantea)", font=("Arial", 14))
    tree_title.pack()
    tree_text_entry = tk.Entry(outer_frame)
    tree_text_entry.pack()
    tree_search_button = tk.Button(outer_frame, text="Display", command=button_click)
    tree_search_button.pack()


def create_map_widget() -> tkintermapview.TkinterMapView:
    bottom_frame = tk.Frame(root, width=width, height=800, bg='grey')
    bottom_frame.grid(row=1, column=0, padx=5, pady=5)

    map_widget = tkintermapview.TkinterMapView(bottom_frame, width=width, height=1000, corner_radius=0)
    map_widget.set_position(41.3874, 2.1686)
    map_widget.set_zoom(12)
    map_widget.pack()
    return map_widget


def temperature_frame(management_bar: tk.Frame):
    def button_click():
        input_text = temperature_text_entry.get().strip().split(" ")
        start, end, month = input_text[0], input_text[1], input_text[2]
        data = temperature_data(int(start), int(end), month)
        create_scatter_graph(data)

    outer_frame = tk.Frame(management_bar, width=width // 4, height=200, bg='grey')
    outer_frame.grid(row=0, column=3, padx=5, pady=5)
    temperature_title = tk.Label(outer_frame, text="Temperatures (start end month)", font=("Arial", 14))
    temperature_title.pack()
    temperature_text_entry = tk.Entry(outer_frame)
    temperature_text_entry.pack()
    temperature_search_button = tk.Button(outer_frame, text="View", command=button_click)
    temperature_search_button.pack()


def create_scatter_graph(data):
    popup = tk.Toplevel(root)
    popup.title("Temperature Pop-up")

    fig, ax = plt.subplots()
    x, y = zip(*data)
    ax.scatter(x, y, color='red')
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature")
    ax.set_title("Temperature over time")

    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()


if __name__ == "__main__":
    main()
