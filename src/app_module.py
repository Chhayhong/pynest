from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from nest.core import PyNestFactory, Module
from .account.account_module import AccountModule
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.organization.organization_module import OrganizationModule
from src.event_management.event_management_module import EventManagementModule
from fastapi.middleware.cors import CORSMiddleware
import os
from src.event_attendee_management.event_attendee_management_module import (
    EventAttendeeManagementModule,
)
from src.event_organizer.event_organizer_module import EventOrganizerModule


@Module(
    imports=[
        AccountModule,
        OrganizationModule,
        EventManagementModule,
        EventAttendeeManagementModule,
        EventOrganizerModule,
    ],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Where everyone connected 🤝",
    title="EventBridgeKH",
    version="1.0.0",
    debug=True,
)
http_server = app.get_server()
origins = ["*"]
http_server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../API_FrontPage"))
templates = Jinja2Templates(directory=templates_dir)


@http_server.middleware("http")
async def redirect_to_index(request: Request, call_next):
    if not request.url.path.startswith("/v1/"):
        response = await call_next(request)
        if response.status_code == 404:
            return HTMLResponse(
                content=open(f"{templates_dir}/index.html", "r").read(), status_code=200
            )
        return response
    else:
        return await call_next(request)


@http_server.on_event("startup")
async def startup():
    await config.create_all()
