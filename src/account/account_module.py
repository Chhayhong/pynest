from nest.core import Module

from .admin_account_service import AdminAccountService

from .admin_account_controller import AdminAccountController
from .account_controller import AccountController
from .account_service import AccountService

@Module(
    controllers=[AccountController,AdminAccountController],
    providers=[AccountService,AdminAccountService],
    imports=[]
)   
class AccountModule:
    pass

    