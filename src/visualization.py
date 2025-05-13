import matplotlib.pyplot as plt
import seaborn as sns

def create_visualization(df, chart_type, x_col, y_col=None, color_col=None):
    """Create visualization based on user selection"""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == "Bar Chart":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "Line Chart":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=color_col, ax=ax)
        elif chart_type == "Histogram":
            sns.histplot(data=df, x=x_col, ax=ax)
        elif chart_type == "Box Plot":
            sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "Violin Plot":
            sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        return None 