import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import requests
import io
import streamlit as st

st.set_page_config(layout="wide")
st.title("Automobile Sales Analysis Dashboard")

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"

response = requests.get(URL)
response.raise_for_status()
csv_content = io.StringIO(response.text)
df = pd.read_csv(csv_content)

st.header("📘 Tasks Description")

st.markdown("""
TASK 1.1:
Develop a **Line chart** using pandas to show how Average automobile sales fluctuate from year to year.

TASK 1.1.1:
Modify the chart to show recession annotations.

TASK 1.2:
How do trends in advertising expenditure correlate with automobile sales during non-recession periods, and what insights can be derived from this relationship.

TASK 1.3:
Visualization to compare the sales trend per vehicle type for a recession period with a non-recession period.

TASK 1.3.1:
Vehicle wise sales comparison.

TASK 1.4:
GDP trend comparison during recession and non-recession.

TASK 1.5:
A Bubble plot for displaying the impact of seasonality on Automobile Sales.

TASK 1.6:
A scatter plot to identify the relationship between consumer confidence and automobile sales during recessions.

TASK 1.6.1:
Relationship between Vehicle Price and Sales during Recessions.

TASK 1.7:
Advertising expenditure of XYZAutomotives during recession and non-recession periods.

TASK 1.8:
A pie chart to display the total Advertisement expenditure for each vehicle type during recession period.

TASK 1.9:
The effect of the unemployment rate on vehicle type and sales during the Recession Period.
""")

plot_option = st.sidebar.radio(
    "Select Task",
    [
        "Task 1.1",
        "Task 1.1.1",
        "Task 1.2",
        "Task 1.3.1",
        "Task 1.3.2",
        "Task 1.4",
        "Task 1.5",
        "Task 1.6",
        "Task 1.6.1",
        "Task 1.7",
        "Task 1.8",
        "Task 1.9"
    ]
)

st.divider()

