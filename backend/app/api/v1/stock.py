from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.stock import StockDaily
from app.utils.tushare_client import TuShareClient
from pydantic import BaseModel
from datetime import date
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for response
class StockDailyBase(BaseModel):
    ts_code: str
    trade_date: date
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    pre_close: Optional[float]
    change: Optional[float]
    pct_chg: Optional[float]
    vol: Optional[float]
    amount: Optional[float]

    class Config:
        orm_mode = True

class StockDailyResponse(BaseModel):
    data: List[StockDailyBase]
    total: int

@router.get("/daily/{ts_code}", response_model=StockDailyResponse)
async def get_stock_daily(
    ts_code: str,
    start_date: Optional[str] = Query(None, description="开始日期，格式YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式YYYYMMDD"),
    limit: int = Query(100, description="返回记录数限制"),
    db: Session = Depends(get_db)
):
    """
    获取股票日线数据
    - ts_code: 股票代码，如000001.SZ
    - start_date: 开始日期（可选）
    - end_date: 结束日期（可选）
    - limit: 返回记录数限制（默认100）
    """
    # 先尝试从数据库获取
    query = db.query(StockDaily).filter(StockDaily.ts_code == ts_code)
    
    if start_date:
        query = query.filter(StockDaily.trade_date >= start_date)
    if end_date:
        query = query.filter(StockDaily.trade_date <= end_date)
    
    # 按日期倒序排列，最新的在前
    query = query.order_by(StockDaily.trade_date.desc())
    
    # 应用限制
    stocks = query.limit(limit).all()
    
    # 如果数据库中没有数据，则从TuShare获取并保存
    if not stocks:
        try:
            tu_share_client = TuShareClient()
            df = tu_share_client.get_daily_data(ts_code, start_date, end_date)
            
            if df is not None and not df.empty:
                # 将DataFrame转换为模型实例并保存到数据库
                stock_records = []
                for _, row in df.iterrows():
                    stock_record = StockDaily(
                        ts_code=row['ts_code'],
                        trade_date=row['trade_date'],
                        open=row['open'],
                        high=row['high'],
                        low=row['low'],
                        close=row['close'],
                        pre_close=row['pre_close'],
                        change=row['change'],
                        pct_chg=row['pct_chg'],
                        vol=row['vol'],
                        amount=row['amount']
                    )
                    stock_records.append(stock_record)
                
                # 批量保存
                db.add_all(stock_records)
                db.commit()
                
                # 重新查询刚刚保存的数据
                stocks = db.query(StockDaily).filter(StockDaily.ts_code == ts_code)
                if start_date:
                    stocks = stocks.filter(StockDaily.trade_date >= start_date)
                if end_date:
                    stocks = stocks.filter(StockDaily.trade_date <= end_date)
                stocks = stocks.order_by(StockDaily.trade_date.desc()).limit(limit).all()
            else:
                logger.warning(f"No data returned from TuShare for {ts_code}")
                
        except Exception as e:
            logger.error(f"Error fetching data from TuShare for {ts_code}: {e}")
            # 如果TuShare失败，尝试返回数据库中可能已有的数据
            if not stocks:
                raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
    
    if not stocks:
        raise HTTPException(status_code=404, detail=f"No data found for stock {ts_code}")
    
    return {
        "data": stocks,
        "total": len(stocks)
    }

# 导出路由器
__all__ = ["router"]
