from sqlalchemy import Column, Integer, String, Date, DateTime, Float, BigInteger
from sqlalchemy.sql import func
from app.db.base import Base

class CryptoDaily(Base):
    """加密货币日线数据模型"""
    __tablename__ = "crypto_daily"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)  # 交易对符号，如BTCUSDT
    open_time = Column(DateTime(timezone=True), nullable=False, index=True)  # 开盘时间
    open = Column(Float)  # 开盘价
    high = Column(Float)  # 最高价
    low = Column(Float)   # 最低价
    close = Column(Float) # 收盘价
    volume = Column(Float)  # 成交量
    close_time = Column(DateTime(timezone=True))  # 收盘时间
    quote_asset_volume = Column(Float)  # 计价资产成交量
    number_of_trades = Column(Integer)  # 交易笔数
    taker_buy_base_asset_volume = Column(Float)  # 主动买入成交量
    taker_buy_quote_asset_volume = Column(Float)  # 主动买入计价资产成交量
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 复合索引
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
    )
