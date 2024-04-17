from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    project_name: str
    project_host: str
    project_port: int
    socket_host: str
    socket_port: int

    class Config:
        env_file = '.env'


app_settings = AppSettings()
