13
# Analysis
- The analysis.html file does not contain the license of the dataset to be generated.
# Ontology
- The ontology presents serialization issues; is not a valid Turtle file. Do not create ontologies by hand; use some tool.
- The ontology does not follow the resource naming strategy defined in the analysis.
- The namespaces are wrong.
- The defined datatype properties are not correct.
- In OWL, there are object properties (where value of the property is a resource) and datatype properties (where the value of the property is a string literal, usually typed). 
- Check that all class names start with capital letter.
# RDF data
- URIs are encoded as strings.
- Datatypes are missing.
- Classes are used as properties.
- The values of agendafechaInicio are wrong.
- Solve the character encoding issues.
# Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
