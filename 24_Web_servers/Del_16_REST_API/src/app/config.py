from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Super API"
    app_description: str = "Helpers API"
    app_version: str = "1.0.0"
    api_version: str = "/v1"
    db_uri: str = "postgresql://hello_fastapi:hello_fastapi@db/hello_fastapi_dev"

    class Config:
        case_sensitive = True


settings = Settings()
