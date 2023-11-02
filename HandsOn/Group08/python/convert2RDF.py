
import morph_kgc
from globals import CONFIG_MAPPING, CONFIG_MAPPING_LINKS, OUT_GRAPH, OUT_GRAPH_LINKS


# Without linking


# Create a Graph
g = morph_kgc.materialize(CONFIG_MAPPING)

# Write Graph
with open(OUT_GRAPH, "w", encoding='utf8') as f:
    f.write(g.serialize(format="nt"))


# Create a Graph
g = morph_kgc.materialize(CONFIG_MAPPING_LINKS)
# withlinking
with open(OUT_GRAPH_LINKS, "w", encoding='utf8') as f:
    f.write(g.serialize(format="turtle"))
