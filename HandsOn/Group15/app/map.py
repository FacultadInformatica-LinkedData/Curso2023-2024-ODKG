from typing import List

import tkintermapview
import tkinter as tk


def add_marker(map_widget: tkintermapview.TkinterMapView, latitude: float, longitude: float, text: str,
               icon_filename="air-quality.png"):
    """
    Renders a marker on a map widget.
    :param map_widget:
    :param latitude:
    :param longitude:
    :param text:
    :param icon_filename: the filename of the icon to use for the marker
    :return:
    """
    icon = tk.PhotoImage(file=icon_filename)
    map_widget.set_marker(latitude, longitude, text=text, icon=icon)


def add_markers(map_widget: tkintermapview.TkinterMapView, latitudes: List[float], longitudes: List[float],
                texts: List[str], icon_filename="air-quality.png"):
    """
    Renders a list of markers on a map widget.
    :param map_widget: map to render markers on
    :param latitudes: list of latitudes of markers
    :param longitudes: list of longitudes of markers
    :param texts: list of texts of markers
    :param icon_filename: the filename of the icon to use for the markers

    :return: None
    """

    for latitude, longitude, text in zip(latitudes, longitudes, texts):
        add_marker(map_widget, latitude, longitude, text, icon_filename)
