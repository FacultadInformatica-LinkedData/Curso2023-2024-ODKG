#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[46]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[47]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[48]:


# TO DO
ns = Namespace("http://somewhere#")
#
print("SPARQL")
#for r in g.query(q1):
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT  ?sub  
  WHERE {
    ?sub rdfs:subClassOf ns:LivingThing.
  }  
  ''', initNs={"ns": ns}
                  )

for r in g.query(q1):
    print(r.sub)

#
print("RDFLib")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[49]:


# TO DO

print("SPARQL")

q2 = prepareQuery('''
  SELECT  ?instance  
  WHERE {
    {?sub rdfs:subClassOf* ns:Person.
    ?instance a ?sub}
  }  
  ''', initNs={"ns": ns}
                  )
# Visualize the results
for r in g.query(q2):
    print(r.instance)

print("with RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
        print(s1)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[50]:


# TO DO

print("SPARQL")
q3 = prepareQuery('''
    SELECT DISTINCT ?individual ?property ?value 
    WHERE {
        ?individual rdf:type ns:Person.
        
        ?individual ?property ?value.
        
    }
    ''', initNs={"ns": ns}
                 )
# Visualize the results

for r in g.query(q3):
    print(r.individual, r.property, r.value)
    
    
print("with RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s)
    for s0, p0, o0 in g.triples((s, None, None)):
        print(s0, p0, o0)


# In[51]:


# TO DO
q3 = prepareQuery('''
    SELECT DISTINCT ?individual ?property ?value 
    WHERE {
        ?individual rdf:type ns:Animal.
        
        ?individual ?property ?value.
        
    }
    ''', initNs={"ns": ns}
                 )
# Visualize the results

for r in g.query(q3):
    print(r.individual, r.property, r.value)
    
    
print("with RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Animal)):
    print(s)
    for s0, p0, o0 in g.triples((s, None, None)):
        print(s0, p0, o0)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[52]:


# TO DO
from rdflib import FOAF
from rdflib import XSD
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

print("SPARQL")
q4 = prepareQuery('''
  SELECT  DISTINCT ?individual ?Given  
  WHERE {
    ?individual foaf:knows ?RockySmith.
    ?RockySmith vcard:FN ?RockySmithFullName.
    ?individual vcard:Given ?Given.
  }  
  ''',
  initNs = { "foaf": FOAF, "ns": ns, "vcard":VCARD }
)
# Visualize the results

for r in g.query(q4, initBindings = {'?RockySmithFullName' : Literal('Rocky Smith', datatype=XSD.string)}):
    print(r.individual, r.Given)


# In[53]:


print("RDFLib")
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
    print(f"{s} knows {o}")
    for s0, p0, o0 in g.triples((s, VCARD.FN, None)):
        print(o0)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[54]:


print("SPARQL")
q5 = prepareQuery('''
SELECT ?subject ?FullName
WHERE {
  ?subject foaf:knows ?object1, ?object2.
  ?subject vcard:FN ?FullName.
  FILTER (?object1 != ?object2)
  
}
GROUP BY ?subject
HAVING (COUNT(?object1) + COUNT(?object2) >= 2)
''',
  initNs = { "foaf": FOAF, "vcard": VCARD, "xsd":XSD}
)
# Visualize the results

for r in g.query(q5):
    print(r.subject, r.FullName)
    


# In[55]:


# TO DO
from rdflib import Graph, Namespace, URIRef

print("RDFLib")
sujetos=[] #Todos los sujetos que conocen a alguien
sujetos_validos=[] #Los sujetos que conocen a al menos dos personas
for s, p, o in g.triples((None, FOAF.knows, None)):
    sujetos.append(s)
    print(f"{s} knows {o}")

sujetos_unicos=list(dict.fromkeys(sujetos))#Sujetos que conocen a alguien sin repetirse

for i in range(0, len(sujetos_unicos)):   
    x = sujetos.count(sujetos_unicos[i])
    if x>= 2:
        sujetos_validos.append(sujetos_unicos[i])
  

for sujeto in sujetos_validos:
    # Iterar sobre las tripletas donde el sujeto es el sujeto válido
    for s, p, o in g.triples((sujeto, VCARD.FN, None)):
        print(s,p,o)


# In[ ]:




