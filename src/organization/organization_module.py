from nest.core import Module
from .organization_controller import OrganizationController
from .organization_service import OrganizationService


@Module(
    controllers=[OrganizationController],
    providers=[OrganizationService],
    imports=[]
)   
class OrganizationModule:
    pass

    