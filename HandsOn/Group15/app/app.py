import tkinter as tk

import tkintermapview

from map import add_markers

root = tk.Tk()
width, height = 1500, 1000
root.geometry(f"{width}x{height}")
root.title("Barcelona Environmental Monitoring")
root.config(bg="skyblue")


def main():
    create_input_frame()
    map_widget = create_map_widget()
    latitudes = [41.3, 41.4, 41.5]
    longitudes = [2.1, 2.2, 2.3]
    texts = ["Yum", "Madrid", "Valencia"]
    add_markers(map_widget, latitudes, longitudes, texts)

    # run the GUI
    root.mainloop()


def create_input_frame():
    def button_click():
        print(text_entry.get())

    # Make the top frame cover the whole width of the root
    top_frame = tk.Frame(root, width=width, height=200, bg='grey')
    top_frame.grid(row=0, column=0, padx=5, pady=5)

    title = tk.Label(top_frame, text="Barcelona Environmental Monitoring", font=("Arial", 20))
    title.pack()
    text_entry = tk.Entry(top_frame)
    text_entry.pack()
    button = tk.Button(top_frame, text="Search", command=button_click)
    button.pack()


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
