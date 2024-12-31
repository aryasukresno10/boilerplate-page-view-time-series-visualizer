import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    global df
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df['value'], color='red', linewidth=1)

    #  Set the y-axis
    ax.set_ylim(df['value'].min())

    # date formatiing for x-axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Page Views", fontsize=12)

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # Draw bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    df_bar = df_bar.groupby(['year','month'])['value'].mean()
    
    df_bar = df_bar.unstack()
    df_bar.columns = ['January','February','March','April','May','June','July','August','September','October','November','December']
    
    # Draw bar plot
    fig = df_bar.plot(kind = 'bar', figsize = (15,10)).figure
  
    plt.xlabel('Years', fontsize = 15)
    plt.ylabel('Average Page Views', fontsize = 15)
    plt.legend(loc = 'upper left', title = 'Months', fontsize = 13)
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
     # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    # df_box['year'] = [d.year for d in df_box.date]
    # df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Draw box plots (using Seaborn)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise Box Plot
    sns.boxplot(
        ax=axes[0],
        data=df_box,
        x="year",
        y="value",
        palette="Set2"
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot
    sns.boxplot(
        ax=axes[1],
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        palette="Set3"
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
