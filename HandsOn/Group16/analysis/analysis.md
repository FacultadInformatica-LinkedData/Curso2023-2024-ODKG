## Data AnalysisData Analysis
Datasets
The topic of the selected datasets are describe next:

desfibriladores_externos_fuera_ambito_sanitario.csv: A dataset that collects the location of defibrillators located outside the health area in the Region of Madrid.
Exploratory Data Analysis 
The exploratory data analysis can be found in the analysis folder. The notebook analysis.ipynb gathers the necessary code for creating the reports regarding the data types and ranges for each variable. From this analysis we can extract some conclusions as expressed next:

The address of the building containing the defibrilator is separated in several columns (direccion_via_codigo, direccion_via_nombre, etc.). A unique variable will be made, merging these serparated columns.
Variables like horario_acceso and direccion_via_nombre need to be preprocessed before being added to the ontology.
Data Source’s Licensing
Each of the selected datasets are edited by the Region of Madrid, while the responsibles for the data are described next:

desfibriladores_externos_fuera_ambito_sanitario.csv: Directorate General for Health Inspection and Organisation (Dirección General de Inspección y Ordenación Sanitaria).
Each dataset offered in the Open Data service of the Region of Madrid indicates the specific licence that applies to it. In general, the datasets are published under the terms of the Creative Commons - Attribution (CC-BY 4.0) licence, which allows:

copy, distribute and publicly disseminate.
serve as the basis for derivative works as a result of their analysis or study.
be used for commercial or non-commercial purposes, provided that such use does not constitute a public administrative activity.
modify, transform and adapt.
The authorship of the Region of Madrid must be mentioned.
Notwithstanding the above, the datasets of the Regional Transport Consortium of the Region of Madrid have different and personalised licences according to their peculiarities, the description of which appears in each dataset. In this case the desfibriladores_externos_fuera_ambito_sanitario.csv's license,Creative Commons Attribution, can be revised clicking here.

Applicable legislation
Open Data is a global initiative linked to the Open Government policies, which intends that data and information in power of public administrations are published in an open, regular and reusable way for everybody, without restrictions of access, copyright, patents or other control mechanisms.

European level

Directive (EU) 2019/1024
National level

Real Decreto-ley 24/2021, de 2 de noviembre, de transposición de la Directiva (UE) 2019/1024 de datos abiertos y reutilización de la información del sector público

Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público.

Real Decreto 1495/2011, de 24 de octubre, por el que se desarrolla la Ley 37/2007, de 16 de noviembre

Norma Técnica de Interoperabilidad de Reutilización de recursos de la información

Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno

Ley 18/2015, de 9 de julio, por la que se modifica la Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público

Regional level

Ley 10/2019, de 10 de abril, de Transparencia y de Participación de la Comunidad de Madrid.
Local level

Ordenanza de Transparencia de la Ciudad de Madrid, de 27 de julio de 2016
Data-licensing
We decided to use a CC0 license for our data, since it waives copyright and database protection, we saw fit to use this kind of license to trully make Open Data and allow any user to make applications based on this data.

Creative Commons: CC0

Resource Naming Strategy (RNS)
Base domain: http://ext.defibrilator/
Path: map/
Ontological Term Path: https://miciudadamiga.madrid/map/ontology#[classOrPropertyName]
Individuals Path: https://miciudadamiga.madrid/map/resource/[className]/[identifier]
Metro: https://miciudadamiga.madrid/map/resource/SubwayStation/[identifier]
District: https://miciudadamiga.madrid/map/resource/MadridDistrict/[identifier]
Neighborhood: https://miciudadamiga.madrid/map/resource/MadridNeighborhood/[identifier]
Day Center: https://miciudadamiga.madrid/map/resource/DayCenter/[identifier]
Some examples of specific use cases are shown below:

https://miciudadamiga.madrid/map/ontology#DayCenter
https://miciudadamiga.madrid/map/ontology#belongsToMadridNeighborhood
https://miciudadamiga.madrid/map/resource/SubwayStation/Legazpi
https://miciudadamiga.madrid/map/resource/MadridDistrict/76