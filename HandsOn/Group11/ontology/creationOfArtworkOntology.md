# Artwork Ontology

We couldn't find an ontology that could fit our properties for Artwork so I created one. I created the URLs so they could all be available in the searching bar.
Here are our properties, and their URLs :
# Artwork Ontology

This ontology defines a model for artworks and related entities. Below are the key properties, object properties, and classes with their corresponding URLs:

## Classes:

1. **Artwork**
   - [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Type: Class

2. **ArtworkDimension**
   - [https://soum2111.github.io/ArtworkDimension](https://soum2111.github.io/ArtworkDimension)
   - Type: Class

## Object Properties:

1. **hasArtist**
   - [https://soum2111.github.io/hasArtist](https://soum2111.github.io/hasArtist)
   - Type: Object Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [https://soum2111.github.io/Artist](https://soum2111.github.io/Artist)

2. **hasMedium**
   - [https://soum2111.github.io/hasMedium](https://soum2111.github.io/hasMedium)
   - Type: Object Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

## Properties:

1. **hasId**
   - [https://soum2111.github.io/hasId](https://soum2111.github.io/hasId)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#integer](http://www.w3.org/2001/XMLSchema#integer)

2. **hasAccessionNumber**
   - [https://soum2111.github.io/hasAccessionNumber](https://soum2111.github.io/hasAccessionNumber)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

3. **hasArtist**
   - [https://soum2111.github.io/hasArtist](https://soum2111.github.io/hasArtist)
   - Type: Object Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [https://soum2111.github.io/Artist](https://soum2111.github.io/Artist)

4. **hasArtistRole**
   - [https://soum2111.github.io/hasArtistRole](https://soum2111.github.io/hasArtistRole)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

5. **hasTitle**
   - [https://soum2111.github.io/hasTitle](https://soum2111.github.io/hasTitle)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

6. **hasMedium**
   - [https://soum2111.github.io/hasMedium](https://soum2111.github.io/hasMedium)
   - Type: Object Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

7. **hasCreditLine**
   - [https://soum2111.github.io/hasCreditLine](https://soum2111.github.io/hasCreditLine)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

8. **madeInYear**
   - [https://soum2111.github.io/madeInYear](https://soum2111.github.io/madeInYear)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#integer](http://www.w3.org/2001/XMLSchema#integer)

9. **acquiredInYear**
   - [https://soum2111.github.io/acquiredInYear](https://soum2111.github.io/acquiredInYear)
   - Type: Datatype Property
   - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
   - Range: [http://www.w3.org/2001/XMLSchema#integer](http://www.w3.org/2001/XMLSchema#integer)

10. **hasDimension**
    - [https://soum2111.github.io/hasDimension](https://soum2111.github.io/hasDimension)
    - Type: Object Property
    - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
    - Range: [https://soum2111.github.io/ArtworkDimension](https://soum2111.github.io/ArtworkDimension)

11. **hasInscription**
    - [https://soum2111.github.io/hasInscription](https://soum2111.github.io/hasInscription)
    - Type: Datatype Property
    - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
    - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

12. **hasThumbnailCopyright**
    - [https://soum2111.github.io/hasThumbnailCopyright](https://soum2111.github.io/hasThumbnailCopyright)
    - Type: Datatype Property
    - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
    - Range: [http://www.w3.org/2001/XMLSchema#string](http://www.w3.org/2001/XMLSchema#string)

13. **hasThumbnailUrl**
    - [https://soum2111.github.io/hasThumbnailUrl](https://soum2111.github.io/hasThumbnailUrl)
    - Type: Datatype Property
    - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
    - Range: [http://www.w3.org/2001/XMLSchema#anyURI](http://www.w3.org/2001/XMLSchema#anyURI)

14. **hasUrl**
    - [https://soum2111.github.io/hasUrl](https://soum2111.github.io/hasUrl)
    - Type: Datatype Property
    - Domain: [https://soum2111.github.io/Artwork](https://soum2111.github.io/Artwork)
    - Range: [http://www.w3.org/2001/XMLSchema#anyURI](http://www.w3.org/2001/XMLSchema#anyURI)
