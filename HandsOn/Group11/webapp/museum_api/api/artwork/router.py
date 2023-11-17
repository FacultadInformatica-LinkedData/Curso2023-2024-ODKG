import rdflib
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from museum_api.api.artwork.responses import ArtworkResponse
from museum_api.data.data_loader import get_data_graph_object

artwork_router = APIRouter(prefix='/artwork')

ARTWORK_PROPERTIES = ["accession_number", "artist", "artist_role", "title", "art_medium", "credit_text", "made_in_year",
					  "acquired_in_year", "copyright_notice", "thumbnail_url", "url", "width", "height", "link", "artist_name"]


@artwork_router.get(
	"",
	responses={
		200: {
			"model": list[ArtworkResponse],
			"description": "Successfully read artworks"
		}
	},
	tags=["Artwork"],
	summary="Get artworks (filtered)",
)
async def api_endpoints_artwork_get(
		accession_number: str | None = None,
		artist: str | None = None,
		artist_role: str | None = None,
		title: str | None = None,
		art_medium: str | None = None,
		credit_text: str | None = None,
		made_in_year: str | None = None,
		acquired_in_year: str | None = None,
		copyright_notice: str | None = None,
		thumbnail_url: str | None = None,
		url: str | None = None,
		width: str | None = None,
		height: str | None = None,
		link: str | None = None,
		artist_name: str | None = None
) -> list[ArtworkResponse]:
	data_graph: rdflib.Graph = get_data_graph_object()

	query_params = locals()
	artwork_properties_filtered = [prop for prop in ARTWORK_PROPERTIES if prop in query_params]
	null_properties = [prop for prop in artwork_properties_filtered if query_params[prop] is None]

	query = """
		SELECT """ + (" ".join([f"?{prop}" for prop in null_properties])) + """
		WHERE {
		  ?artwork a sch:VisualArtwork .
		  ?artwork own:hasAccessionNumber """ + (
		f'"{accession_number}"' if accession_number is not None else "?accession_number") + """ .
		  ?artwork sch:artist """ + (f'"{artist}"' if artist is not None else "?artist") + """ .
		  ?artwork sch:hasArtistRole """ + (f'"{artist_role}"' if artist_role is not None else "?artist_role") + """ .
		  ?artwork sch:name """ + (f'"{title}"' if title is not None else "?title") + """ .
		  ?artwork sch:artMedium """ + (f'"{art_medium}"' if art_medium is not None else "?art_medium") + """ .
		  ?artwork sch:creditText """ + (f'"{credit_text}"' if credit_text is not None else "?credit_text") + """ .
		  ?artwork own:madeInYear """ + (f'{made_in_year}' if made_in_year is not None else "?made_in_year") + """ .
		  ?artwork own:acquiredInYear """ + (
				f'{acquired_in_year}' if acquired_in_year is not None else "?acquired_in_year") + """ .
		  ?artwork sch:copyrightNotice """ + (
				f'"{copyright_notice}"' if copyright_notice is not None else "?copyright_notice") + """ .
		  ?artwork sch:thumbnailUrl """ + (f'"{thumbnail_url}"' if thumbnail_url is not None else "?thumbnail_url") + """ .
		  ?artwork sch:url """ + (f'"{url}"' if url is not None else "?url") + """ .
		  ?artwork sch:width """ + (f'{width}' if width is not None else "?width") + """ .
		  ?artwork sch:height """ + (f'{height}' if height is not None else "?height") + """ .
		  ?artist owl:sameAs """ + (f'"{link}"' if link is not None else "?link") + """ .
		  ?artist vcard:FN ?artist_name . """ + (
			f'filter contains(?artist_name,"{artist_name}")' if artist_name is not None else "" 
	) + """}
		LIMIT 1000
	"""
	result = data_graph.query(query)

	non_null_properties = {
		prop: query_params[prop]
		for prop in artwork_properties_filtered if query_params[prop] is not None
	}

	response = []
	for row in result:
		row_object = {
			param_name: param_value
			for param_name, param_value in zip(null_properties, row)
		}
		complete_response = ArtworkResponse(**row_object, **non_null_properties)
		response.append(complete_response)

	return response
