from fastapi.staticfiles import StaticFiles
from nest.core import PyNestFactory, Module
from .account.account_module import AccountModule
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.organization.organization_module import OrganizationModule
from src.event_management.event_management_module import EventManagementModule
from fastapi.middleware.cors import CORSMiddleware


@Module(
    imports=[AccountModule, OrganizationModule, EventManagementModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Where everyone connected - build with pynest python framework",
    title="EventBridgeKH",
    version="1.0.0",
    debug=True,
)

http_server = app.get_server()
origins = [
    "*"
    # "http://localhost",
    # "http://localhost:8080",
]
http_server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

http_server.mount("/static", StaticFiles(directory="static"), name="static")


@http_server.on_event("startup")
async def startup():
    await config.create_all()
