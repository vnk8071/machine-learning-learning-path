from pydantic_settings import BaseSettings


class CustomSettings(BaseSettings):
    PROJECT_NAME: str = "CODE BASE"
    AUTHOR: str = "KhoiVN"
    REDIS_URL: str = "redis://redis:6379/0"


settings = CustomSettings()


if __name__ == "__main__":
    print(settings.PROJECT_NAME)  # CODE BASE
    print(settings.AUTHOR)  # KhoiVN
