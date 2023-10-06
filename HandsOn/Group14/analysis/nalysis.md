## Data Analysis
The following document presents the analysis made to the selected datasets.

### Datasets
The topic of the selected datasets are describe next:

* [200342-0-centros-dia.csv](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=22bceca8a5a03410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default): Municipal and subsidized day centers in the city of Madrid specialized in elderly care.

### Exploratory Data Analysis (EDA)
The exploratory data analysis can be found in the `analysis` folder. The notebook `analysis.ipynb` gathers the necessary code for creating the reports regarding the data types and ranges for each variable. From this analysis we can extract some conclusions as expressed next:

* The variables regarding the specifics attributes of the addresses like `PUERTA` and `ESCALERA` have a high percentage of nulity so they aren't going to be used in the ontology we are building.
* Variables like `HORARIO` and `TRANSPORTE` need to be preprocessed before being added to the ontology.

### Data Source's Licensing
Each of the selected datasets are edited by the City of Madrid, while the responsibles for the data are described next:

* `200342-0-centros-dia.csv`: General Directorate for the Elderly (*Dirección General de Mayores*).

Regarding the [licences of each of the datasets and its conditions of use](https://datos.madrid.es/egob/catalogo/aviso-legal), all of them can be use for commercial and non-commercial purposes subject to the acknowledgment of source's authority.

We haven't found a specific license of the dataset. All the information related with the use of data provided by the Madrid City council shows that it's an open license. However, they didn't refer to a specific license.

#### Condition of re-use

1. It is forbidden to denature the data meaning.
2. The data source must be indicated in the documents which reuse information. This indication can be made in the following way: "Data origin: Madrid City Council (or the corresponding organ or entity)."
3. The last update date must be mentioned in the documents which reuse information, as long as this is included in the original document.
4. It is not allowed to indicate, insinuate or suggest that Madrid City Council participates, patronizes or supports the reutilization carried out with the information.
5. Metadata must be kept unaltered and complete about the reutilization date and the usage condition in the available for reutilization document. 
6. In the cases of anonimized data for the sake of Personal Data Protection, it is expressly forbiden to carry out task of re-identification, using whichever other present, past or future data sources.

#### Applicable legislation
Open Data is a global initiative linked to the Open Government policies, which intends that data and information in power of public administrations
 are published in an open, regular and reusable way for everybody, without restrictions of access, copyright, patents or other control mechanisms.

**European level**

- [Directive (EU) 2019/1024](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019L1024)

**National level**

- [Real Decreto-ley 24/2021, de 2 de noviembre, de transposición de la Directiva (UE) 2019/1024 de datos abiertos y reutilización de la información del sector público](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2021-17910)

- [Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público.](https://www.boe.es/buscar/act.php?id=BOE-A-2007-19814)

- [Real Decreto 1495/2011, de 24 de octubre, por el que se desarrolla la Ley 37/2007, de 16 de noviembre](https://www.boe.es/buscar/act.php?id=BOE-A-2011-17560)
- [Norma Técnica de Interoperabilidad de Reutilización de recursos de la información](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2013-2380)
- [Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno](https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887)

- [Ley 18/2015, de 9 de julio, por la que se modifica la Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público](https://www.boe.es/buscar/doc.php?id=BOE-A-2015-7731)

**Regional level**

- [Ley 10/2019, de 10 de abril, de Transparencia y de Participación de la Comunidad de Madrid.](https://www.boe.es/buscar/act.php?id=BOE-A-2019-10102)

**Local level**

- [Ordenanza de Transparencia de la Ciudad de Madrid, de 27 de julio de 2016](https://sede.madrid.es/FrameWork/generacionPDF/ANM2016_108.pdf?idNormativa=3eabe8e52c796510VgnVCM1000001d4a900aRCRD&nombreFichero=ANM2016_108&cacheKey=163)

### Resource Naming Strategy (RNS)
The Resource Naming Strategy follows the following rules:

* Base domain: `https://miciudadamiga.madrid/`
* Path: `map/`
* Ontological Term Path: `https://miciudadamiga.madrid/map/ontology#[classOrPropertyName]`
* Individuals Path: `https://miciudadamiga.madrid/map/resource/[className]/[identifier]`
    * Metro: `https://miciudadamiga.madrid/map/resource/SubwayStation/[identifier]`
    * District: `https://miciudadamiga.madrid/map/resource/MadridDistrict/[identifier]`
    * Neighborhood: `https://miciudadamiga.madrid/map/resource/MadridNeighborhood/[identifier]`
    * Day Center: `https://miciudadamiga.madrid/map/resource/DayCenter/[identifier]`

Some examples of specific use cases are shown below:

* https://miciudadamiga.madrid/map/ontology#DayCenter
* https://miciudadamiga.madrid/map/ontology#belongsToMadridNeighborhood
* https://miciudadamiga.madrid/map/resource/SubwayStation/Legazpi
* https://miciudadamiga.madrid/map/resource/MadridDistrict/76