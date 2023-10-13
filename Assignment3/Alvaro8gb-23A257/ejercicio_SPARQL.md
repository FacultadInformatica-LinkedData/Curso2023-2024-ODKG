# Exercise 1

1. Get all the properties that can be applied to instances of the Politician class (<http://dbpedia.org/ontology/Politician>)


```

PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?p
WHERE {
    ?x rdf:type dbo:Politician .
    ?x ?p ?z
}
LIMIT 10

```

Solution:

```xml
<rdf:RDF xmlns:res="http://www.w3.org/2005/sparql-results#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:nodeID="rset">
<rdf:type rdf:resource="http://www.w3.org/2005/sparql-results#ResultSet" />
    <res:resultVariable>p</res:resultVariable>
    <res:solution rdf:nodeID="r0">
      <res:binding rdf:nodeID="r0c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r1">
      <res:binding rdf:nodeID="r1c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2000/01/rdf-schema#label"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r2">
      <res:binding rdf:nodeID="r2c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2000/01/rdf-schema#comment"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r3">
      <res:binding rdf:nodeID="r3c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2002/07/owl#sameAs"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r4">
      <res:binding rdf:nodeID="r4c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/name"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r5">
      <res:binding rdf:nodeID="r5c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/topic"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r6">
      <res:binding rdf:nodeID="r6c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2007/05/powder-s#describedby"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r7">
      <res:binding rdf:nodeID="r7c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/homepage"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r8">
      <res:binding rdf:nodeID="r8c0"><res:variable>p</res:variable><res:value rdf:resource="http://purl.org/dc/terms/subject"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r9">
      <res:binding rdf:nodeID="r9c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/isPrimaryTopicOf"/></res:binding>
    </res:solution>
  </rdf:Description>
</rdf:RDF>

```


2. Get all the properties, except rdf:type, that can be applied to instances of the Politician class http://dbpedia.org/ontology/Politician>

```

PREFIX dbo: <http://dbpedia.org/ontology/>


SELECT DISTINCT ?p
WHERE {
    ?x rdf:type dbo:Politician .
    ?x ?p ?z .
    FILTER (?p != rdf:type)
}
LIMIT 10
```

Solution:
```xml

<rdf:RDF xmlns:res="http://www.w3.org/2005/sparql-results#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:nodeID="rset">
<rdf:type rdf:resource="http://www.w3.org/2005/sparql-results#ResultSet" />
    <res:resultVariable>p</res:resultVariable>
    <res:solution rdf:nodeID="r0">
      <res:binding rdf:nodeID="r0c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2000/01/rdf-schema#label"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r1">
      <res:binding rdf:nodeID="r1c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2000/01/rdf-schema#comment"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r2">
      <res:binding rdf:nodeID="r2c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2002/07/owl#sameAs"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r3">
      <res:binding rdf:nodeID="r3c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/name"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r4">
      <res:binding rdf:nodeID="r4c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/topic"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r5">
      <res:binding rdf:nodeID="r5c0"><res:variable>p</res:variable><res:value rdf:resource="http://www.w3.org/2007/05/powder-s#describedby"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r6">
      <res:binding rdf:nodeID="r6c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/homepage"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r7">
      <res:binding rdf:nodeID="r7c0"><res:variable>p</res:variable><res:value rdf:resource="http://purl.org/dc/terms/subject"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r8">
      <res:binding rdf:nodeID="r8c0"><res:variable>p</res:variable><res:value rdf:resource="http://xmlns.com/foaf/0.1/isPrimaryTopicOf"/></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r9">
      <res:binding rdf:nodeID="r9c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/gabinete"/></res:binding>
    </res:solution>
  </rdf:Description>
</rdf:RDF>

```

3. Which different values exist for the properties, except for rdf:type, applicable to the instances of Politician?

```

PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?z
WHERE {
    ?x rdf:type dbo:Politician .
    ?x ?p ?z
    FILTER (?p != rdf:type)
}

LIMIT 10

```


Solution:

```xml

<rdf:RDF xmlns:res="http://www.w3.org/2005/sparql-results#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:nodeID="rset">
<rdf:type rdf:resource="http://www.w3.org/2005/sparql-results#ResultSet" />
    <res:resultVariable>z</res:resultVariable>
    <res:solution rdf:nodeID="r0">
      <res:binding rdf:nodeID="r0c0"><res:variable>z</res:variable><res:value xml:lang="es">Adame Ba Konaré</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r1">
      <res:binding rdf:nodeID="r1c0"><res:variable>z</res:variable><res:value xml:lang="es">Adriano Sánchez Roa</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r2">
      <res:binding rdf:nodeID="r2c0"><res:variable>z</res:variable><res:value xml:lang="es">Adrián Ward</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r3">
      <res:binding rdf:nodeID="r3c0"><res:variable>z</res:variable><res:value xml:lang="es">Agustín Haya de la Torre de la Rosa</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r4">
      <res:binding rdf:nodeID="r4c0"><res:variable>z</res:variable><res:value xml:lang="es">Agustín Molina Martínez</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r5">
      <res:binding rdf:nodeID="r5c0"><res:variable>z</res:variable><res:value xml:lang="es">Ahmed Hilmi Pasha</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r6">
      <res:binding rdf:nodeID="r6c0"><res:variable>z</res:variable><res:value xml:lang="es">Aileen Baviera</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r7">
      <res:binding rdf:nodeID="r7c0"><res:variable>z</res:variable><res:value xml:lang="es">Aisha Musa el-Said</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r8">
      <res:binding rdf:nodeID="r8c0"><res:variable>z</res:variable><res:value xml:lang="es">Akua Asabea Ayisi</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r9">
      <res:binding rdf:nodeID="r9c0"><res:variable>z</res:variable><res:value xml:lang="es">Alain Vivien</res:value></res:binding>
    </res:solution>
  </rdf:Description>
</rdf:RDF>


```

4. For each of these applicable properties, except for rdf:type, which different values do they take globally for all those instances?

you should get all the possible values of all the possible properties (except for rdf:type) that are applicable to instances of the class Politician.

```
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?p (GROUP_CONCAT(DISTINCT ?z; SEPARATOR=";")) AS ?values_of_p
WHERE {
    ?x rdf:type dbo:Politician .
    ?x ?p ?z .
    FILTER (?p != rdf:type)
}
GROUP BY ?p
LIMIT 10

```

Solution:

```xml
<rdf:RDF xmlns:res="http://www.w3.org/2005/sparql-results#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:nodeID="rset">
<rdf:type rdf:resource="http://www.w3.org/2005/sparql-results#ResultSet" />
    <res:resultVariable>p</res:resultVariable>
    <res:resultVariable>values_of_p</res:resultVariable>
    <res:solution rdf:nodeID="r0">
      <res:binding rdf:nodeID="r0c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/sitioweb"/></res:binding>
      <res:binding rdf:nodeID="r0c1"><res:variable>values_of_p</res:variable><res:value>Página oficial www.amylkaracosta.net;http://blogdehermogenes.blogspot.com/;http://christianengstrom.wordpress.com/;http://www.camara.cl/camara/diputado_detalle.aspx%3Fprmid=812;http://www.fmorande.com/;http://www.gladysmarin.cl/;https://mobile.twitter.com/elianecapobianc%3Flang=es;https://web.archive.org/web/20100120162516/http:/www.albertocienfuegos.cl/;https://web.archive.org/web/20120306155424/http:/xn--b1aaebccb4c.xn--d1abbgf6aiiy.xn--p1ai/;www.pirque.cl</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r1">
      <res:binding rdf:nodeID="r1c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/lugarNacimiento"/></res:binding>
      <res:binding rdf:nodeID="r1c1"><res:variable>values_of_p</res:variable><res:value>http://es.dbpedia.org/resource/España;http://es.dbpedia.org/resource/Leganés;http://es.dbpedia.org/resource/Madrid</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r2">
      <res:binding rdf:nodeID="r2c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/cargo"/></res:binding>
      <res:binding rdf:nodeID="r2c1"><res:variable>values_of_p</res:variable><res:value>;( por Entre Rios );(Constituyente de 1917);(Encargado );(Interino );11;111;13;15;17;18;2;20;21;22;23;3;30;34;35;37;4;40;48;5;6;60;8;99;Administrador Regional de la región de Antofagasta;Alcalde de Alcalá de Guadaíra;Alcalde de Knoxville;Autoridad de carreteras;Candidato a vicepresidente de Argentina;Cargo Permanente;Cargo protocolar;Concejal de Puente Alto;Concejal de la Ciudad de Mendoza;Concejal de la ciudad de Avellaneda;Concejal del Ayuntamiento de Benidorm;Concejal del Ayuntamiento de Pontevedra;Consejero Regional de O&#39;Higgins;Consejero de Sanidad del Gobierno de Euzkadi;Consejero regional de O&#39;Higgins;Coordinador general de Izquierda Unida de Aragón;Delegado Federal de la Secretaría de Gobernación;Diputada del Parlamento de Andalucía;Diputado Federal de la Cámara de Diputados de México;Diputado al Congreso de la República de Venezuela;Diputado al Congreso de la Unión;Diputado al Congreso de la Unión de México;Diputado de la Asamblea Legislativa de Costa Rica;Diputado de la Provincia de Entre Ríos;Diputado de la República de Chile al Primer Congreso Nacional de Chile;Diputado de las Cortes Valencianas;Diputado de las Cortes de Aragón;Diputado del Parlamento de Andalucía;Diputado del Parlamento de Galicia;Diputado en el Congreso;Diputado en las Cortes Generales;Director de la Seguridad del Estado;Elección: 25 de abril de 1954;Embajador de Argentina en Paraguay;Embajador de Chile ante la OCDE;Gobernador civil de Las Palmas;Gobernador civil de León;Gobernador civil de Zaragoza;Gobernador civil de la provincia de Las Palmas;Gobernador civil de la provincia de León;Gobernador de San Juan;Gobernador de Tennessee;Gobernador de Wisconsin;Gobernador de la Provincia de Quito;Gobernador de la provincia de Antofagasta;Gobernador del Valle del Cauca;Intendente de la Ciudad de Mendoza;Interino;Jefe Supremo del Estado de Honduras;Jefe de la Comisión Permanente de secretarios de Estado y de subsecretarios;Líder del Parti Québécois;Magister equitum;Mayoría relativa;Miembro del Parlamento Europeo por Suecia;Ministro de Asuntos Exteriores de la Unión Soviética;Ministro de Educación de Israel;Ministro plenipotenciario, encargado de Negocios y embajador de Chile en Europa;Ministro sin Cartera;Oficial Mayor de la Secretaría de Gobernación;Oficial Mayor del Departamento del Distrito Federal;Periodista liberal, secretario municipal de Avilés en el 1908;Portavoz del Grupo Popular en;Presidenta del Parlamento de Andalucía;Presidente Honorable Concejo Deliberante de la Ciudad de Mendoza;Presidente de Blanco y Negro;Presidente de la AFE;Presidente de la Real Audiencia;Presidente del Consejo Regional de O&#39;Higgins;Presidente del Consejo de Estado de la República Socialista de Rumania;Presidente del Partido Popular de la Comunidad Valenciana;Presidente del Partido Socialdemócrata de Alemania;Presidente del Real Instituto Elcano;Presidente interino;Primer Ministro de Toda Palestina;Primer ministro de Malta;Regidor de la Municipalidad de San José;Regidor por el Partido del Trabajo;Secretario de Administración de Gobierno;Senador al Congreso de la Unión de México;Senador de las Cortes Generales de España;Senador de los Estados Unidos;Senador en las Cortes Generales;Senadora de las Cortes Generales de España;Senadora en las Cortes Generales;Tribuno consular;Tribuno consular II;Tribuno consular III;Verdugo titular de la Audiencia de Burgos;Viceprimer Ministro;de la Provincia de Tucumán;de la República Argentina;el Congreso de los Diputados;http://es.dbpedia.org/resource/Abjasia;http://es.dbpedia.org/resource/Alcalde_de_Huelva;http://es.dbpedia.org/resource/Alcalde_de_Madrid;http://es.dbpedia.org/resource/Alcaldía_de_Bucaramanga;http://es.dbpedia.org/resource/Anexo:Alcaldes_de_Huancayo;http://es.dbpedia.org/resource/Anexo:Alcaldes_de_Peñaflor_(Chile);http://es.dbpedia.org/resource/Anexo:Alcaldes_de_Pirque;http://es.dbpedia.org/resource/Anexo:Alcaldes_de_Torrelavega;http://es.dbpedia.org/resource/Anexo:Dux_de_Venecia;http://es.dbpedia.org/resource/Anexo:Embajadores_del_Perú_en_Estados_Unidos;http://es.dbpedia.org/resource/Anexo:Gobernadores_coloniales_de_Chile;http://es.dbpedia.org/resource/Anexo:Gobernadores_de_Tucumán;http://es.dbpedia.org/resource/Anexo:Gobernadores_de_la_provincia_de_Formosa;http://es.dbpedia.org/resource/Anexo:Gobernadores_del_Caquetá;http://es.dbpedia.org/resource/Anexo:Gobernadores_regionales_de_Huancavelica;http://es.dbpedia.org/resource/Anexo:Gobernadores_regionales_de_San_Martín;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Jalisco;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Nayarit;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Nicaragua;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Querétaro;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_San_Luis_Potosí;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Sinaloa;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Tamaulipas;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Veracruz;http://es.dbpedia.org/resource/Anexo:Gobernantes_de_Yucatán;http://es.dbpedia.org/resource/Anexo:Ministros_de_Asuntos_Exteriores_de_España;http://es.dbpedia.org/resource/Anexo:Ministros_de_Fomento_de_España;http://es.dbpedia.org/resource/Anexo:Presidente_del_Senado_de_Colombia;http://es.dbpedia.org/resource/Anexo:Presidentes_de_El_Salvador;http://es.dbpedia.org/resource/Anexo:Presidentes_de_Filipinas;http://es.dbpedia.org/resource/Arquidiócesis_de_Sucre;http://es.dbpedia.org/resource/Asamblea_Constituyente_de_Bolivia_de_2006;http://es.dbpedia.org/resource/Asamblea_Legislativa_Plurinacional_de_Bolivia;http://es.dbpedia.org/resource/Asamblea_Nacional_de_Gobiernos_Regionales;http://es.dbpedia.org/resource/Audiencia_Provincial_de_Albacete;http://es.dbpedia.org/resource/Ayuntamiento_de_Bilbao;http://es.dbpedia.org/resource/Ayuntamiento_de_Madrid;http://es.dbpedia.org/resource/Ayuntamiento_de_Maruri;http://es.dbpedia.org/resource/Benidorm;http://es.dbpedia.org/resource/Bloque_Nacionalista_Galego;http://es.dbpedia.org/resource/Canciller_de_Alemania;http://es.dbpedia.org/resource/Capitán_general_de_Chile;http://es.dbpedia.org/resource/Casa_de_Moneda_de_México;http://es.dbpedia.org/resource/Centro_de_Comercio_Internacional_(organismo_internacional);http://es.dbpedia.org/resource/Comisión_Nacional_de_Libros_de_Texto_Gratuitos;http://es.dbpedia.org/resource/Congreso_de_Paraguay;http://es.dbpedia.org/resource/Congreso_de_la_República_del_Perú;http://es.dbpedia.org/resource/Consejería_de_Empleo,_Formación_y_Trabajo_Autónomo_de_la_Junta_de_Andalucía;http://es.dbpedia.org/resource/Consejo_de_Estado_(España);http://es.dbpedia.org/resource/Consejo_de_la_Magistratura_(Argentina);http://es.dbpedia.org/resource/Corregimiento_de_Santiago;http://es.dbpedia.org/resource/Cortes_de_la_Restauración;http://es.dbpedia.org/resource/Cámara_de_Diputadas_y_Diputados_de_Chile;http://es.dbpedia.org/resource/Cámara_de_Diputados_de_la_Nación_Argentina;http://es.dbpedia.org/resource/Cámara_de_Representantes_de_los_Estados_Unidos;http://es.dbpedia.org/resource/Cámara_de_Senadores_(Uruguay);http://es.dbpedia.org/resource/Departamento_de_Alto_Paraná;http://es.dbpedia.org/resource/Diócesis_de_San_Pedro;http://es.dbpedia.org/resource/Eidgenössische_Sammlung;http://es.dbpedia.org/resource/Embajada_de_Estados_Unidos_en_Afganistán;http://es.dbpedia.org/resource/Embajada_de_Estados_Unidos_en_Argentina;http://es.dbpedia.org/resource/Embajada_de_Estados_Unidos_en_México;http://es.dbpedia.org/resource/Facultad_de_Humanidades_y_Ciencias_de_la_Educación_(Universidad_de_la_República);http://es.dbpedia.org/resource/Federal_(Entre_Ríos);http://es.dbpedia.org/resource/Frente_Nacional_(Suiza);http://es.dbpedia.org/resource/General_director_de_Carabineros_de_Chile;http://es.dbpedia.org/resource/Gobernador_de_Campeche;http://es.dbpedia.org/resource/Gobernador_de_Santander;http://es.dbpedia.org/resource/Gobernador_de_la_Provincia_de_Catamarca;http://es.dbpedia.org/resource/Gobernador_de_la_provincia_de_Mendoza;http://es.dbpedia.org/resource/Gobernantes_de_Honduras;http://es.dbpedia.org/resource/Historia_de_los_ministerios_de_Trabajo_de_España;http://es.dbpedia.org/resource/Instituto_Nacional_de_Deportes_de_Chile;http://es.dbpedia.org/resource/Intendente_de_la_región_de_Los_Ríos;http://es.dbpedia.org/resource/Jefe_de_Gobierno_de_Túnez;http://es.dbpedia.org/resource/Juez_asociado_de_la_Corte_Suprema_de_los_Estados_Unidos;http://es.dbpedia.org/resource/Junta_de_Andalucía;http://es.dbpedia.org/resource/Junta_de_Gobierno_de_Chile_(1823);http://es.dbpedia.org/resource/Juventudes_Comunistas_de_Chile;http://es.dbpedia.org/resource/MAS_Región;http://es.dbpedia.org/resource/Ministerio_de_Agricultura,_Ganadería_y_Pesca_(Argentina);http://es.dbpedia.org/resource/Ministerio_de_Agricultura_y_Desarrollo_Rural;http://es.dbpedia.org/resource/Ministerio_de_Asuntos_Exteriores_de_Sudán;http://es.dbpedia.org/resource/Ministerio_de_Desarrollo_Rural_y_Tierras;http://es.dbpedia.org/resource/Ministerio_de_Desarrollo_Social_y_Familia;http://es.dbpedia.org/resource/Ministerio_de_Empleo_y_Seguridad_Social;http://es.dbpedia.org/resource/Ministerio_de_Fomento_y_Obras_Públicas_del_Perú;http://es.dbpedia.org/resource/Ministerio_de_Industria,_Comercio_y_Turismo;http://es.dbpedia.org/resource/Ministerio_de_Justicia_(España);http://es.dbpedia.org/resource/Ministerio_de_Justicia_y_Derechos_Humanos_(Chile);http://es.dbpedia.org/resource/Ministerio_de_Minas_y_Energía_(Colombia);http://es.dbpedia.org/resource/Ministerio_de_Relaciones_Exteriores_(Chile);http://es.dbpedia.org/resource/Ministerio_de_Relaciones_Exteriores_(Israel);http://es.dbpedia.org/resource/Ministerio_de_Relaciones_Exteriores_de_Uruguay;http://es.dbpedia.org/resource/Ministerio_de_Trabajo_y_Seguridad_Social_(Uruguay);http://es.dbpedia.org/resource/Ministerio_de_Transportes_y_Telecomunicaciones;http://es.dbpedia.org/resource/Ministerio_de_Turismo_(Israel);http://es.dbpedia.org/resource/Ministerio_de_Ultramar;http://es.dbpedia.org/resource/Ministerio_del_Deporte_(Chile);http://es.dbpedia.org/resource/Ministerio_del_Interior;http://es.dbpedia.org/resource/Ministerio_del_Interior_(Argentina);http://es.dbpedia.org/resource/Ministerio_del_Interior_(Uruguay);http://es.dbpedia.org/resource/Ministerio_del_Interior_y_Seguridad_Pública_(Chile);http://es.dbpedia.org/resource/Ministerios_de_Economía_de_España;http://es.dbpedia.org/resource/Ministro_de_Asuntos_Exteriores_de_España;http://es.dbpedia.org/resource/Ministro_de_Comercio_Exterior_y_Turismo_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Desarrollo_e_Inclusión_Social_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Economía_y_Finanzas_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Justicia_y_Derechos_Humanos_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Relaciones_Exteriores_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Trabajo_y_Promoción_del_Empleo_del_Perú;http://es.dbpedia.org/resource/Ministro_de_Transporte_de_Israel;http://es.dbpedia.org/resource/Ministro_de_la_Suprema_Corte_de_Justicia_de_la_Nación_(México);http://es.dbpedia.org/resource/Misión_Permanente_de_México_ante_la_Unión_Europea_y_Bélgica;http://es.dbpedia.org/resource/Misión_Permanente_de_México_en_Estados_Unidos;http://es.dbpedia.org/resource/Partido_Comunista_Rumano;http://es.dbpedia.org/resource/Partido_Comunista_de_Chile;http://es.dbpedia.org/resource/Partido_Guatemalteco_del_Trabajo;http://es.dbpedia.org/resource/Partido_de_los_Trabajadores_de_Kurdistán;http://es.dbpedia.org/resource/Poder_Ejecutivo_de_Honduras;http://es.dbpedia.org/resource/Portavoz_del_Gobierno_de_España;http://es.dbpedia.org/resource/Presidente_de_Checoslovaquia;http://es.dbpedia.org/resource/Presidente_de_Chile;http://es.dbpedia.org/resource/Presidente_de_Colombia;http://es.dbpedia.org/resource/Presidente_de_Filipinas;http://es.dbpedia.org/resource/Presidente_de_Francia;http://es.dbpedia.org/resource/Presidente_de_Mauritania;http://es.dbpedia.org/resource/Presidente_de_Nicaragua;http://es.dbpedia.org/resource/Presidente_de_Rusia;http://es.dbpedia.org/resource/Presidente_de_la_Corte_Suprema_del_Perú;http://es.dbpedia.org/resource/Presidente_de_la_Cámara_de_Diputadas_y_Diputados_de_Chile;http://es.dbpedia.org/resource/Presidente_de_la_Cámara_de_Diputados_de_México;http://es.dbpedia.org/resource/Presidente_de_la_Generalidad_Valenciana;http://es.dbpedia.org/resource/Presidente_de_la_Junta_Nacional_de_Gobierno_de_Chile;http://es.dbpedia.org/resource/Presidente_de_la_Suprema_Corte_de_Justicia_de_la_Nación_(México);http://es.dbpedia.org/resource/Presidente_de_los_Estados_Unidos_Mexicanos;http://es.dbpedia.org/resource/Presidente_del_Comité_Central_del_Partido_Comunista_de_China;http://es.dbpedia.org/resource/Presidente_del_Consejo_de_Ministros_del_Perú;http://es.dbpedia.org/resource/Presidente_del_Ecuador;http://es.dbpedia.org/resource/Presidente_del_Gobierno_de_Rusia;http://es.dbpedia.org/resource/Presidente_del_Perú;http://es.dbpedia.org/resource/Presidente_pro_tempore_de_la_Unasur;http://es.dbpedia.org/resource/Primer_Ministro_de_Sudáfrica;http://es.dbpedia.org/resource/Primer_ministro_de_Checoslovaquia;http://es.dbpedia.org/resource/Primer_ministro_de_Costa_de_Marfil;http://es.dbpedia.org/resource/Primer_ministro_de_Francia;http://es.dbpedia.org/resource/Primer_ministro_de_Irak;http://es.dbpedia.org/resource/Primer_ministro_de_Japón;http://es.dbpedia.org/resource/Primer_ministro_de_Rumania;http://es.dbpedia.org/resource/Primera_dama_de_Costa_Rica;http://es.dbpedia.org/resource/Primera_dama_de_Ecuador;http://es.dbpedia.org/resource/Primera_dama_de_Malí;http://es.dbpedia.org/resource/Primera_dama_de_los_Estados_Unidos;http://es.dbpedia.org/resource/Renania_del_Norte-Westfalia;http://es.dbpedia.org/resource/Riksdag;http://es.dbpedia.org/resource/Rusia_Unida;http://es.dbpedia.org/resource/Secretario_general_del_Comité_Central_del_Partido_Comunista_de_China;http://es.dbpedia.org/resource/Secretaría_de_Derechos_Humanos_(Argentina);http://es.dbpedia.org/resource/Secretaría_de_Educación_Pública_(México);http://es.dbpedia.org/resource/Secretaría_de_Estado_de_Empleo;http://es.dbpedia.org/resource/Secretaría_de_Gobernación_(México);http://es.dbpedia.org/resource/Segunda_dama_de_los_Estados_Unidos;http://es.dbpedia.org/resource/Senado_de_Chile;http://es.dbpedia.org/resource/Senado_de_la_Nación_Argentina;http://es.dbpedia.org/resource/Senado_de_la_República_de_Colombia;http://es.dbpedia.org/resource/Senado_de_la_República_de_Venezuela;http://es.dbpedia.org/resource/Senado_de_los_Estados_Unidos;http://es.dbpedia.org/resource/Subsecretaría_General_de_Gobierno_de_Chile;http://es.dbpedia.org/resource/Subsecretaría_de_Redes_Asistenciales_de_Chile;http://es.dbpedia.org/resource/Subsecretaría_del_Medio_Ambiente_de_Chile;http://es.dbpedia.org/resource/Superintendencia_de_Isapres_de_Chile;http://es.dbpedia.org/resource/Tegucigalpa;http://es.dbpedia.org/resource/Universidad_Nacional_de_Costa_Rica;http://es.dbpedia.org/resource/Unión_Cívica_Radical;http://es.dbpedia.org/resource/Unión_General_de_Trabajadores;http://es.dbpedia.org/resource/VIII_legislatura_de_España;http://es.dbpedia.org/resource/VII_legislatura_de_España;http://es.dbpedia.org/resource/VI_legislatura_de_España;http://es.dbpedia.org/resource/Veracruz;http://es.dbpedia.org/resource/Vicepresidente_de_Guatemala;http://es.dbpedia.org/resource/Vicepresidente_de_la_Nación_Argentina;por Federal</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r3">
      <res:binding rdf:nodeID="r3c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/2data"/></res:binding>
      <res:binding rdf:nodeID="r3c1"><res:variable>values_of_p</res:variable><res:value>1940;Año de aliyá</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r4">
      <res:binding rdf:nodeID="r4c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/isbn"/></res:binding>
      <res:binding rdf:nodeID="r4c1"><res:variable>values_of_p</res:variable><res:value>0;84;8487204198;968;9681609018;970;978;9780691101019;9780914710844;9781850653868;9786079001063;9788434004610;9788489666214;9788497172127;9789684523906;9789707681118</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r5">
      <res:binding rdf:nodeID="r5c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/capítulo"/></res:binding>
      <res:binding rdf:nodeID="r5c1"><res:variable>values_of_p</res:variable><res:value>Capitulo B;El Oriente Medio de la segunda posguerra: Revolución y Panarabismo;Los años recientes. 1964-1976</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r6">
      <res:binding rdf:nodeID="r6c0"><res:variable>p</res:variable><res:value rdf:resource="http://dbpedia.org/ontology/wikiPageID"/></res:binding>
      <res:binding rdf:nodeID="r6c1"><res:variable>values_of_p</res:variable><res:value>1024267;1029203;1056176;106272;107629;1093939;1146517;1152132;1155290;1176673;1177936;1180515;1221382;123625;1240361;13178;1324986;133279;1355637;1380259;1382590;1448420;1460025;146378;149285;1593573;1598077;160797;1613535;1673619;172082;1739698;1749854;1839976;1843987;1868718;19541;202272;2067902;2113105;213315;2134188;2180976;2194174;2237364;2305368;2308940;2311852;2312484;2313149;2314901;2340266;2350565;2563506;2625882;2636174;2642650;2662347;2760530;2815344;2842959;285706;2944907;2996478;3007593;3022263;3026546;311712;317771;3339579;3358415;338239;341490;3584408;3595392;359594;3743538;3787605;3832383;3847353;4026909;409451;4139319;4176956;4201716;4215143;4223325;4229579;4231226;423778;4339565;4362937;4384395;4388334;4464825;4492590;4526697;4565909;4566903;4621263;4744649;48927;49392;512131;5172779;5352525;548101;554424;588146;590503;610473;623165;626685;6290889;646241;6549092;667038;671598;687037;700826;729324;734826;751650;756014;7617151;77925;799377;813677;874642;9040654;9056947;907378;9088680;9090625;9105364;9110852;9113267;9116194;9149801;9150559;9159782;9170408;9193795;9195047;9205722;92081;9224667;9229463;9243445;9244297;924820;9249617;9262629;9263422;9277237;9285069;929518;9295633;9307865;9324037;9332710;9340072;9346338;9355045;9366782;9366829;9374218;9374834;9375497;9378402;9385780;9392364;9395911;9397606;9414726;9416666;9423055;9430793;9436616;9440923;9452536;9580295;96537;982871</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r7">
      <res:binding rdf:nodeID="r7c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/cónyuge"/></res:binding>
      <res:binding rdf:nodeID="r7c1"><res:variable>values_of_p</res:variable><res:value>(Lucía Carrillo Gutiérrez );(María Izaguirre );; ; Miguel Ángel Morales;Abogado;Ana Coll Juliá;Ana Emilia del Carmen Nogueira Cifuentes;Ana María Correa;Andrea Vicuña;Beatriz Elena Arreaza Arreaza;Bebé Vicuña;Brian Burke;Carola Zúñiga;Carolina Isaza de Lourido;Cecilia Báez Palacios;Cesárea Rosa Carrera Ponce de León y Moyano Cornejo;Claudette Toupin;Crissy Garrett Haslam;Darsy González;Desconocida;Dominique Ouattara;Dora Crespo Quinones;Dora Pawlikowski Andrade;Esther Racedo;Fabiana Calleja;Gustavo Vidal  ; Carlos Videla  ; Miguel Ángel Morales;Hana Benešová;Hildur Fredrika Abenius;Inés Castro Salinas;Isabel Labra;Isabel Riquelme Vera;Jacinta Trueba Barrera / Alicia Vargas García;Jorge Muñoz Poutays;Judith Gaxiola de Valdés;Leonor María de Osorio;Liliana Belando;Loreto Barros;Margaret Millward Blood;Maria Louw;Maria del Pilar Gonzalez;Martha Bayona;Martha Van Tonder;Maruja Pujols de Pérez;María Elmira Bohórquez Núñez;María Fernanda Flores de Alemán;María Inés Garcés Escalona;María Julia Rosa Johnson Ureta;María Magdaleno;María Soledad Vial Valdés;María Walker Linares;María del Carmen Fernández de Córdova y Álvarez de las Asturias-Bohorques;María del Carmen Gutiérrez de Quintanilla Flores;María del Rosario Echecopar Rey;Micaela del Castillo;Mónica Terrada;Nydia Restrepo;Pablo Guarino;Sandra Milena Farfán Varón;Shoshana Eban;Sylvia Spikin Urrutia;Teresa Tenorio Santacruz;http://es.dbpedia.org/resource/Adriana_Bortolozzi;http://es.dbpedia.org/resource/Amice_de_Gael;http://es.dbpedia.org/resource/Cónyuge;http://es.dbpedia.org/resource/Ellen_Vesta_Emery_Hamlin;http://es.dbpedia.org/resource/Fanny_Roger;http://es.dbpedia.org/resource/Hilaria_del_Rosario;http://es.dbpedia.org/resource/José_Figueres_Ferrer;http://es.dbpedia.org/resource/Li_Zhao;http://es.dbpedia.org/resource/Maria_Alexe;http://es.dbpedia.org/resource/María_Agoncillo;http://es.dbpedia.org/resource/María_Francisca_de_la_Gándara_de_Calleja;http://es.dbpedia.org/resource/Micaela_Josefa_Quezada_Borjas;http://es.dbpedia.org/resource/Nanuli_Shevardnadze;http://es.dbpedia.org/resource/Nina_Katzir;http://es.dbpedia.org/resource/Rafael_Correa</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r8">
      <res:binding rdf:nodeID="r8c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/enlaceautor"/></res:binding>
      <res:binding rdf:nodeID="r8c1"><res:variable>values_of_p</res:variable><res:value>Carlos Sabino;Dennis Deletant;Gerald H. Meaker;John Julius Norwich;José Amodia;Juan Avilés Farré;Julio Zárate;Paul Heywood</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r9">
      <res:binding rdf:nodeID="r9c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/tamaño"/></res:binding>
      <res:binding rdf:nodeID="r9c1"><res:variable>values_of_p</res:variable><res:value>150;170;180;185;190;200;220;240;250;260;270;300</res:value></res:binding>
    </res:solution>
  </rdf:Description>
</rdf:RDF>
```

Solutio

5. For each of these applicable properties, except for rdf:type, how many distinct values do they take globally for all those instances?


```

PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?p (COUNT(DISTINCT ?z)) AS ?counting_vals
WHERE {
    ?x rdf:type dbo:Politician .
    ?x ?p ?z .
    FILTER (?p != rdf:type)
}
GROUP BY ?p
LIMIT 10

```

Solution:

```xml

<rdf:RDF xmlns:res="http://www.w3.org/2005/sparql-results#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:nodeID="rset">
<rdf:type rdf:resource="http://www.w3.org/2005/sparql-results#ResultSet" />
    <res:resultVariable>p</res:resultVariable>
    <res:resultVariable>counting_vals</res:resultVariable>
    <res:solution rdf:nodeID="r0">
      <res:binding rdf:nodeID="r0c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/vuelta"/></res:binding>
      <res:binding rdf:nodeID="r0c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r1">
      <res:binding rdf:nodeID="r1c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/luganac"/></res:binding>
      <res:binding rdf:nodeID="r1c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">2</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r2">
      <res:binding rdf:nodeID="r2c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/urlmorto"/></res:binding>
      <res:binding rdf:nodeID="r2c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r3">
      <res:binding rdf:nodeID="r3c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/autores"/></res:binding>
      <res:binding rdf:nodeID="r3c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r4">
      <res:binding rdf:nodeID="r4c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/branch"/></res:binding>
      <res:binding rdf:nodeID="r4c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r5">
      <res:binding rdf:nodeID="r5c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/nombreEnEspañol"/></res:binding>
      <res:binding rdf:nodeID="r5c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">2</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r6">
      <res:binding rdf:nodeID="r6c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/precedesor"/></res:binding>
      <res:binding rdf:nodeID="r6c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r7">
      <res:binding rdf:nodeID="r7c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/fechaDeFalleciemiento"/></res:binding>
      <res:binding rdf:nodeID="r7c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">1</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r8">
      <res:binding rdf:nodeID="r8c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/caption"/></res:binding>
      <res:binding rdf:nodeID="r8c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">10</res:value></res:binding>
    </res:solution>
    <res:solution rdf:nodeID="r9">
      <res:binding rdf:nodeID="r9c0"><res:variable>p</res:variable><res:value rdf:resource="http://es.dbpedia.org/property/posiciónTítulo"/></res:binding>
      <res:binding rdf:nodeID="r9c1"><res:variable>counting_vals</res:variable><res:value datatype="http://www.w3.org/2001/XMLSchema#integer">3</res:value></res:binding>
    </res:solution>
  </rdf:Description>
</rdf:RDF>
```

