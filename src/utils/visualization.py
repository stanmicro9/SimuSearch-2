"""
Optional visualization utilities for investigation results
"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import seaborn as sns

class ResultsVisualizer:
    """Visualize scientific investigation results"""
    
    def __init__(self, style: str = "scientific"):
        plt.style.use("seaborn-v0_8" if style == "scientific" else "default")
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    def plot_experimental_data(self, raw_data: Dict[str, List[float]], 
                             title: str = "Experimental Results") -> str:
        """Create visualization of experimental data"""
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Find independent and dependent variables
        data_keys = list(raw_data.keys())
        if len(data_keys) >= 2:
            x_data = raw_data[data_keys[0]]
            y_data = raw_data[data_keys[1]]
            
            # Scatter plot with trend line
            axes[0].scatter(x_data, y_data, alpha=0.7, s=50)
            
            # Add trend line
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            axes[0].plot(x_data, p(x_data), "r--", alpha=0.8)
            
            axes[0].set_xlabel(data_keys[0].replace('_', ' ').title())
            axes[0].set_ylabel(data_keys[1].replace('_', ' ').title())
            axes[0].set_title("Relationship Analysis")
            axes[0].grid(True, alpha=0.3)
            
            # Residuals plot
            residuals = np.array(y_data) - p(x_data)
            axes[1].scatter(x_data, residuals, alpha=0.7)
            axes[1].axhline(y=0, color='r', linestyle='--')
            axes[1].set_xlabel(data_keys[0].replace('_', ' ').title())
            axes[1].set_ylabel("Residuals")
            axes[1].set_title("Residual Analysis")
            axes[1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Save plot
        filename = f"results_{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_interactive_plot(self, raw_data: Dict[str, List[float]]) -> str:
        """Create interactive Plotly visualization"""
        
        data_keys = list(raw_data.keys())
        if len(data_keys) >= 2:
            x_data = raw_data[data_keys[0]]
            y_data = raw_data[data_keys[1]]
            
            fig = go.Figure()
            
            # Add scatter plot
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='markers+lines',
                name='Experimental Data',
                marker=dict(size=8, opacity=0.7),
                line=dict(width=2)
            ))
            
            fig.update_layout(
                title="Interactive Experimental Results",
                xaxis_title=data_keys[0].replace('_', ' ').title(),
                yaxis_title=data_keys[1].replace('_', ' ').title(),
                hovermode='closest',
                template='plotly_white'
            )
            
            filename = "interactive_results.html"
            fig.write_html(filename)
            return filename
        
        return ""