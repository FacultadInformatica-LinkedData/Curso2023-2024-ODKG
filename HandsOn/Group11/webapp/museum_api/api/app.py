from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from museum_api.data.data_loader import get_data_graph_object
from museum_api.api.artwork.router import artwork_router


app = FastAPI(
    title="Museum app REST API",
    description="Museum app REST API",
    version='0.1.0',
    docs_url="/api/ui",
    on_startup=[get_data_graph_object]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix='/api')
api_router.include_router(artwork_router)

app.include_router(api_router)
