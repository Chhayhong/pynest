from nest.core import Module
from .users_controller import UsersController
from .users_service import UsersService

@Module(
    controllers=[UsersController],
    providers=[UsersService],
    imports=[]
)   
class UsersModule:
    pass

    