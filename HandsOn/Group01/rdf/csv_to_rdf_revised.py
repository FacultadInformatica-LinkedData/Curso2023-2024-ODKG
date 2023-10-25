import os
import pandas as pd
import rdflib
import re
from rdflib import RDF, RDFS, XSD, Literal
from tqdm import tqdm


# Separate a camelCased word
def split_camel_case(text):
    if text == "TV":
        return text
    else:
        return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)





def preprocess_for_uri(value):
    # Split camel case
    split_text = split_camel_case(str(value))

    # Convert to URI-friendly format
    return split_text.replace(" ", "_")


def create_rdf_graph():
    # Create RDF graph
    g = rdflib.Graph()

    # Namespaces from residuos.yml
    nso = rdflib.Namespace("http://madridwastemanagement.org/group01/ontology/")

    # Namespaces from ontology.ttl
    base = rdflib.Namespace("http://madridwastemanagement.org/")
    xsd = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")

    # Bind them to the graph
    g.bind("rdf", RDF)
    g.bind("nso", nso)
    g.bind("rdfs", RDFS)
    g.bind("xsd", xsd)

    return g, nso


def add_classes_to_graph(g, nso):
    # Define Namespaces for each class
    Zone = nso.Zone
    WasteType = nso.WasteType
    District = nso.District
    Total = nso.Total
    Year = nso.Year
    Month = nso.Month

    # Zone
    g.add((Zone, RDF.type, RDFS.Class))

    # WasteType
    g.add((WasteType, RDF.type, RDFS.Class))

    # District
    g.add((District, RDF.type, RDFS.Class))

    # Total
    g.add((Total, RDF.type, RDFS.Class))

    # Year
    g.add((Year, RDF.type, RDFS.Class))

    # Month
    g.add((Month, RDF.type, RDFS.Class))



def add_properties_to_graph(g, nso):
    # Define properties
    zoneID = nso.zoneID
    hasDistrict = nso.hasDistrict
    districtID = nso.districtID
    districtName = nso.districtName
    hasResidue = nso.hasResidue
    wasteName = nso.wasteName
    hasTotal = nso.hasTotal
    value = nso.value
    referedTo = nso.referedTo
    hasYear = nso.hasYear
    hasMonth = nso.hasMonth

    # Now, add property definitions to the graph:

    # zoneID
    g.add((zoneID, RDF.type, RDF.Property))
    g.add((zoneID, RDFS.domain, nso.Zone))
    g.add((zoneID, RDFS.range, XSD.integer))

    # hasDistrict
    g.add((hasDistrict, RDF.type, RDF.Property))
    g.add((hasDistrict, RDFS.domain, nso.Zone))
    g.add((hasDistrict, RDFS.range, nso.District))

    # districtID
    g.add((districtID, RDF.type, RDF.Property))
    g.add((districtID, RDFS.domain, nso.District))
    g.add((districtID, RDFS.range, XSD.integer))

    # districtName
    g.add((districtName, RDF.type, RDF.Property))
    g.add((districtName, RDFS.domain, nso.District))
    g.add((districtName, RDFS.range, XSD.string))

    # hasResidue
    g.add((hasResidue, RDF.type, RDF.Property))
    g.add((hasResidue, RDFS.domain, nso.District))
    g.add((hasResidue, RDFS.range, nso.WasteType))

    # wasteName
    g.add((wasteName, RDF.type, RDF.Property))
    g.add((wasteName, RDFS.domain, nso.WasteType))
    g.add((wasteName, RDFS.range, XSD.string))

    # hasTotal
    g.add((hasTotal, RDF.type, RDF.Property))
    g.add((hasTotal, RDFS.domain, nso.WasteType))
    g.add((hasTotal, RDFS.range, nso.Total))

    # value
    g.add((value, RDF.type, RDF.Property))
    g.add((value, RDFS.domain, nso.Total))
    g.add((value, RDFS.range, XSD.float))

    # referedTo
    g.add((referedTo, RDF.type, RDF.Property))
    g.add((referedTo, RDFS.domain, nso.Total))
    g.add((referedTo, RDFS.range, nso.District))

    # hasYear
    g.add((hasYear, RDF.type, RDF.Property))
    g.add((hasYear, RDFS.domain, nso.Total))
    g.add((hasYear, RDFS.range, nso.Year))

    # hasMonth
    g.add((hasMonth, RDF.type, RDF.Property))
    g.add((hasMonth, RDFS.domain, nso.Total))
    g.add((hasMonth, RDFS.range, nso.Month))


