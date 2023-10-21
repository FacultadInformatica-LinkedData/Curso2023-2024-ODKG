# %% [markdown]
# **Task 06: Modifying RDF(s)**

# %%
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"
# %% [markdown]
# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

# %% [markdown]
# Create a new class named Researcher

# %%
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.1: Create a new class named "University"**
#

# %%
g.add((ns.University, RDF.type, RDFS.Class))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# %%
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**

# %%
g.add((ns.JaneSmith, RDF.type, ns.Researcher))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.4: Add to the individual JaneSmith the fullName, given and family names**

# %%
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.add((ns.JaneSmith, VCARD.FN, Literal('Jane Smith', datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Given, Literal('Jane', datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Family, Literal('Smith', datatype=XSD.string)))

# Visualize the results
for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s,p,o)

# %% [markdown]
# **TASK 6.5: Add UPM as the university where John Smith works**

# %%
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, ns.Work, ns.UPM))

# Visualize the results
for s, p, o in g.triples((None, None, ns.UPM)):
  print(s,p,o)