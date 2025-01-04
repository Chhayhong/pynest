from nest.core import Module
from .event_organizer_controller import EventOrganizerController
from .event_organizer_service import EventOrganizerService


@Module(
    controllers=[EventOrganizerController],
    providers=[EventOrganizerService],
    imports=[]
)   
class EventOrganizerModule:
    pass

    