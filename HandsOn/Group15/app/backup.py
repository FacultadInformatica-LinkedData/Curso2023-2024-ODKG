import tkinter as tk

import tkintermapview

from knowledge_graph import cabins_which_measure_contaminants, cabins_in_neighbourhoods_with_populations_bigger_than
from map import add_markers

root = tk.Tk()
width, height = 1500, 1000
root.geometry(f"{width}x{height}")
root.title("Barcelona Environmental Monitoring")
root.config(bg="skyblue")


def main():
    map_widget = create_map_widget()

    management_bar = tk.Frame(root, width=width, height=200, bg='grey')
    contaminant_frame(management_bar, map_widget)
    cabin_frame(management_bar, map_widget)
    management_bar.grid(row=0, column=0, padx=5, pady=5)

    # run the GUI
    root.mainloop()


def contaminant_frame(management_bar: tk.Frame, map_widget: tkintermapview.TkinterMapView):
    def button_click():
        map_widget.delete_all_marker()
        latitudes, longitudes, texts = cabins_which_measure_contaminants(contaminant_text_entry.get())
        add_markers(map_widget, latitudes, longitudes, texts)

    # Make the top frame cover the whole width of the root
    outer_frame = tk.Frame(management_bar, width=width // 2 - 100, height=200, bg='grey')
    outer_frame.grid(row=0, column=0, padx=5, pady=5)

    contaminant_title = tk.Label(outer_frame, text="Search by contaminant name (e.g. carbon monoxide)",
                                 font=("Arial", 20))
    contaminant_title.pack()
    contaminant_text_entry = tk.Entry(outer_frame)
    contaminant_text_entry.pack()
    contaminant_search_button = tk.Button(outer_frame, text="Search", command=button_click)
    contaminant_search_button.pack()


def cabin_frame(management_bar: tk.Frame, map_widget: tkintermapview.TkinterMapView):
    def button_click():
        map_widget.delete_all_marker()
        latitudes, longitudes, texts = cabins_in_neighbourhoods_with_populations_bigger_than(
            population_text_entry.get())
        add_markers(map_widget, latitudes, longitudes, texts)

    # Make the top frame cover the whole width of the root
    outer_frame = tk.Frame(management_bar, width=width // 2, height=200, bg='grey')
    outer_frame.grid(row=0, column=1, padx=5, pady=5)

    population_title = tk.Label(outer_frame, text="Search by population threshold (e.g. 50000)", font=("Arial", 20))
    population_title.pack()
    population_text_entry = tk.Entry(outer_frame)
    population_text_entry.pack()
    population_search_button = tk.Button(outer_frame, text="Search", command=button_click)
    population_search_button.pack()


def create_map_widget() -> tkintermapview.TkinterMapView:
    # Map widget on bottom
    bottom_frame = tk.Frame(root, width=width, height=800, bg='grey')
    bottom_frame.grid(row=1, column=0, padx=5, pady=5)

    map_widget = tkintermapview.TkinterMapView(bottom_frame, width=width, height=1000, corner_radius=0)
    map_widget.set_position(41.3874, 2.1686)
    map_widget.set_zoom(12)
    map_widget.pack()
    return map_widget


if __name__ == "__main__":
    main()
