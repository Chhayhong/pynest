from nest.core import Controller
from .app_service import AppService


@Controller("/")
class AppController:

    def __init__(self, service: AppService):
        self.service = service

