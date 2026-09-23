"""应用配置（使用 pydantic-settings 读取环境变量，便于后续部署扩展）。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "家庭财务管理系统"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./finance.db"
    # 登录令牌签名密钥，部署时务必改成随机值
    SECRET_KEY: str = "dev-secret-change-me"
    # 前端开发服务器地址，用于 CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()
