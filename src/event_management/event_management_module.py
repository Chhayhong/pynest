from nest.core import Module
from .event_management_controller import EventManagementController
from .event_management_service import EventManagementService


@Module(
    controllers=[EventManagementController],
    providers=[EventManagementService],
    imports=[]
)   
class EventManagementModule:
    pass

    