import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca data csv menggunakan library pandas
bike_data_hour =  pd.read_csv('Bike-sharing-dataset/hour.csv')
bike_data_day =  pd.read_csv('Bike-sharing-dataset/day.csv')

# Mengkonversikan tipe object menjadi tipe datetime
bike_data_day['dteday'] = pd.to_datetime(bike_data_day['dteday'])
bike_data_hour['dteday'] = pd.to_datetime(bike_data_hour['dteday'])

bike_data_day['day_of_week'] = bike_data_day['dteday'].dt.day_name()

min_date = bike_data_day["dteday"].min()
max_date = bike_data_day["dteday"].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    # st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("DigiBike")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.caption("Assuming the cost to rent a bike is $10 AUD.")

main_df_day = bike_data_day[(bike_data_day["dteday"] >= str(start_date)) & 
                (bike_data_day["dteday"] <= str(end_date))]

main_df_hour = bike_data_hour[(bike_data_hour["dteday"] >= str(start_date)) & 
                (bike_data_hour["dteday"] <= str(end_date))]

st.header("Bike Rental Dashboard :sparkles:")


st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
total_rental = main_df_day['cnt'].sum()
with col1:
    st.metric("Total Rental Bikes", value=total_rental)
 
with col2:
    total_revenue = format_currency(total_rental*10, "$", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)



def plot_and_show(title, x_label, y_label, data, x, y, kind, ax):
    if kind == 'line':
        sns.lineplot(x=data.groupby(x)[y].sum().index, y=data.groupby(x)[y].sum().values, color='skyblue', ax=ax)
    elif kind == 'bar':
        sns.barplot(x=data.groupby(x)[y].sum().index, y=data.groupby(x)[y].sum().values, color='skyblue', ax=ax)

    ax.set_title(title, loc="center")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

# Create subplots
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(12, 18))

# Plot Daily Trend
plot_and_show('Daily Bike Rental Trend', 'Date', 'Total Rental Count', main_df_day, 'dteday', 'cnt', 'line', ax=ax[0])
# Plot Hour Trend
plot_and_show('Bike Rental Pattern at Different Hours of the Day', 'Hour of the Day', 'Total Rental Count', main_df_hour, 'hr', 'cnt', 'bar', ax=ax[1])
# Plot Day Trend
daily_trend = main_df_hour.groupby('weekday')['cnt'].sum()
daily_trend.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
plot_and_show('Bike Rental Pattern at Different Day of the Week', 'Day of the Week', 'Total Rental Count', main_df_hour, 'weekday', 'cnt', 'bar', ax=ax[2])

# Display the plots using Streamlit
st.pyplot(fig)

st.subheader("Total Rent Bike by Category")

# Mengubah ke temperatur yang aslinya sebelum dinormalisasikan
main_df_day['temp_normal'] = main_df_day['temp']*41

# Membuat column temperature_category berdasarkan percentil
cold_percentile = main_df_day['temp_normal'].quantile(0.25)
moderate_percentile = main_df_day['temp_normal'].quantile(0.75)

main_df_day['temperature_category'] = pd.cut(main_df_day['temp_normal'], bins=[-float('inf'), cold_percentile, moderate_percentile, float('inf')],
                                              labels=['Cold', 'Moderate', 'Hot'])



# Plot Total Rent by Category
fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(12, 6))

sns.countplot(x='temperature_category', data=main_df_day, color='skyblue', ax=ax[0])

ax[0].set_title('Rental Count Based on Temperature Category')
ax[0].set_xlabel('Temperature Category')
ax[0].set_ylabel('Total Rental Count')



# Plot Total Rent by Category
weather_mapping = {
    1: 'Clear',
    2: ' Mist',
    3: 'Light Rain',
    4: 'Heavy Rain',
}
main_df_day['weather_category'] = main_df_day['weathersit'].map(weather_mapping)

sns.countplot(x='weather_category', data=main_df_day, color='skyblue', ax=ax[1])

ax[1].set_title('Rental Count Based on Temperature Category')
ax[1].set_xlabel('Weather Category')
ax[1].set_ylabel('Total Rental Count')

st.pyplot(fig)