import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os

direct = './test_data'
new_df = pd.DataFrame([], columns=['date', 'BLUEs'])

file_dates= []
file_areas = []
file_days_since = []
allowed_genotypes = ['Romaine', 'Sunbelt', 'Angie', 'Batavia Rouge Grenobloise', 'Ruby', 'Colorado', 'Sucrine', 'Aido']
file_genes = []
first_date = pd.to_datetime('2022-01-27')
palette = sns.color_palette("Set1")

def get_data() :
    """
    This function retrieves the data, and generates the new_df dataframe in the format for plotting. 
    The expected format for the file names is 2022-01-01_0-0-0-0__some_other_name.csv
    """
    for file in os.listdir(direct) :
        full_path = os.path.join(direct, file)
        df = pd.read_csv(full_path)
        count_df = 0
        new_df = df[df['genotype'].isin(allowed_genotypes)] 
        new_df['date'] = new_df['date'].str.split('__', expand=True)[0]
        new_df['date'] = pd.to_datetime(new_df['date'])
        new_df['days_since'] = (new_df['date'] - first_date).dt.days
        file_dates.append(new_df['date'])
        file_days_since.append(new_df['days_since'])
        file_areas.append(new_df['BLUEs'])
        file_genes.append(new_df['genotype'])
        count_df +=1
    
    df_days_since = pd.concat(file_days_since)
    df_dates = pd.concat(file_dates)
    df_areas = pd.concat(file_areas)
    df_genotypes = pd.concat(file_genes)
    df = pd.concat([df_days_since, df_dates, df_areas, df_genotypes], axis=1)
    return df

def plot_all_together(df) :
    """
    This function plots all of the market types on the same graph. 
    """
    plt.figure()
    sns.lineplot(data=df,
        x='days_since',y='BLUEs', 
        hue="genotype",
        palette=palette,
    ).set(xlabel='Days Since Season Start',
        ylabel='BLUE',
        title='BLUEs in Season 13 Lettuce')
    plt.savefig('blues_by_time_together.png', dpi=900)

def plot_all_separate(df) :
    """ 
    This function plots all of the market types on separate graphs. 
    """
    plt.figure()
    sns.relplot(
        data=df, x="days_since", y="BLUEs", col="genotype", hue="genotype",
        col_wrap=4, palette=palette, kind='line',
        height=4, 
    )
    plt.savefig('blues_by_time_cols_separate.png', dpi=900)

def plot_histogram(df, inputDate):
    """
    This function plots a histogram of the BLUEs on the given date.
    """
    plt.figure()
    print(df)
    grouped_df = df[df['date'] == inputDate]
    print(grouped_df)
    #this_date = grouped_df['2022-01-28']
    sns.histplot(data=grouped_df, x='BLUEs', hue='genotype', palette=palette).set(title='Histogram of BLUEs values')
    plt.savefig('blues_histogram.png', dpi=900)


df = get_data()
plot_all_separate(df)
plot_all_together(df)
plot_histogram(df, '2022-01-28')
