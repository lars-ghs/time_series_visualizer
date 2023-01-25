import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0)
df.index = pd.to_datetime(df.index)

# Clean data
df = df.loc[(df.value >= df.value.quantile(0.025))
            & (df.value <= df.value.quantile(0.975))]


def draw_line_plot():
  fig, ax = plt.subplots(figsize=(16, 6))
  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  ax.set_ylabel("Page Views")
  ax.set_xlabel("Date")
  plt.plot(df, color='r')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()
  months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]
  df_bar['Month'] = pd.Categorical(df_bar.index.strftime('%B'), # 	%B: Month as locale’s full name; months for sorting
                                   categories=months,
                                   ordered=True)  
  df_bar['Years'] = df_bar.index.year
  df_bar = pd.pivot_table(data=df_bar,
                          index=df_bar.Years,
                          columns='Month',
                          values='value')

  # Draw bar plot
  ax = df_bar.plot.bar(figsize=(12,6))
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_ylabel('Average Page Views')
  fig = ax.figure

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  fig, ax = plt.subplots(1, 2, figsize=(12, 6))

  sns.boxplot(data=df_box, x='year', y='value', ax=ax[0])
  ax[0].set_title('Year-wise Box Plot (Trend)')
  ax[0].set_ylabel('Page Views')
  ax[0].set_xlabel('Year')
  
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  df_box.month = pd.Categorical(df_box.month, 
                                categories=months,
                                ordered=True)
  
  sns.boxplot(data=df_box, x='month', y='value', ax=ax[1])
  ax[1].set_title('Month-wise Box Plot (Seasonality)')
  ax[1].set_ylabel('Page Views')
  ax[1].set_xlabel('Month')

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
