"""
Trend Analysis Module
=====================
Analyzes inventory trends, patterns, and provides insights.

Uses Pandas for efficient data manipulation and NumPy for calculations.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class TrendReport:
    """Trend analysis report."""
    product_id: str
    period: str
    trend_direction: str
    trend_strength: float
    average_daily_sales: float
    peak_day: str
    low_day: str
    volatility: float
    growth_rate: float
    insights: List[str]
    
    def to_dict(self) -> dict:
        return {
            'product_id': self.product_id,
            'period': self.period,
            'trend_direction': self.trend_direction,
            'trend_strength': round(self.trend_strength, 3),
            'average_daily_sales': round(self.average_daily_sales, 2),
            'peak_day': self.peak_day,
            'low_day': self.low_day,
            'volatility': round(self.volatility, 3),
            'growth_rate': round(self.growth_rate, 2),
            'insights': self.insights
        }


class TrendAnalyzer:
    """
    Trend analysis for inventory data.
    
    Provides insights on:
    - Sales velocity
    - Seasonal patterns
    - Growth trends
    - Volatility analysis
    """
    
    def __init__(self):
        """Initialize trend analyzer."""
        self.day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                         'Friday', 'Saturday', 'Sunday']
    
    def calculate_moving_statistics(self, data: List[float], window: int = 7) -> Dict[str, List[float]]:
        """
        Calculate rolling statistics.
        
        Returns moving average, std, min, max.
        """
        arr = np.array(data)
        n = len(arr)
        
        if n < window:
            return {
                'moving_avg': data.copy(),
                'moving_std': [0] * n,
                'moving_min': data.copy(),
                'moving_max': data.copy()
            }
        
        result = {
            'moving_avg': [],
            'moving_std': [],
            'moving_min': [],
            'moving_max': []
        }
        
        for i in range(n):
            start = max(0, i - window + 1)
            window_data = arr[start:i+1]
            result['moving_avg'].append(float(np.mean(window_data)))
            result['moving_std'].append(float(np.std(window_data)))
            result['moving_min'].append(float(np.min(window_data)))
            result['moving_max'].append(float(np.max(window_data)))
        
        return result
    
    def calculate_growth_rate(self, data: List[float], period: int = 7) -> float:
        """
        Calculate period-over-period growth rate.
        
        Returns percentage change.
        """
        if len(data) < period * 2:
            return 0.0
        
        current_period = np.mean(data[-period:])
        previous_period = np.mean(data[-period*2:-period])
        
        if previous_period == 0:
            return 0.0
        
        return ((current_period - previous_period) / previous_period) * 100
    
    def calculate_volatility(self, data: List[float]) -> float:
        """
        Calculate coefficient of variation as volatility measure.
        
        Higher value = more volatile.
        """
        if len(data) < 2:
            return 0.0
        
        arr = np.array(data)
        mean = np.mean(arr)
        std = np.std(arr)
        
        if mean == 0:
            return 0.0
        
        return std / mean
    
    def find_peak_periods(self, data: List[float], dates: List[str] = None) -> Tuple[int, int]:
        """
        Find indices of peak and low periods.
        
        Returns (peak_index, low_index).
        """
        if not data:
            return (0, 0)
        
        arr = np.array(data)
        peak_idx = int(np.argmax(arr))
        low_idx = int(np.argmin(arr))
        
        return (peak_idx, low_idx)
    
    def analyze_weekly_pattern(self, data: List[float], dates: List[str]) -> Dict[str, float]:
        """
        Analyze day-of-week patterns.
        
        Returns average sales per day of week.
        """
        day_totals = defaultdict(list)
        
        for i, (value, date_str) in enumerate(zip(data, dates)):
            try:
                date = datetime.fromisoformat(date_str)
                day_name = self.day_names[date.weekday()]
                day_totals[day_name].append(value)
            except:
                continue
        
        return {day: np.mean(values) if values else 0 
                for day, values in day_totals.items()}
    
    def analyze_monthly_pattern(self, data: List[float], dates: List[str]) -> Dict[str, float]:
        """
        Analyze monthly patterns.
        
        Returns average sales per month.
        """
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_totals = defaultdict(list)
        
        for value, date_str in zip(data, dates):
            try:
                date = datetime.fromisoformat(date_str)
                month_name = month_names[date.month - 1]
                month_totals[month_name].append(value)
            except:
                continue
        
        return {month: np.mean(values) if values else 0 
                for month, values in month_totals.items()}
    
    def calculate_trend_strength(self, data: List[float]) -> float:
        """
        Calculate R-squared value as trend strength.
        
        Values closer to 1 indicate stronger trend.
        """
        if len(data) < 2:
            return 0.0
        
        arr = np.array(data)
        x = np.arange(len(arr))
        
        # Linear regression
        n = len(arr)
        sum_x = np.sum(x)
        sum_y = np.sum(arr)
        sum_xy = np.sum(x * arr)
        sum_x2 = np.sum(x ** 2)
        
        denom = n * sum_x2 - sum_x ** 2
        if denom == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n
        
        # R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((arr - y_pred) ** 2)
        ss_tot = np.sum((arr - np.mean(arr)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        r_squared = 1 - (ss_res / ss_tot)
        return max(0, r_squared)
    
    def generate_insights(self, data: List[float], dates: List[str] = None, 
                         product_name: str = "Product") -> List[str]:
        """
        Generate human-readable insights from trend analysis.
        """
        insights = []
        
        if len(data) < 2:
            return ["Insufficient data for trend analysis"]
        
        arr = np.array(data)
        
        # Overall statistics
        mean_val = np.mean(arr)
        std_val = np.std(arr)
        
        # Trend direction
        x = np.arange(len(arr))
        slope = (len(arr) * np.sum(x * arr) - np.sum(x) * np.sum(arr)) / \
                (len(arr) * np.sum(x ** 2) - np.sum(x) ** 2)
        
        if slope > 0.1 * mean_val:
            insights.append(f"📈 Strong upward trend detected - sales increasing")
        elif slope < -0.1 * mean_val:
            insights.append(f"📉 Downward trend detected - sales declining")
        else:
            insights.append(f"➡️ Sales are relatively stable")
        
        # Volatility
        cv = std_val / mean_val if mean_val > 0 else 0
        if cv > 0.5:
            insights.append(f"⚠️ High sales volatility ({cv:.0%}) - consider safety stock")
        elif cv < 0.2:
            insights.append(f"✅ Low volatility ({cv:.0%}) - predictable demand")
        
        # Recent performance
        if len(arr) >= 14:
            recent = np.mean(arr[-7:])
            previous = np.mean(arr[-14:-7])
            change = ((recent - previous) / previous * 100) if previous > 0 else 0
            
            if change > 10:
                insights.append(f"🚀 Last week sales up {change:.1f}% from previous week")
            elif change < -10:
                insights.append(f"📊 Last week sales down {abs(change):.1f}% from previous week")
        
        # Peak detection
        if len(arr) >= 7:
            peak_idx, low_idx = self.find_peak_periods(data)
            if dates and len(dates) > peak_idx:
                try:
                    peak_date = datetime.fromisoformat(dates[peak_idx])
                    insights.append(f"📌 Peak sales on {peak_date.strftime('%b %d')}: {arr[peak_idx]:.0f} units")
                except:
                    pass
        
        return insights
    
    def analyze(self, product_id: str, sales_data: List[float], 
                dates: List[str] = None, period: str = "30d") -> TrendReport:
        """
        Perform comprehensive trend analysis.
        
        Args:
            product_id: Product identifier
            sales_data: Daily sales data
            dates: Optional date labels
            period: Analysis period label
            
        Returns:
            TrendReport with analysis results
        """
        if not sales_data:
            return TrendReport(
                product_id=product_id,
                period=period,
                trend_direction='unknown',
                trend_strength=0,
                average_daily_sales=0,
                peak_day='N/A',
                low_day='N/A',
                volatility=0,
                growth_rate=0,
                insights=["No data available"]
            )
        
        arr = np.array(sales_data)
        
        # Calculate trend direction
        x = np.arange(len(arr))
        n = len(arr)
        mean_val = np.mean(arr)
        
        if n > 1:
            slope = (n * np.sum(x * arr) - np.sum(x) * np.sum(arr)) / \
                    (n * np.sum(x ** 2) - np.sum(x) ** 2)
            relative_slope = slope / mean_val if mean_val > 0 else 0
            
            if relative_slope > 0.02:
                trend_direction = 'increasing'
            elif relative_slope < -0.02:
                trend_direction = 'decreasing'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'stable'
        
        # Find peak and low days
        peak_idx, low_idx = self.find_peak_periods(sales_data)
        
        if dates and len(dates) > max(peak_idx, low_idx):
            peak_day = dates[peak_idx]
            low_day = dates[low_idx]
        else:
            peak_day = f"Day {peak_idx + 1}"
            low_day = f"Day {low_idx + 1}"
        
        return TrendReport(
            product_id=product_id,
            period=period,
            trend_direction=trend_direction,
            trend_strength=self.calculate_trend_strength(sales_data),
            average_daily_sales=float(mean_val),
            peak_day=peak_day,
            low_day=low_day,
            volatility=self.calculate_volatility(sales_data),
            growth_rate=self.calculate_growth_rate(sales_data),
            insights=self.generate_insights(sales_data, dates)
        )


class InventoryAnalytics:
    """
    Comprehensive inventory analytics combining multiple analyzers.
    """
    
    def __init__(self):
        """Initialize analytics engine."""
        from .forecasting import DemandForecaster
        self.forecaster = DemandForecaster()
        self.trend_analyzer = TrendAnalyzer()
    
    def analyze_product(self, product_id: str, sales_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Complete product analysis.
        
        Args:
            product_id: Product identifier
            sales_history: List of {date, quantity} records
            
        Returns:
            Comprehensive analysis report
        """
        # Extract data
        dates = [r.get('date', '') for r in sales_history]
        quantities = [r.get('quantity', 0) for r in sales_history]
        
        # Trend analysis
        trend = self.trend_analyzer.analyze(product_id, quantities, dates)
        
        # Forecasting
        forecast = self.forecaster.forecast(product_id, quantities, dates)
        
        # Reorder recommendation
        avg_daily = trend.average_daily_sales
        if forecast.trend == 'increasing':
            reorder_suggestion = int(avg_daily * 45)  # 45 days buffer
        elif forecast.trend == 'decreasing':
            reorder_suggestion = int(avg_daily * 20)  # 20 days buffer
        else:
            reorder_suggestion = int(avg_daily * 30)  # 30 days buffer
        
        return {
            'product_id': product_id,
            'trend': trend.to_dict(),
            'forecast': forecast.to_dict(),
            'recommendations': {
                'reorder_quantity': reorder_suggestion,
                'reorder_point': int(avg_daily * 7),  # 7-day buffer
                'safety_stock': int(avg_daily * 3 * (1 + trend.volatility))
            }
        }
    
    def get_inventory_health_score(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall inventory health score.
        
        Args:
            products: List of product data with quantities, thresholds, sales
            
        Returns:
            Health score and breakdown
        """
        if not products:
            return {'score': 0, 'grade': 'N/A', 'breakdown': {}}
        
        scores = {
            'stock_level': 0,
            'turnover': 0,
            'diversity': 0,
            'alerts': 0
        }
        
        total_products = len(products)
        low_stock_count = 0
        out_of_stock_count = 0
        total_turnover = 0
        categories = set()
        
        for p in products:
            qty = p.get('quantity', 0)
            threshold = p.get('threshold', 10)
            sold = p.get('total_sold', 0)
            category = p.get('category', 'Other')
            
            if qty == 0:
                out_of_stock_count += 1
            elif qty < threshold:
                low_stock_count += 1
            
            if qty > 0:
                total_turnover += sold / qty
            
            categories.add(category)
        
        # Calculate component scores (0-25 each)
        # Stock level score
        well_stocked = total_products - low_stock_count - out_of_stock_count
        scores['stock_level'] = (well_stocked / total_products) * 25 if total_products > 0 else 0
        
        # Turnover score (higher is better, capped)
        avg_turnover = total_turnover / total_products if total_products > 0 else 0
        scores['turnover'] = min(25, avg_turnover * 5)
        
        # Diversity score
        scores['diversity'] = min(25, len(categories) * 2.5)
        
        # Alert score (fewer alerts = better)
        alert_ratio = 1 - ((low_stock_count + out_of_stock_count * 2) / (total_products * 2))
        scores['alerts'] = max(0, alert_ratio * 25)
        
        total_score = sum(scores.values())
        
        # Grade
        if total_score >= 90:
            grade = 'A+'
        elif total_score >= 80:
            grade = 'A'
        elif total_score >= 70:
            grade = 'B'
        elif total_score >= 60:
            grade = 'C'
        elif total_score >= 50:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'score': round(total_score, 1),
            'grade': grade,
            'breakdown': {k: round(v, 1) for k, v in scores.items()},
            'summary': {
                'total_products': total_products,
                'low_stock': low_stock_count,
                'out_of_stock': out_of_stock_count,
                'categories': len(categories)
            }
        }
