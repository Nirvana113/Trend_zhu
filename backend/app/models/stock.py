from sqlalchemy import Column, Integer, String, Date, DateTime, Float, BigInteger
from sqlalchemy.sql import func
from app.db.base import Base

class StockDaily(Base):
    """股票日线数据模型"""
    __tablename__ = "stock_daily"

    id = Column(Integer, primary_key=True, index=True)
    ts_code = Column(String(20), index=True, nullable=False)  # 股票代码
    trade_date = Column(Date, nullable=False, index=True)  # 交易日期
    open = Column(Float)  # 开盘价
    high = Column(Float)  # 最高价
    low = Column(Float)   # 最低价
    close = Column(Float) # 收盘价
    pre_close = Column(Float)  # 前收盘价
    change = Column(Float)  # 涨跌额
    pct_chg = Column(Float)  # 涨跌幅 (%)
    vol = Column(Float)  # 成交量 (手)
    amount = Column(Float)  # 成交额 (千元)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 复合索引
    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
    )

class StockBasic(Base):
    """股票基本信息模型"""
    __tablename__ = "stock_basic"

    id = Column(Integer, primary_key=True, index=True)
    ts_code = Column(String(20), unique=True, index=True, nullable=False)  # 股票代码
    symbol = Column(String(20), index=True)  # 股票代码无后缀
    name = Column(String(100), index=True)  # 股票名称
    area = Column(String(50))  # 地域
    industry = Column(String(100))  # 行业
    list_date = Column(Date)  # 上市日期
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
