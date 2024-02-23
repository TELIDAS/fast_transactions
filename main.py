from fastapi import FastAPI

from api.endpoints.rates import router

app = FastAPI()

app.include_router(router, prefix="/api")
