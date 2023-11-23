9
# Analysis
- The definition of the resource naming strategy is not complete.
- The analysis.html file does not contain the license of the dataset to be generated.
# Ontology
- The ontology presents serialization issues; is not a valid Turtle file.
- The namespaces used in the ontology are wrong.
- The xsd datatypes defined in the ontology do not exist.
- In OWL, having multiple domains (or ranges) means that the domain (or range) is the intersection of all the classes.  The current definitions of properties with multiple domains are wrong.
- The domain and/or range of some property is not defined.
# RDF data
- Verify that the class and property names used in the RDF data are the same as those used in the ontology.
- The classes defined in the ontology are not used in the RDF data.
- There are no object properties in the RDF data.
# Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
