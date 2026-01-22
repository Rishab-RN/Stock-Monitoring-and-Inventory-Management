"""
Visualization Module
====================
Generate charts and visualizations using Matplotlib.

Creates production-ready charts for:
- Sales trends
- Inventory levels
- Demand forecasts
- Supplier network
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import io
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple


class InventoryVisualizer:
    """
    Chart generation for inventory analytics.
    
    Uses Matplotlib for high-quality visualizations.
    """
    
    # Modern color palette
    COLORS = {
        'primary': '#6366F1',
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'info': '#3B82F6',
        'purple': '#8B5CF6',
        'pink': '#EC4899',
        'gray': '#6B7280',
        'dark': '#1F2937',
        'light': '#F3F4F6'
    }
    
    GRADIENT_COLORS = [
        ['#667eea', '#764ba2'],  # Purple gradient
        ['#f093fb', '#f5576c'],  # Pink gradient
        ['#4facfe', '#00f2fe'],  # Blue gradient
        ['#43e97b', '#38f9d7'],  # Green gradient
        ['#fa709a', '#fee140'],  # Orange gradient
    ]
    
    def __init__(self, style: str = 'modern'):
        """
        Initialize visualizer with style preset.
        
        Args:
            style: 'modern', 'minimal', or 'classic'
        """
        self.style = style
        self._setup_style()
    
    def _setup_style(self):
        """Configure matplotlib style."""
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 11,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': '#E5E7EB',
            'grid.color': '#F3F4F6',
            'grid.linestyle': '-',
            'grid.linewidth': 0.5
        })
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{img_str}"
    
    def _save_fig(self, fig, filepath: str) -> str:
        """Save figure to file."""
        fig.savefig(filepath, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        return filepath
    
    def plot_sales_trend(self, dates: List[str], values: List[float],
                         title: str = "Sales Trend",
                         forecast: List[float] = None,
                         forecast_dates: List[str] = None,
                         output_path: str = None) -> str:
        """
        Create sales trend line chart with optional forecast.
        
        Returns base64 image string or saves to file.
        """
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Plot actual data
        x = list(range(len(values)))
        ax.fill_between(x, values, alpha=0.3, color=self.COLORS['primary'])
        ax.plot(x, values, color=self.COLORS['primary'], linewidth=2.5, 
                label='Actual Sales', marker='o', markersize=4)
        
        # Plot forecast if provided
        if forecast and forecast_dates:
            forecast_x = list(range(len(values), len(values) + len(forecast)))
            ax.fill_between(forecast_x, forecast, alpha=0.2, color=self.COLORS['success'])
            ax.plot(forecast_x, forecast, color=self.COLORS['success'], 
                   linewidth=2.5, linestyle='--', label='Forecast', 
                   marker='s', markersize=4)
            
            # Vertical line separating actual from forecast
            ax.axvline(x=len(values) - 0.5, color=self.COLORS['gray'], 
                      linestyle=':', alpha=0.7)
        
        # Styling
        ax.set_title(title, fontweight='bold', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Units')
        ax.legend(loc='upper left', framealpha=0.9)
        
        # Set x-axis labels
        all_dates = dates + (forecast_dates or [])
        tick_positions = list(range(0, len(all_dates), max(1, len(all_dates) // 10)))
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([all_dates[i][:10] if i < len(all_dates) else '' 
                           for i in tick_positions], rotation=45, ha='right')
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_inventory_levels(self, products: List[Dict[str, Any]],
                              title: str = "Inventory Levels",
                              output_path: str = None) -> str:
        """
        Create horizontal bar chart of inventory levels.
        """
        fig, ax = plt.subplots(figsize=(10, max(6, len(products) * 0.4)))
        
        # Sort by quantity
        products = sorted(products, key=lambda x: x.get('quantity', 0))
        
        names = [p.get('name', p.get('id', ''))[:20] for p in products]
        quantities = [p.get('quantity', 0) for p in products]
        thresholds = [p.get('threshold', 10) for p in products]
        
        # Color based on stock level
        colors = []
        for qty, thresh in zip(quantities, thresholds):
            if qty == 0:
                colors.append(self.COLORS['danger'])
            elif qty < thresh:
                colors.append(self.COLORS['warning'])
            else:
                colors.append(self.COLORS['success'])
        
        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, quantities, color=colors, alpha=0.8, height=0.6)
        
        # Add threshold markers
        for i, thresh in enumerate(thresholds):
            ax.plot([thresh, thresh], [i - 0.3, i + 0.3], 
                   color=self.COLORS['dark'], linewidth=2, linestyle='--')
        
        # Add value labels
        for bar, qty in zip(bars, quantities):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'{qty}', va='center', fontsize=9, color=self.COLORS['dark'])
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names)
        ax.set_xlabel('Quantity')
        ax.set_title(title, fontweight='bold', pad=20)
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.COLORS['success'], label='Well Stocked'),
            Patch(facecolor=self.COLORS['warning'], label='Low Stock'),
            Patch(facecolor=self.COLORS['danger'], label='Out of Stock'),
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_category_distribution(self, categories: Dict[str, int],
                                   title: str = "Products by Category",
                                   output_path: str = None) -> str:
        """
        Create pie/donut chart of category distribution.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(categories.keys())
        sizes = list(categories.values())
        
        # Color palette
        colors = [self.GRADIENT_COLORS[i % len(self.GRADIENT_COLORS)][0] 
                 for i in range(len(labels))]
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            colors=colors, pctdistance=0.75,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
        )
        
        # Style the text
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Add center text
        total = sum(sizes)
        ax.text(0, 0, f'{total}\nProducts', ha='center', va='center',
               fontsize=16, fontweight='bold', color=self.COLORS['dark'])
        
        ax.set_title(title, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_top_sellers(self, products: List[Dict[str, Any]],
                         title: str = "Top Selling Products",
                         output_path: str = None) -> str:
        """
        Create bar chart of top selling products.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        names = [p.get('name', '')[:15] for p in products[:10]]
        sales = [p.get('total_sold', p.get('sold', 0)) for p in products[:10]]
        revenues = [p.get('total_revenue', p.get('revenue', 0)) for p in products[:10]]
        
        x = np.arange(len(names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, sales, width, label='Units Sold',
                      color=self.COLORS['primary'], alpha=0.8)
        
        # Secondary y-axis for revenue
        ax2 = ax.twinx()
        bars2 = ax2.bar(x + width/2, revenues, width, label='Revenue (₹)',
                       color=self.COLORS['success'], alpha=0.8)
        
        ax.set_xlabel('Product')
        ax.set_ylabel('Units Sold', color=self.COLORS['primary'])
        ax2.set_ylabel('Revenue (₹)', color=self.COLORS['success'])
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        
        ax.set_title(title, fontweight='bold', pad=20)
        
        # Combined legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_forecast_comparison(self, actual: List[float], 
                                 forecasts: Dict[str, List[float]],
                                 dates: List[str],
                                 title: str = "Forecast Comparison",
                                 output_path: str = None) -> str:
        """
        Compare multiple forecasting methods.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = list(range(len(actual)))
        
        # Plot actual
        ax.plot(x, actual, color=self.COLORS['dark'], linewidth=2.5,
               label='Actual', marker='o', markersize=4)
        
        # Plot each forecast
        colors = [self.COLORS['primary'], self.COLORS['success'], 
                 self.COLORS['warning'], self.COLORS['purple']]
        
        for i, (method, values) in enumerate(forecasts.items()):
            ax.plot(x[:len(values)], values, color=colors[i % len(colors)],
                   linewidth=2, linestyle='--', label=method, alpha=0.8)
        
        ax.set_title(title, fontweight='bold', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.legend(loc='upper left')
        
        # X-axis labels
        tick_positions = list(range(0, len(dates), max(1, len(dates) // 10)))
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([dates[i][:10] for i in tick_positions], 
                          rotation=45, ha='right')
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_health_gauge(self, score: float, grade: str,
                          title: str = "Inventory Health Score",
                          output_path: str = None) -> str:
        """
        Create gauge chart for health score.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create gauge background
        theta = np.linspace(0, np.pi, 100)
        
        # Background arc
        for i, (start, end, color) in enumerate([
            (0, np.pi/3, self.COLORS['danger']),
            (np.pi/3, 2*np.pi/3, self.COLORS['warning']),
            (2*np.pi/3, np.pi, self.COLORS['success'])
        ]):
            theta_section = np.linspace(start, end, 30)
            ax.fill_between(np.cos(theta_section), 0, np.sin(theta_section),
                           color=color, alpha=0.3)
        
        # Score needle
        score_angle = np.pi * (1 - score / 100)
        ax.annotate('', xy=(np.cos(score_angle) * 0.8, np.sin(score_angle) * 0.8),
                   xytext=(0, 0),
                   arrowprops=dict(arrowstyle='->', color=self.COLORS['dark'],
                                  lw=3))
        
        # Center circle
        circle = plt.Circle((0, 0), 0.15, color='white', zorder=10)
        ax.add_patch(circle)
        
        # Score text
        ax.text(0, -0.3, f'{score:.0f}', ha='center', va='center',
               fontsize=36, fontweight='bold', color=self.COLORS['dark'])
        ax.text(0, -0.5, grade, ha='center', va='center',
               fontsize=24, fontweight='bold', color=self.COLORS['primary'])
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.6, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
    
    def plot_weekly_pattern(self, day_averages: Dict[str, float],
                            title: str = "Weekly Sales Pattern",
                            output_path: str = None) -> str:
        """
        Create radar chart for weekly patterns.
        """
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday', 'Sunday']
        values = [day_averages.get(day, 0) for day in days]
        
        # Normalize values
        max_val = max(values) if values else 1
        normalized = [v / max_val * 100 for v in values]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        # Create angles
        angles = np.linspace(0, 2 * np.pi, len(days), endpoint=False).tolist()
        normalized += normalized[:1]  # Complete the loop
        angles += angles[:1]
        
        # Plot
        ax.plot(angles, normalized, 'o-', linewidth=2, color=self.COLORS['primary'])
        ax.fill(angles, normalized, alpha=0.25, color=self.COLORS['primary'])
        
        # Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(days, size=10)
        ax.set_title(title, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_path:
            return self._save_fig(fig, output_path)
        return self._fig_to_base64(fig)
