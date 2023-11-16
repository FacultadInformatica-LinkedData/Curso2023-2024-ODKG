# %% [markdown]
# **Task 06: Modifying RDF(s)**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# Read the RDF file as shown in class

# %%
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, FOAF
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
# TO DO
# Visualize the results
g.add((ns.University,RDF.type,RDFS.Class))
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# %%
# TO DO
# Visualize the results
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**

# %%
# TO DO
#Create the individual Jane Smith
individual1 = URIRef("http://somewhere#JaneSmith")
#Add the individual as an instance of Class Researcher
g.add((individual1, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**

# %%
# TO DO
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
# Add the properties to the individual JaneSmith
g.add((individual1, FOAF.mbox, Literal('janesmith@gmail.com')))
g.add((individual1, VCARD.FN, Literal('Jane Smith')))
g.add((individual1, VCARD.Given, Literal('Jane')))
g.add((individual1, VCARD.Family, Literal('Smith')))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# %% [markdown]
# **TASK 6.5: Add UPM as the university where John Smith works**

# %%
# TO DO
#Create instance of University with name UPM
upm = URIRef("https://www.upm.es/")
g.add((upm, RDF.type, ns.UNIVERSITY))

#Add upm as John smith's working place
g.add((ns.JohnSmith, FOAF.workplaceHomepage, upm))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**

# %%
# TO DO
g.add((ns.JohnSmith,FOAF.knows,ns.JaneSmith))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


