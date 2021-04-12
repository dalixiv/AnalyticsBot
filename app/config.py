from pydantic import BaseSettings, Field, PostgresDsn


class Config(BaseSettings):

    tg_bot_token: str = Field(..., env='TG_BOT_TOKEN')

    pg_url: str = Field(..., env='DATABASE_URL')

    # constants
    P_TIMEZONE = "Europe/Kiev"  # для установки времени, чтобы по этой зоне обновлялось
    TIMEZONE_COMMON_NAME = "Kiev"  # Название Зоны


ctx = Config()


__all__ = ('ctx',)
