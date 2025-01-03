from nest.core import PyNestFactory, Module
from fastapi.middleware.cors import CORSMiddleware
from .account.account_module import AccountModule
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.organization.organization_module import OrganizationModule
from src.event_management.event_management_module import EventManagementModule


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
if http_server is None:
    raise RuntimeError("Failed to get the server instance from PyNestFactory")

http_server.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.9"],  # Replace with the specific IP address
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_server.on_event("startup")
async def startup():
    await config.create_all()
