import tushare as ts
import pandas as pd
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class TuShareClient:
    def __init__(self):
        if not settings.TUSHARE_TOKEN:
            logger.warning("TuShare token not configured")
            self.pro_api = None
        else:
            ts.set_token(settings.TUSHARE_TOKEN)
            self.pro_api = ts.pro_api()
    
    def get_daily_data(self, ts_code: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
        """获取日线数据"""
        if not self.pro_api:
            logger.error("TuShare API not initialized")
            return None
        
        try:
            df = self.pro_api.daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            return df
        except Exception as e:
            logger.error(f"Error fetching daily data for {ts_code}: {e}")
            return None
    
    def get_stock_basic(self, exchange: str = '', list_status: str = 'L') -> Optional[pd.DataFrame]:
        """获取股票基本信息"""
        if not self.pro_api:
            logger.error("TuShare API not initialized")
            return None
            
        try:
            df = self.pro_api.stock_basic(
                exchange=exchange,
                list_status=list_status,
                fields='ts_code,symbol,name,area,industry,list_date'
            )
            return df
        except Exception as e:
            logger.error(f"Error fetching stock basic info: {e}")
            return None
