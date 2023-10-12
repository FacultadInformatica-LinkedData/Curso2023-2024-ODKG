#%% md
# **Task 06: Modifying RDF(s)**
#%%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"
#%% md
# Read the RDF file as shown in class
#%%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")
#%% md
# Create a new class named Researcher
#%%
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)
#%% md
# **TASK 6.1: Create a new class named "University"**
# 
#%%
# TO DO
# Visualize the results
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)
#%% md
# **TASK 6.2: Add "Researcher" as a subclass of "Person"**
#%%
# TO DO
# Visualize the results
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
for s, p, o in g:
  print(s,p,o)
#%% md
# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**
#%%
# TO DO
# Visualize the results
g.add((ns.JaneSmith, RDF.type, ns.Researcher))
for s, p, o in g:
  print(s,p,o)
#%% md
# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**
#%%
# TO DO
# Visualize the results
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

g.add((ns.JaneSmith, VCARD.EMAIL, Literal("janesmith@email.com")))
g.add((ns.JaneSmith, VCARD.FN, Literal("Jane Smith")))
g.add((ns.JaneSmith, VCARD.Given, Literal("Jane")))
g.add((ns.JaneSmith, VCARD.Family, Literal("Smith")))

for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s, p, o)
#%% md
# **TASK 6.5: Add UPM as the university where John Smith works**
#%%
# TO DO
# Visualize the results
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, VCARD.WorkPlace, ns.UPM))

for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s, p, o)
#%% md
# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**
#%%
# TO DO
# Visualize the results
from rdflib import FOAF

g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))
for s, p, o in g.triples((None, FOAF.knows, None)):
    print(s, p, o)