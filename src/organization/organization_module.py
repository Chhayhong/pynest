from nest.core import Module

from ..organization.organization_public_controller import OrganizationPublicController
from .organization_controller import OrganizationController
from .organization_service import OrganizationService


@Module(
    controllers=[OrganizationController,OrganizationPublicController],
    providers=[OrganizationService],
    imports=[]
)   
class OrganizationModule:
    pass

    