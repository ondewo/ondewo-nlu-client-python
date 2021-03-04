from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.services.users import Users
from ondewo.nlu.user_pb2 import LoginRequest, LoginResponse


def login(config: ClientConfig, use_secure_channel: bool) -> str:
    """Log in using the user and password in the client config and return the auth token"""
    request: LoginRequest = LoginRequest(
        user_email=config.user_name,
        password=config.password,
    )
    user_service: Users = Users(config=config, nlu_token='', use_secure_channel=use_secure_channel)
    response: LoginResponse = user_service.login(request)
    nlu_token: str = response.auth_token
    user_service.grpc_channel.close()
    return nlu_token
