from pydantic import BaseModel


class ArtworkResponse(BaseModel):
	accession_number: str
	artist: str
	artist_role: str
	title: str
	art_medium: str
	credit_text: str
	made_in_year: str
	acquired_in_year: str
	copyright_notice: str
	thumbnail_url: str
	url: str
	width: str
	height: str
	link: str
