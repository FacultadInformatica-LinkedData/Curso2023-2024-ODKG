
import morph_kgc

CONFIG_MAPPING = "mappings/config.ini"
OUT_GRAPH = "rdf/University.ttl"

# Create a Graph
g = morph_kgc.materialize(CONFIG_MAPPING)

# Write Graph
with open(OUT_GRAPH, "w") as f:
    f.write(g.serialize(format="turtle"))
