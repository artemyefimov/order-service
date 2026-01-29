from collections.abc import Callable
from typing import Never

from pydantic import Field
from pydantic_settings import BaseSettings


def missing(value: str) -> Callable[[], Never]:
    def inner() -> Never:
        raise ValueError(f"Missing setting '{value}'")

    return inner


class Settings(BaseSettings):
    postgres_connection_string: str = Field(
        default_factory=missing("POSTGRES_CONNECTION_STRING")
    )
    capashino_base_url: str = Field(default_factory=missing("CAPASHINO_BASE_URL"))
    capashino_api_key: str = Field(default_factory=missing("CAPASHINO_API_KEY"))
