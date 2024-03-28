from pathlib import Path
from dataclasses import dataclass

from dotenv import dotenv_values


DIR_PROJECT = Path(__file__).parent
DIR_SESSIONS = Path('sessions')
FILEPATH_ENV = Path('.env')
FILEPATH_LOGGER = (DIR_PROJECT / DIR_PROJECT.name).with_suffix('.log')

for d in [DIR_SESSIONS]:
    DIR_SESSIONS.mkdir(exist_ok=True)


@dataclass
class Config:
    api_id: int | str
    api_hash: str
    phone: str
    password: str

    @property
    def session_filepath(self) -> str:
        return str((DIR_SESSIONS / self.phone).absolute())


env = dotenv_values(FILEPATH_ENV)
cfg = Config(**{k.lower(): v for k, v in env.items()})