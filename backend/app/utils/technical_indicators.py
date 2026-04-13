import pandas as pd
import numpy as np
import talib
from typing import Union, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def ma(data: Union[pd.Series, List[float]], timeperiod: int = 30) -> pd.Series:
        """
        计算简单移动平均线 (MA)
        :param data: 价格序列（通常是收盘价）
        :param timeperiod: 计算周期，默认30
        :return: MA序列
        """
        if isinstance(data, list):
            data = pd.Series(data)
        return pd.Series(talib.SMA(data.values, timeperiod=timeperiod), index=data.index)
    
    @staticmethod
    def ema(data: Union[pd.Series, List[float]], timeperiod: int = 30) -> pd.Series:
        """
        计算指数移动平均线 (EMA)
        :param data: 价格序列
        :param timeperiod: 计算周期，默认30
        :return: EMA序列
        """
        if isinstance(data, list):
            data = pd.Series(data)
        return pd.Series(talib.EMA(data.values, timeperiod=timeperiod), index=data.index)
    
    @staticmethod
    def rsi(data: Union[pd.Series, List[float]], timeperiod: int = 14) -> pd.Series:
        """
        计算相对强弱指数 (RSI)
        :param data: 价格序列（通常是收盘价）
        :param timeperiod: 计算周期，默认14
        :return: RSI序列 (0-100)
        """
        if isinstance(data, list):
            data = pd.Series(data)
        return pd.Series(talib.RSI(data.values, timeperiod=timeperiod), index=data.index)
    
    @staticmethod
    def macd(data: Union[pd.Series, List[float]], 
             fastperiod: int = 12, 
             slowperiod: int = 26, 
             signalperiod: int = 9) -> Dict[str, pd.Series]:
        """
        计算移动平均收敛发散指标 (MACD)
        :param data: 价格序列（通常是收盘价）
        :param fastperiod: 快线周期，默认12
        :param slowperiod: 慢线周期，默认26
        :param signalperiod: 信号线周期，默认9
        :return: 包含MACD、信号线、直方图的字典
        """
        if isinstance(data, list):
            data = pd.Series(data)
        macd, signal, hist = talib.MACD(
            data.values, 
            fastperiod=fastperiod, 
            slowperiod=slowperiod, 
            signalperiod=signalperiod
        )
        return {
            'macd': pd.Series(macd, index=data.index),
            'signal': pd.Series(signal, index=data.index),
            'hist': pd.Series(hist, index=data.index)
        }
    
    @staticmethod
    def bollinger_bands(data: Union[pd.Series, List[float]], 
                        timeperiod: int = 20, 
                        nbdevup: float = 2, 
                        nbdevdn: float = 2) -> Dict[str, pd.Series]:
        """
        计算布林带 (Bollinger Bands)
        :param data: 价格序列（通常是收盘价）
        :param timeperiod: 计算周期，默认20
        :param nbdevup: 上带标准差倍数，默认2
        :param nbdevdn: 下带标准差倍数，默认2
        :return: 包含上轨、中轨、下轨的字典
        """
        if isinstance(data, list):
            data = pd.Series(data)
        upper, middle, lower = talib.BBANDS(
            data.values, 
            timeperiod=timeperiod, 
            nbdevup=nbdevup, 
            nbdevdn=nbdevdn
        )
        return {
            'upper': pd.Series(upper, index=data.index),
            'middle': pd.Series(middle, index=data.index),
            'lower': pd.Series(lower, index=data.index)
        }
    
    @staticmethod
    def kdj(high: Union[pd.Series, List[float]], 
            low: Union[pd.Series, List[float]], 
            close: Union[pd.Series, List[float]], 
            fastk_period: int = 9, 
            slowk_period: int = 3, 
            slowd_period: int = 3) -> Dict[str, pd.Series]:
        """
        计算KDJ指标
        :param high: 最高价序列
        :param low: 最低价序列
        :param close: 收盘价序列
        :param fastk_period: K值周期，默认9
        :param slowk_period: K值平滑周期，默认3
        :param slowd_period: D值平滑周期，默认3
        :return: 包含K、D、J值的字典
        """
        if isinstance(high, list):
            high = pd.Series(high)
        if isinstance(low, list):
            low = pd.Series(low)
        if isinstance(close, list):
            close = pd.Series(close)
            
        slowk, slowd = talib.STOCH(
            high.values, low.values, close.values,
            fastk_period=fastk_period,
            slowk_period=slowk_period,
            slowd_period=slowd_period
        )
        
        # J = 3*K - 2*D
        slowj = 3 * slowk - 2 * slowd
        
        return {
            'k': pd.Series(slowk, index=high.index),
            'd': pd.Series(slowd, index=high.index),
            'j': pd.Series(slowj, index=high.index)
        }
    
    @staticmethod
    def atr(high: Union[pd.Series, List[float]], 
            low: Union[pd.Series, List[float]], 
            close: Union[pd.Series, List[float]], 
            timeperiod: int = 14) -> pd.Series:
        """
        计算平均真实范围 (ATR)
        :param high: 最高价序列
        :param low: 最低价序列
        :param close: 收盘价序列
        :param timeperiod: 计算周期，默认14
        :return: ATR序列
        """
        if isinstance(high, list):
            high = pd.Series(high)
        if isinstance(low, list):
            low = pd.Series(low)
        if isinstance(close, list):
            close = pd.Series(close)
        return pd.Series(talib.ATR(high.values, low.values, close.values, timeperiod=timeperiod), index=high.index)
