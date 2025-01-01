from nest.core import Module
from .account_controller import AccountController
from .account_service import AccountService

@Module(
    controllers=[AccountController],
    providers=[AccountService],
    imports=[]
)   
class AccountModule:
    pass

    