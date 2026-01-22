"""
Demand Forecasting Module
==========================
Uses time series analysis for inventory demand prediction.

Algorithms:
- Simple Moving Average
- Exponential Moving Average  
- Linear Regression
- Seasonal Decomposition
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ForecastResult:
    """Forecast result container."""
    product_id: str
    method: str
    predictions: List[float]
    dates: List[str]
    confidence_lower: List[float]
    confidence_upper: List[float]
    mae: float  # Mean Absolute Error
    rmse: float  # Root Mean Square Error
    trend: str  # 'increasing', 'decreasing', 'stable'
    seasonality: Optional[str]  # 'daily', 'weekly', 'monthly', None
    
    def to_dict(self) -> dict:
        return {
            'product_id': self.product_id,
            'method': self.method,
            'predictions': self.predictions,
            'dates': self.dates,
            'confidence_lower': self.confidence_lower,
            'confidence_upper': self.confidence_upper,
            'mae': round(self.mae, 2),
            'rmse': round(self.rmse, 2),
            'trend': self.trend,
            'seasonality': self.seasonality
        }


class DemandForecaster:
    """
    Demand forecasting using various time series methods.
    
    Uses NumPy for efficient numerical computations.
    """
    
    def __init__(self):
        """Initialize forecaster."""
        self.models = {}
    
    def simple_moving_average(self, data: List[float], window: int = 7) -> List[float]:
        """
        Calculate Simple Moving Average (SMA).
        
        Time Complexity: O(n)
        
        Args:
            data: Historical data points
            window: Window size for averaging
            
        Returns:
            SMA values
        """
        if len(data) < window:
            return data.copy()
        
        arr = np.array(data)
        weights = np.ones(window) / window
        sma = np.convolve(arr, weights, mode='valid')
        
        # Pad beginning with first available values
        padded = np.concatenate([arr[:window-1], sma])
        return padded.tolist()
    
    def exponential_moving_average(self, data: List[float], alpha: float = 0.3) -> List[float]:
        """
        Calculate Exponential Moving Average (EMA).
        
        More weight to recent values. Alpha = smoothing factor (0-1).
        Higher alpha = more weight to recent values.
        
        Time Complexity: O(n)
        """
        if not data:
            return []
        
        arr = np.array(data)
        ema = np.zeros(len(arr))
        ema[0] = arr[0]
        
        for i in range(1, len(arr)):
            ema[i] = alpha * arr[i] + (1 - alpha) * ema[i-1]
        
        return ema.tolist()
    
    def linear_regression_forecast(self, data: List[float], periods: int = 7) -> Tuple[List[float], float, float]:
        """
        Linear regression based forecast.
        
        Returns predictions and trend slope.
        
        Time Complexity: O(n)
        """
        if len(data) < 2:
            return [data[0]] * periods if data else [0] * periods, 0, 0
        
        arr = np.array(data)
        x = np.arange(len(arr))
        
        # Calculate linear regression using least squares
        n = len(arr)
        sum_x = np.sum(x)
        sum_y = np.sum(arr)
        sum_xy = np.sum(x * arr)
        sum_x2 = np.sum(x ** 2)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Predict future values
        future_x = np.arange(len(arr), len(arr) + periods)
        predictions = slope * future_x + intercept
        
        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((arr - y_pred) ** 2)
        ss_tot = np.sum((arr - np.mean(arr)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return predictions.tolist(), float(slope), float(r_squared)
    
    def detect_seasonality(self, data: List[float], max_period: int = 30) -> Optional[int]:
        """
        Detect seasonality period using autocorrelation.
        
        Time Complexity: O(n * max_period)
        """
        if len(data) < max_period * 2:
            return None
        
        arr = np.array(data)
        mean = np.mean(arr)
        variance = np.var(arr)
        
        if variance == 0:
            return None
        
        # Calculate autocorrelation for different lags
        autocorr = []
        for lag in range(1, max_period + 1):
            if lag >= len(arr):
                break
            corr = np.corrcoef(arr[:-lag], arr[lag:])[0, 1]
            autocorr.append((lag, corr if not np.isnan(corr) else 0))
        
        # Find significant peaks
        if not autocorr:
            return None
        
        max_corr_lag = max(autocorr, key=lambda x: x[1])
        if max_corr_lag[1] > 0.5:  # Significant correlation
            return max_corr_lag[0]
        
        return None
    
    def calculate_confidence_interval(self, data: List[float], predictions: List[float], 
                                       confidence: float = 0.95) -> Tuple[List[float], List[float]]:
        """
        Calculate confidence intervals for predictions.
        
        Uses standard deviation and z-score.
        """
        arr = np.array(data)
        std = np.std(arr)
        
        # Z-score for confidence level (95% = 1.96)
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        # Widen interval for further predictions
        lower = []
        upper = []
        for i, pred in enumerate(predictions):
            width = z * std * np.sqrt(1 + (i + 1) / len(data))
            lower.append(max(0, pred - width))
            upper.append(pred + width)
        
        return lower, upper
    
    def calculate_errors(self, actual: List[float], predicted: List[float]) -> Dict[str, float]:
        """Calculate forecast error metrics."""
        if len(actual) != len(predicted):
            min_len = min(len(actual), len(predicted))
            actual = actual[:min_len]
            predicted = predicted[:min_len]
        
        actual_arr = np.array(actual)
        pred_arr = np.array(predicted)
        
        # Mean Absolute Error
        mae = np.mean(np.abs(actual_arr - pred_arr))
        
        # Root Mean Square Error
        rmse = np.sqrt(np.mean((actual_arr - pred_arr) ** 2))
        
        # Mean Absolute Percentage Error (avoid division by zero)
        nonzero_mask = actual_arr != 0
        if np.any(nonzero_mask):
            mape = np.mean(np.abs((actual_arr[nonzero_mask] - pred_arr[nonzero_mask]) / actual_arr[nonzero_mask])) * 100
        else:
            mape = 0
        
        return {'mae': float(mae), 'rmse': float(rmse), 'mape': float(mape)}
    
    def determine_trend(self, data: List[float]) -> str:
        """Determine overall trend direction."""
        if len(data) < 2:
            return 'stable'
        
        arr = np.array(data)
        x = np.arange(len(arr))
        
        # Simple linear regression slope
        n = len(arr)
        slope = (n * np.sum(x * arr) - np.sum(x) * np.sum(arr)) / (n * np.sum(x ** 2) - np.sum(x) ** 2)
        
        # Normalize slope by mean to get relative change
        mean_val = np.mean(arr) if np.mean(arr) != 0 else 1
        relative_slope = slope / mean_val
        
        if relative_slope > 0.02:
            return 'increasing'
        elif relative_slope < -0.02:
            return 'decreasing'
        else:
            return 'stable'
    
    def forecast(self, product_id: str, historical_data: List[float], 
                 dates: List[str] = None, periods: int = 30,
                 method: str = 'auto') -> ForecastResult:
        """
        Generate demand forecast for a product.
        
        Args:
            product_id: Product identifier
            historical_data: Historical sales/demand data
            dates: Optional date labels
            periods: Number of periods to forecast
            method: 'sma', 'ema', 'linear', or 'auto'
            
        Returns:
            ForecastResult with predictions and metrics
        """
        if not historical_data:
            return ForecastResult(
                product_id=product_id,
                method='none',
                predictions=[0] * periods,
                dates=[],
                confidence_lower=[0] * periods,
                confidence_upper=[0] * periods,
                mae=0,
                rmse=0,
                trend='stable',
                seasonality=None
            )
        
        # Auto-select best method
        if method == 'auto':
            seasonality = self.detect_seasonality(historical_data)
            if len(historical_data) >= 30:
                method = 'ema'
            elif len(historical_data) >= 7:
                method = 'linear'
            else:
                method = 'sma'
        else:
            seasonality = self.detect_seasonality(historical_data)
        
        # Generate predictions based on method
        if method == 'sma':
            window = min(7, len(historical_data))
            sma = self.simple_moving_average(historical_data, window)
            last_sma = sma[-1] if sma else 0
            predictions = [last_sma] * periods
            
        elif method == 'ema':
            ema = self.exponential_moving_average(historical_data)
            last_ema = ema[-1] if ema else 0
            # Slight decay for future predictions
            predictions = [last_ema * (0.99 ** i) for i in range(periods)]
            
        elif method == 'linear':
            predictions, slope, r2 = self.linear_regression_forecast(historical_data, periods)
            
        else:
            predictions = [np.mean(historical_data)] * periods
        
        # Ensure non-negative predictions
        predictions = [max(0, p) for p in predictions]
        
        # Calculate confidence intervals
        lower, upper = self.calculate_confidence_interval(historical_data, predictions)
        
        # Calculate error metrics on historical data
        if method == 'ema':
            fitted = self.exponential_moving_average(historical_data)
        elif method == 'sma':
            fitted = self.simple_moving_average(historical_data)
        else:
            fitted_count = len(historical_data)
            x = np.arange(fitted_count)
            pred, slope, _ = self.linear_regression_forecast(historical_data[:fitted_count//2], fitted_count//2)
            fitted = historical_data[:fitted_count//2] + pred
        
        errors = self.calculate_errors(historical_data, fitted)
        
        # Generate future dates
        future_dates = []
        if dates and len(dates) > 0:
            try:
                last_date = datetime.fromisoformat(dates[-1])
                future_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                               for i in range(periods)]
            except:
                future_dates = [f"Day {i+1}" for i in range(periods)]
        else:
            future_dates = [f"Day {i+1}" for i in range(periods)]
        
        # Determine seasonality label
        seasonality_label = None
        if seasonality:
            if seasonality <= 7:
                seasonality_label = 'weekly'
            elif seasonality <= 14:
                seasonality_label = 'bi-weekly'
            else:
                seasonality_label = 'monthly'
        
        return ForecastResult(
            product_id=product_id,
            method=method,
            predictions=predictions,
            dates=future_dates,
            confidence_lower=lower,
            confidence_upper=upper,
            mae=errors['mae'],
            rmse=errors['rmse'],
            trend=self.determine_trend(historical_data),
            seasonality=seasonality_label
        )
