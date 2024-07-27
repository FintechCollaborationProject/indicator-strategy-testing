# Import classes from individual modules
from .backtest_metrics import BacktestMetrics
from .return_analysis import ReturnAnalysis
from .tgr import TGR
from .cagr import CAGR

# Define what should be available when importing the package
__all__ = ['BacktestMetrics', 'ReturnAnalysis', 'TGR', 'CAGR']