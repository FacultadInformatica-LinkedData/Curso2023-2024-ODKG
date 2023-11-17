Run the app by running the _main()_ function in app.py

There are 4 main ways to interact with the app
- **Cabins by contaminant name:** enter the name of a contaminant e.g. sulfur dioxide, ozone. Once clicking the corresponding 'Display' button, a pop up with some information about the contaminant such as its mass and effect will appear. Once closing the window, on the map, a marker will appear for each air quality cabin which measures that contaminant. Each cabin is labelled by its cabin number.
- **Cabins by population threshold**: enter the population threshold e.g. 20000. Once clicking the 'Display' button, on the map, a marker will appear every cabin located in a neighbourhood with a population meeting or exceeding the threshold. This uses the knowledge graph to traverse through the address and then neighbourhood corresponding to a cabin.
- **Trees by species** e.g. enter the name of a tree species e.g. Yucca gigantea. Once clicking the 'Display' button, on the map, a marker will appear for each tree of that species.
- **Temperatures (start end month)**: enter the start year, end year and month e.g. 1850 1960 Apr. Once clicking the 'View' button, a pop-up window with a scatter plot will appear with year on the x-axis and temperature on the y-axis. The years selected should be in the range 1780 - 2020 and the month should be the standard 3 letter abbreviation. 


