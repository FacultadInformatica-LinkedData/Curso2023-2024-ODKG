14
# Analysis
- The description of the resource naming strategy is incomplete.
# Ontology
- The ontology does not follow a proper resource naming strategy.
- The XML Schema datatypes are not correctly written.
- In OWL, having multiple domains (or ranges) means that the domain (or range) is the intersection of all the classes.  The current definitions of properties with multiple domains are wrong.
- The domain and/or range of some property is not defined.
- The class BikeID in fact represents the bike itself; all that information should be on the bike.
- The class BikeType should not be used only for defining a string. If it is only for that, just use a datatype property.
# RDF data
- Verify that the class and property names used in the RDF data are the same as those used in the ontology.
- Properties are related to classes in a way that is not consistent with the ontology.
- Review the values; for example longitude and latitude are wrong.
# Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