def create_triples(df, g, nso):
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Creating triples"):
        """----------------------URIs for each entity--------------------------"""
        zone_uri = rdflib.URIRef(f"{nso}data/Zone/{preprocess_for_uri(row['Zone'])}")
        district_uri = rdflib.URIRef(f"{nso}data/District/{preprocess_for_uri(row['District'])}")
        wasteType_uri = rdflib.URIRef(f"{nso}data/WasteType/{preprocess_for_uri(row['WasteType'])}")
        total_uri = rdflib.URIRef(
            f"{nso}data/Total/{preprocess_for_uri(row['WasteType'])}_{preprocess_for_uri(row['District'])}_{preprocess_for_uri(row['Year'])}_{preprocess_for_uri(row['Month'])}")
        year_uri = rdflib.URIRef(f"{nso}data/Year/{preprocess_for_uri(row['Year'])}")
        month_uri = rdflib.URIRef(f"{nso}data/Month/{preprocess_for_uri(row['Month'])}")
        name_uri = rdflib.URIRef(f"{nso}data/Name/{preprocess_for_uri(row['Name'])}")  # Add URI for Name

        """----------------------Data properties---------------------------------"""

        # Zone data properties
        zone_id_literal = Literal(row['Zone'], datatype=XSD.integer)

        if not (zone_uri, nso['zoneID'], zone_id_literal) in g:
            g.add((zone_uri, nso['zoneID'], zone_id_literal))
            g.add((zone_uri, RDFS.label, Literal(f"Zone {row['Zone']}")))

        # District data properties
        district_id_literal = Literal(row['District'], datatype=XSD.integer)

        if not (district_uri, nso['districtID'], district_id_literal) in g:
            g.add((district_uri, nso['districtID'], district_id_literal))


        district_name_literal = Literal(row['Name'], datatype=XSD.string)

        if not (district_uri, nso['districtName'], district_name_literal) in g:
            g.add((district_uri, nso['districtName'], district_name_literal))
            g.add((district_uri, RDFS.label, Literal(f'District {district_id_literal}')))


        # WasteType data properties
        wasteType_literal = Literal(row['WasteType'], datatype=XSD.string)

        if not (wasteType_uri, nso['wasteName'], wasteType_literal) in g:
            g.add((wasteType_uri, nso['wasteName'], wasteType_literal))
            g.add((wasteType_uri, RDFS.label, Literal(row['WasteType'])))

        # Total data properties
        total_value_literal = Literal(row['Total'], datatype=XSD.float)
        total_label_literal = Literal(
            f"Total for {row['WasteType']} in District {row['District']} for {row['Year']}-{row['Month']}: {row['Total']}")

        if not (total_uri, nso['value'], None) in g:
            g.add((total_uri, nso['value'], total_value_literal))
            g.add((total_uri, RDFS.label, total_label_literal))
            g.add((total_uri, nso['hasYear'], year_uri))
            g.add((total_uri, nso['hasMonth'], month_uri))

        # Year data properties
        year_literal = Literal(row['Year'], datatype=XSD.integer)

        if not (year_uri, RDF.type, nso['Year']) in g.triples((year_uri, RDF.type, None)):
            g.add((year_uri, RDF.type, nso['Year']))
            g.add((year_uri, RDFS.label, year_literal))

        # Month data properties
        month_label = Literal(row['Month'], datatype=XSD.string)

        if not (month_uri, RDF.type, nso['Month']) in g.triples((month_uri, RDF.type, None)):
            g.add((month_uri, RDF.type, nso['Month']))
            g.add((month_uri, RDFS.label, month_label))



        """----------------------Entity relationships---------------------------------"""

        g.add((zone_uri, RDF.type, nso['Zone']))
        g.add((zone_uri, nso['hasDistrict'], district_uri))

        # District relationships
        g.add((district_uri, RDF.type, nso['District']))
        g.add((district_uri, nso['hasResidue'], wasteType_uri))

        # WasteType relationships
        g.add((wasteType_uri, RDF.type, nso['WasteType']))
        g.add((wasteType_uri, nso['hasTotal'], total_uri))


        # Total relationships
        g.add((total_uri, RDF.type, nso['Total']))
        g.add((total_uri, nso['referedTo'], district_uri))
        g.add((total_uri, nso['hasYear'], year_uri))

        # Year relationships
        g.add((year_uri, RDF.type, nso['Year']))

        # Month relationships
        g.add((month_uri, RDF.type, nso['Month']))



def main():
    # Load and preprocess data
    csv_path = "Residuos_2021_2023-updated.csv"

    try:
        print("Serialization  1 in progress")
        df = pd.read_csv(csv_path)

        g, nso = create_rdf_graph()

        add_classes_to_graph(g, nso)

        add_properties_to_graph(g, nso)

        create_triples(df, g, nso)

        # Save RDF graph to a file
        rdf_path = "Residuos_2021_2023-updated_3.ttl"  # Change extension to .ttl for Turtle format
        g.serialize(destination=rdf_path, format="turtle")  # Use 'turtle' format
        print(f"RDF graph saved to {rdf_path}")
    except FileNotFoundError:
        print("Please try again with a valid path.")
    try:
        print("Serialization 2 in progress")
        df = pd.read_csv(csv_path)

        g, nso = create_rdf_graph()

        add_classes_to_graph(g, nso)

        add_properties_to_graph(g, nso)

        create_triples(df, g, nso)

        # Save RDF graph to a file
        rdf_path = "Residuos_2021_2023-updated_3.nt"  # Change extension to .nt for N-Triples format
        g.serialize(destination=rdf_path, format="nt")  # Use 'nt' format
        print(f"RDF graph saved to {rdf_path}")
    except FileNotFoundError:
        print("Please try again with a valid path.")


if __name__ == "__main__":
    main()
