# Importing necessary libraries for web application setup
import json
import random
from datetime import date
from datetime import datetime
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.responses import StreamingResponse

from app.controllers import indicators_controller, news_controller, sheets_controller, indicators_entry_controller, \
    global_setting_controller, report_controller, driver_controller
# from app.controllers import sheets_controller
# Importing specific scrapping services
from app.controllers.new_profile_controller import test_create_notice
from app.services.db_service import DatabaseService
from app.services.driver.news_crud import create_new
from .env import env
from .services.diariocolatino import DiarioColatinoScrapper
from .services.diarioelmundo import DiarioElMundoScrapper
from .services.diarioelsalvador import DiarioElSalvadorScrapper
from .services.elsalvador import ElSalvadorScraper

# Initializing FastAPI application
app = FastAPI()

# INIT DATABASE
DatabaseService()

# Setting up environment variables
env.set_env()

# Defining origins for CORS
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:4200"
]
add_pagination(app)
# Configuring CORS middleware
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


app.include_router(driver_controller.router)
app.include_router(indicators_controller.router)
app.include_router(news_controller.router)
app.include_router(sheets_controller.router)
app.include_router(global_setting_controller.router)
app.include_router(indicators_entry_controller.router)
app.include_router(report_controller.router)

add_pagination(app)

if __name__ == '__main__':
    print("TEST JOIN")
