
import morph_kgc
from globals import CONFIG_MAPPING, CONFIG_MAPPING_LINKS, OUT_GRAPH, OUT_GRAPH_LINKS


# Without linking
g = morph_kgc.materialize(CONFIG_MAPPING)

with open(OUT_GRAPH, "w", encoding='utf8') as f:
    f.write(g.serialize(format="nt"))


print("\n"*2, "-"*20, "\n"*2)

# With links

g_with_links = morph_kgc.materialize(CONFIG_MAPPING_LINKS)

with open(OUT_GRAPH_LINKS, "w", encoding='utf8') as f:
    f.write(g.serialize(format="turtle"))
