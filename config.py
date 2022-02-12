from dataclasses import dataclass

from environs import Env


@dataclass
class DBAccess:
    
    DRIVER: str
    NAME: str
    USERNAME: str
    PASSWORD: str
    ADDRESS: str
    PORT: str


@dataclass
class APIData:

    URL: str
    KEY: str


@dataclass
class Config:

    DB: DBAccess
    API: APIData


def load_config(path_to_env: str = ".env"):

    env = Env()
    env.read_env(path_to_env)

    return Config(
        DB=DBAccess(
            DRIVER=env.str("DB_DRIVER"),
            NAME=env.str("DB_NAME"),
            USERNAME=env.str("DB_USERNAME"),
            PASSWORD=env.str("DB_PASSWORD"),
            ADDRESS=env.str("DB_ADDRESS"),
            PORT=env.str("DB_PORT"),
            ),
        API=APIData(
            URL=env.str("API_URL"),
            KEY=env.str("API_KEY"),
            )
        )
