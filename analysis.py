import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('clean_online_retail.csv')

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Quantity'] = df['Quantity'].astype(int)

df = df[df['Quantity'] > 0]
df = df[df['Price'] > 0]
df['Total Price'] = df['Quantity'] * df['Price']

unique_users = df['Customer ID'].nunique()
unique_orders = df['Invoice'].nunique()
total_revenue = df['Total Price'].sum()
aov = total_revenue / unique_orders

print(f"Общая выручка: {total_revenue:,.2f}")
print(f"Уникальных клиентов: {unique_users}")
print(f"Уникальных заказов: {unique_orders}")
print(f"Средний чек (AOV): {aov:.2f}")

df['Date'] = df['InvoiceDate'].dt.date
df['Month'] = df['InvoiceDate'].dt.month

Rev_by_date = df.groupby('Date')['Total Price'].sum().reset_index()
revenue_by_month = df.groupby('Month').agg({'Total Price': 'sum'}).reset_index()

#Выручка по месяцам
plt.figure(figsize=(10, 5))
sns.barplot(x='Month', y='Total Price', data=revenue_by_month, palette='viridis')
plt.title('Выручка по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.show()

#Ежедневная выручка
plt.figure(figsize=(12, 5))
sns.lineplot(data=Rev_by_date, x='Date', y='Total Price', color='blue')
plt.title('Ежедневная выручка')
plt.xlabel('Дата')
plt.ylabel('Выручка')
plt.xticks(rotation=25)
plt.show()

# Аномалии
rev_per_day = Rev_by_date['Total Price'].mean()
std = Rev_by_date['Total Price'].std()
Rev_by_date['is_anomaly'] = Rev_by_date['Total Price'] > (rev_per_day + 2 * std)
anomaly = Rev_by_date[Rev_by_date['is_anomaly'] == True]

#Ежедневная выручка с аномалиями
plt.figure(figsize=(12, 5))
sns.lineplot(data=Rev_by_date, x='Date', y='Total Price', label='Выручка', color='blue', alpha=0.7)
sns.scatterplot(data=anomaly, x='Date', y='Total Price', color='red', label='Аномалии', s=50)
plt.title('Ежедневная выручка с выделением аномалий')
plt.xlabel('Дата')
plt.ylabel('Выручка')
plt.xticks(rotation=25)
plt.show()

# RFM-анализ
max_date = df['InvoiceDate'].max()

rfm = df.groupby('Customer ID').agg(
    last_purchase_per_user=('InvoiceDate', 'max'),
    Frequency=('Invoice', 'nunique'),
    Monetary=('Total Price', 'sum')
).reset_index()

rfm['Recency'] = (max_date - rfm['last_purchase_per_user']).dt.days

rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1, 2, 3], duplicates='drop')

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['M_Score'].astype(str) + rfm['F_Score'].astype(str)

def segment(score):
    if score >= '434':
        return 'Tier 1'
    elif score >= '422':
        return 'Tier 2'
    elif score >= '311':
        return 'Tier 3'
    else:
        return 'Tier 4'

rfm['Segment'] = rfm['RFM_Score'].apply(segment)

print(rfm['Segment'].value_counts())
print(rfm['Segment'].value_counts(normalize=True) * 100)

# График 4: Распределение сегментов
plt.figure(figsize=(8, 5))
rfm['Segment'].value_counts().plot(kind='bar', color=['gold', 'silver', '#cd7f32', 'gray'])
plt.title('Распределение клиентов по RFM-сегментам')
plt.xlabel('Сегмент')
plt.ylabel('Количество клиентов')
plt.show()