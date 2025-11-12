"""
Visualization utilities for data insights
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, Dict, Any
from src.logger import get_logger

logger = get_logger(__name__)


class VisualizationGenerator:
    """Generates visualizations from data"""
    
    @staticmethod
    def auto_visualize(df: pd.DataFrame, query: str = "") -> Optional[go.Figure]:
        """
        Automatically generate appropriate visualization based on data
        
        Args:
            df: DataFrame to visualize
            query: Original user query for context
            
        Returns:
            Plotly figure or None
        """
        if df is None or df.empty or len(df) > 1000:
            return None
        
        try:
            # Determine best visualization based on data shape and types
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
            # Bar chart for categorical + numeric
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                return VisualizationGenerator.create_bar_chart(
                    df, categorical_cols[0], numeric_cols[0]
                )
            
            # Line chart for time series
            if any('date' in col.lower() or 'time' in col.lower() for col in df.columns):
                date_col = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()][0]
                if len(numeric_cols) > 0:
                    return VisualizationGenerator.create_line_chart(
                        df, date_col, numeric_cols[0]
                    )
            
            # Pie chart for categorical distribution
            if len(df) <= 20 and len(categorical_cols) > 0 and len(numeric_cols) > 0:
                return VisualizationGenerator.create_pie_chart(
                    df, categorical_cols[0], numeric_cols[0]
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error auto-generating visualization: {e}")
            return None
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Create bar chart"""
        fig = px.bar(
            df.head(20),  # Limit to top 20
            x=x_col,
            y=y_col,
            title=title or f"{y_col} by {x_col}",
            template="plotly_white"
        )
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode='x unified'
        )
        return fig
    
    @staticmethod
    def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Create line chart"""
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title or f"{y_col} over {x_col}",
            template="plotly_white",
            markers=True
        )
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode='x unified'
        )
        return fig
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, labels_col: str, values_col: str, title: str = "") -> go.Figure:
        """Create pie chart"""
        fig = px.pie(
            df.head(10),  # Limit to top 10
            names=labels_col,
            values=values_col,
            title=title or f"Distribution of {values_col}",
            template="plotly_white"
        )
        return fig
    
    @staticmethod
    def create_metrics_dashboard(metrics: Dict[str, Any]) -> go.Figure:
        """Create a metrics dashboard"""
        fig = make_subplots(
            rows=1, cols=len(metrics),
            subplot_titles=list(metrics.keys()),
            specs=[[{'type': 'indicator'}] * len(metrics)]
        )
        
        for i, (title, value) in enumerate(metrics.items(), 1):
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=value,
                    title={'text': title},
                ),
                row=1, col=i
            )
        
        fig.update_layout(
            height=200,
            template="plotly_white"
        )
        return fig
    
    @staticmethod
    def create_heatmap(df: pd.DataFrame, x_col: str, y_col: str, value_col: str, title: str = "") -> go.Figure:
        """Create heatmap"""
        pivot_df = df.pivot_table(values=value_col, index=y_col, columns=x_col, aggfunc='sum')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title=title or f"{value_col} Heatmap",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white"
        )
        return fig
