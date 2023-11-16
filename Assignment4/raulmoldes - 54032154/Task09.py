# %% [markdown]
# **Task 09: Data linking**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL
from rdflib.plugins.sparql import prepareQuery
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

# %% [markdown]
# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# %%
#Set the namespace
ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")
VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')

#Iterate over the individuals of the first graph that have a nickname
for s1,p1,o1 in g1.triples((None,VCARD.Given,None)):

    #Iterate over the individuals on the second graph that have the same nickname
    for s2,p2,o2 in g2.triples((None,VCARD.Given,o1)):

        #Check if they have also the same Family name
        if str(g1.value(s1, VCARD.Family)) == str(g2.value(s2, VCARD.Family)):
        
            #If the condition is true, set the `OWL:sameAs` property for those individuals on graph 3
            g3.add((s1, OWL.sameAs, s2))

            print(f"Found similarity between {s1} from graph 1 and {s2} from graph 2")



# %% [markdown]
# Print all the elements from graph 3 that have the property `OWL:sameAs` using `SPARQL`

# %%
#Bindings
g3.bind('owl',OWL)
#query text
query_text = '''
SELECT ?subject ?object
    WHERE{
    ?subject owl:sameAs ?object.
    }
'''
#prepare the query
query = prepareQuery(query_text,initNs={'owl':OWL})

#Visualize the results
for row in g3.query(query):
    print(f"Similarity between: {row[0]} and {row[1]}")


