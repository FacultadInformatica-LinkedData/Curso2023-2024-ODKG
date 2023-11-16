from pydantic import BaseModel, HttpUrl

from typing import Sequence


# TO DO & TO CHANGE: implement the structure of the returned results
class ChargingStation(BaseModel):
    # id: int
    # name: str
    # city: str
    # dbpedia_city: HttpUrl
    pass


class StationSearchResults(BaseModel):
    # results: Sequence[ChargingStation]
    pass
