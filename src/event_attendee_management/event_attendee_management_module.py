from nest.core import Module

from ..event_attendee_management.event_owner_manage_controller import EventOwnerManageController
from .event_attendee_management_controller import EventAttendeeManagementController
from .event_attendee_management_service import EventAttendeeManagementService


@Module(
    controllers=[EventAttendeeManagementController,EventOwnerManageController],
    providers=[EventAttendeeManagementService],
    imports=[]
)   
class EventAttendeeManagementModule:
    pass

    