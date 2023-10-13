import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os

direct = './initialPlots/data/detect_out'
new_df = pd.DataFrame([], columns=['date', 'BLUEs'])

file_dates= []
file_areas = []
allowed_genotypes = ['Blondine', 'Odra', 'Angie', 'Batavia Rouge Grenobloise', 'Ruby', 'Colorado', 'Sucrine', 'Aido']
file_genes = []
first_date = pd.to_datetime('2022-01-27')
palette = sns.color_palette("Set2")

def get_data() :
    for file in os.listdir(direct) :
        full_path = os.path.join(direct, file)
        df = pd.read_csv(full_path)
        count_df = 0
        new_df = df[df['genotype'].isin(allowed_genotypes)] 
        new_df['date'] = new_df['date'].str.split('__', expand=True)[0]
        new_df['date'] = pd.to_datetime(new_df['date'])
        new_df['date'] = (new_df['date'] - first_date).dt.days
        file_dates.append(new_df['date'])
        file_areas.append(new_df['BLUEs'])
        file_genes.append(new_df['genotype'])
        #print("date thing " + df['date'])
        count_df +=1
    #print(file_areas)
    df_date = pd.concat(file_dates)
    print(df_date)
    df_areas = pd.concat(file_areas)
    df_genotypes = pd.concat(file_genes)
    df = pd.concat([df_date, df_areas, df_genotypes], axis=1)
    return df

def plot_ruby_batavia() :
    for file in os.listdir(direct) :
        full_path = os.path.join(direct, file)
        df = pd.read_csv(full_path)
        count_df = 0
        new_df = df[df['genotype'].isin(["Ruby", "Batavia Rouge Grenobloise"])] 
        new_df['date'] = new_df['date'].str.split('__', expand=True)[0]
        new_df['date'] = pd.to_datetime(new_df['date'])
        new_df['date'] = (new_df['date'] - first_date).dt.days
        file_dates.append(new_df['date'])
        file_areas.append(new_df['bounding_area_m2'])
        file_genes.append(new_df['genotype'])
        #print("date thing " + df['date'])
        count_df +=1
    #print(file_areas)
    df_date = pd.concat(file_dates)
    df_areas = pd.concat(file_areas)
    df_genotypes = pd.concat(file_genes)
    rb_df = pd.concat([df_date, df_areas, df_genotypes], axis=1)
    new_palette = {
        "Batavia Rouge Grenobloise": "#ffd92f",
        "Ruby": "#e78ac3"
    }
    sns.lineplot(data=rb_df,
        x='date',y='bounding_area_m2', 
        hue="genotype",
        palette=new_palette,
    ).set(xlabel='Days Since Season Start',
        ylabel='Bounding Area',
        title='Bounding Area in Season 13 Lettuce')
    plt.savefig('bounding_area_by_time_new.png', dpi=900)

def plot_all_together(df) :
    #df = pd.read_csv('./initialPlots/detect_out/2022-01-27__10-54-27-164_lettuce_detection.csv')
    #print(df.columns)
    #sns.displot(x='date', y='bounding-area', hue='genotype', data=df)
    #df['date'] = df['date'].dt.strftime('%m-%d')
    sns.lineplot(data=df,
        x='date',y='bounding_area_m2', 
        hue="genotype",
        palette=palette,
    ).set(xlabel='Days Since Season Start',
        ylabel='Bounding Area',
        title='Bounding Area in Season 13 Lettuce')
    plt.savefig('bounding_area_by_time_new.png', dpi=900)

def plot_all_separate(df) :
    sns.relplot(
        data=df, x="date", y="bounding_area_m2", col="genotype", hue="genotype",
        col_wrap=4, palette=palette, kind='line',
        height=4, 
    )
    plt.savefig('bounding_area_by_time_cols.png', dpi=900)

#df = get_data()
plot_ruby_batavia()

