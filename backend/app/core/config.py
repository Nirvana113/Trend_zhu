from pydantic import BaseSettings, PostgresDsn, RedisDsn
from typing import List, Union
import secrets

class Settings(BaseSettings):
    # 项目信息
    PROJECT_NAME: str = "Trend_zhu"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A股和加密货币选股系统"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # 安全
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8天
    
    # 数据库
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "trend_zhu"
    POSTGRES_PORT: str = "5432"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB or ''}",
        )
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Union[str, None] = None
    
    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=str(self.REDIS_PORT),
            password=self.REDIS_PASSWORD,
        )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # TuShare API
    TUSHARE_TOKEN: str = ""
    
    # Binance API
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
