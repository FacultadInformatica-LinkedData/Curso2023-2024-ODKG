
import morph_kgc
from globals import CONFIG_MAPPING, OUT_GRAPH, OUT_GRAPH_LINKS


# Without linking 


# Create a Graph
g = morph_kgc.materialize(CONFIG_MAPPING)

# Write Graph
with open(OUT_GRAPH, "w", encoding='utf8') as f:
    f.write(g.serialize(format="nt"))


exit()
#withlinking 
with open(OUT_GRAPH_LINKS, "w", encoding='utf8') as f:
    f.write(g.serialize(format="turtle"))
