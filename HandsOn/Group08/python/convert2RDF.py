
import morph_kgc
from globals import CONFIG_MAPPING, CONFIG_MAPPING_LINKS, OUT_GRAPH, OUT_GRAPH_LINKS, CONFIG_MAPPING_UPDATED, OUT_GRAPH_UPDATED


# Without linking


# Create a Graph
g = morph_kgc.materialize(CONFIG_MAPPING)

with open(OUT_GRAPH, "w", encoding='utf8') as f:
    f.write(g.serialize(format="nt"))


# With links

g_with_links = morph_kgc.materialize(CONFIG_MAPPING_LINKS)

with open(OUT_GRAPH_LINKS, "w", encoding='utf8') as f:
    f.write(g_with_links.serialize(format="turtle"))


# Updated

g_with_updated = morph_kgc.materialize(CONFIG_MAPPING_UPDATED)

with open(OUT_GRAPH_UPDATED, "w", encoding='utf8') as f:
    f.write(g_with_updated.serialize(format="turtle"))
