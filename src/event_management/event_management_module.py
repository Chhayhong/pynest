from nest.core import Module

from ..event_management.event_management_public_controller import EventManagementPublicController
from .event_management_controller import EventManagementController
from .event_management_service import EventManagementService


@Module(
    controllers=[EventManagementController,EventManagementPublicController],
    providers=[EventManagementService],
    imports=[]
)   
class EventManagementModule:
    pass

    