# Task 1.1
if plot_option == "Task 1.1":
    fig, ax = plt.subplots()
    Year = list(map(str, range(1980, 2024)))
    df_t1 = df.groupby('Year')['Automobile_Sales'].mean()
    df_t1.plot(kind='line', ax=ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average automobile sales')
    ax.set_title('Automobile Sales over time')
    st.pyplot(fig)

# Task 1.1.1
elif plot_option == "Task 1.1.1":
    fig, ax = plt.subplots(figsize=(10, 6))
    df_t1 = df.groupby('Year')['Automobile_Sales'].mean()
    ax.plot(df_t1.index, df_t1.values)
    ax.set_xticks(list(range(1980, 2024)))
    ax.tick_params(axis='x', rotation=75)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average automobile sales')
    ax.set_title('Automobile Sales during Recession')
    ax.text(1982, 650, '1981-82 Recession')
    ax.text(1991, 700, '1991 Recession')
    st.pyplot(fig)

# Task 1.2
elif plot_option == "Task 1.2":
    fig, ax = plt.subplots(figsize=(12, 6))
    df_t2 = df.loc[df['Recession'] == 0]
    df_t2n = df_t2.groupby('Year')[['Automobile_Sales', 'Advertising_Expenditure']].mean().reset_index()

    ax.plot(df_t2n['Year'], df_t2n['Automobile_Sales'], marker='o', linestyle='-', color='green', label='Average Sales')
    ax.plot(df_t2n['Year'], df_t2n['Advertising_Expenditure'], marker='s', linestyle='--', color='blue', label='Advertising Expenditure')

    ax.set_xlabel('Year')
    ax.set_ylabel('Amount')
    ax.set_title('Average Sales and Advertising Expenditure Over the Years (Non-Recession)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Task 1.3.1
elif plot_option == "Task 1.3.1":
    fig, ax = plt.subplots(figsize=(10, 6))
    new_df = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
    sns.barplot(data=new_df, x='Recession', y='Automobile_Sales', hue='Recession', ax=ax)
    ax.set_xlabel('Recession')
    ax.set_ylabel('Average Automobile Sales')
    ax.set_title('Average Automobile Sales during Recession and Non-Recession')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Non-Recession', 'Recession'])
    st.pyplot(fig)

# Task 1.3.2
elif plot_option == "Task 1.3.2":
    fig, ax = plt.subplots(figsize=(10, 6))
    df_new = df.groupby(['Recession', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
    sns.barplot(data=df_new, x='Recession', y='Automobile_Sales', hue='Vehicle_Type', ax=ax)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Non-Recession', 'Recession'])
    ax.set_title('Vehicle-Wise Sales during Recession and Non-Recession Period')
    st.pyplot(fig)

# Task 1.4
elif plot_option == "Task 1.4":
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    rec_data = df[df['Recession'] == 1]
    non_rec_data = df[df['Recession'] == 0]

    sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession', ax=axes[0])
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('GDP')

    sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recession', ax=axes[1])
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('GDP')

    plt.tight_layout()
    st.pyplot(fig)

# Task 1.5
elif plot_option == "Task 1.5":
    fig, ax = plt.subplots()
    df_nonrec = df[df['Recession'] == 0]
    size = df_nonrec['Seasonality_Weight']
    sns.scatterplot(data=df_nonrec, x='Month', y='Automobile_Sales',
                    size=size, hue='Seasonality_Weight', legend=False, ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Automobile Sales')
    ax.set_title('Seasonality impact on Automobile Sales')
    st.pyplot(fig)

# Task 1.6
elif plot_option == "Task 1.6":
    fig, ax = plt.subplots()
    df_rec = df[df['Recession'] == 1]
    ax.scatter(df_rec['Consumer_Confidence'], df_rec['Automobile_Sales'])
    ax.set_xlabel('Consumer Confidence')
    ax.set_ylabel('Automobile Sales')
    ax.set_title('Consumer Confidence and Automobile Sales during Recessions')
    st.pyplot(fig)

# Task 1.6.1
elif plot_option == "Task 1.6.1":
    fig, ax = plt.subplots()
    df_rec = df[df['Recession'] == 1]
    ax.scatter(df_rec['Price'], df_rec['Automobile_Sales'])
    ax.set_xlabel('Vehicle Price')
    ax.set_ylabel('Automobile Sales')
    ax.set_title('Relationship between Vehicle Price and Sales during Recessions')
    st.pyplot(fig)

# Task 1.7
elif plot_option == "Task 1.7":
    fig, ax = plt.subplots()
    df_rec = df[df['Recession'] == 1]
    df_nonrec = df[df['Recession'] == 0]
    df_recTotal = df_rec['Advertising_Expenditure'].sum()
    df_nonrecTotal = df_nonrec['Advertising_Expenditure'].sum()
    labels = ['Recession', 'Non-Recession']
    sizes = [df_recTotal, df_nonrecTotal]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Advertising Expenditure during Recession and Non-Recession Periods')
    st.pyplot(fig)

# Task 1.8
elif plot_option == "Task 1.8":
    fig, ax = plt.subplots()
    df_rec = df[df['Recession'] == 1]
    df_new = df_rec.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
    labels = df_new.index
    sizes = df_new.values
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Share of Each Vehicle Type in Total Expenditure during Recessions')
    st.pyplot(fig)

# Task 1.9
elif plot_option == "Task 1.9":
    fig, ax = plt.subplots(figsize=(16, 6))
    df_rec = df[df['Recession'] == 1]
    sns.lineplot(data=df_rec, x='unemployment_rate', y='Automobile_Sales',
                 hue='Vehicle_Type', marker='o', ax=ax)
    ax.set_title('Effect of Unemployment Rate on Vehicle Type and Sales')
    ax.set_xlabel('Unemployment Rate')
    ax.set_ylabel('Vehicle Sales')
    ax.legend(title='Vehicle Type')
    plt.tight_layout()
    st.pyplot(fig)