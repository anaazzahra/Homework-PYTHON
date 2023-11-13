#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # A. Introduction to Pandas DataFrame and Transformation (45pts)

# ## Beginner

# ### 1. Membuat DataFrame Manual (5pts)
# 
# Buatlah dataframe secara manual seperti gambar dibawah ini.
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_1_result.png)

# In[49]:


#no.1 Data Frame Manual
df = {'name' : ['fiqri', 'iqbal', 'monica', 'rama', 'johan'],
      'age' : [23, 21, 22, 24, 26],
      'phone_number' : ['+62813123414', '+6287842464', '+62813125554', '+6287834464', '+62813113414'],
      'ielts_score' : [6.5, None, 7.5, 6.5, 8.0]}

df = pd.DataFrame(df)
print(df)


# ### 2. Analisa Sederhana DataFrame (10pts)
# 
# Lakukan import `application_processed.csv` data kedalam notebook (5pts) dan carilah beberapa informasi pada dataset `application_processed` (5pts) dan jawablah beberapa pertanyaan sebagai berikut:
# 
# a. Column apa saja yang memiliki nilai NaN / None?
# b. Berapa rata-rata pada column `amount_income_total`?
# c. Berapa median pada column `amount_income_total`?
# 
# **Hint**:
# - Menggunakan operasi dasar DataFrame pada topik Introduction Pandas DataFrame and Transformation
# 

# In[50]:


#import data
df2 = pd.read_csv('application_processed.csv')
df2


# In[51]:


#no.2a Kolum dengan nilai NaN/None

df2.info()
#untuk memastikan bahwa di kolum 'occupation_type'
df2_null = df2[df2['occupation_type'].isnull()]
print(df2_null)

#atau juga bisa menggunakan
df2_nan = df2.columns[df2.isnull().any()].tolist()
print('Kolom yang memiliki nilai NaN/None adalah', df2_nan)


# In[52]:


#2.b rata-rata
mean_amount_income_total = df2['amount_income_total'].mean()
print(mean_amount_income_total)

#2.c median
median_amount_income_total = df2['amount_income_total'].median()
print(median_amount_income_total)


# ## Intermediate

# ### 3. Mengolah Dataset (30pts)
# 
# Dengan menggunakan dataset `application_processed.csv` buatlah dataframe baru dengan ketentuan:
# 1. Ambil semua users yang memiliki `email`. (ditandai dengan nilai pada column `flag_email` = 1) dan tidak memilik data `duplicates`. (5pts)
# 2. Buatlah column baru bernama `has_car_and_property` dimana nilainya merupakan range dari `0-1`. `1` apabila `flag_own_car` bernilai `1` dan `flag_own_property` bernilai `1`. `0` apabila terdapat atau semua nilai pada column `flag_own_car` dan `flag_own_property` terdapat angka 0. (5pts)
# 3. Ambil column yang diperlukan yaitu `id`, `gender`, `has_car_and_property`, `income_type`, `education_type`, `family_status`, `housing_type`, `occupation_type`, `amount_income_total`. (5pts)
# 4. Lakukan filter dengan ketentuan sebagai berikut: (5pts)
#     - Memiliki `car` dan `property`
#     - Tidak ada nilai null pada column `occupation_type`
#     - Memiliki value pada column `occupation_type` dengan pola `staff`.
# 5. Sudah dilakukan sorting berdasarkan `income_type` dari `A-Z` dan `amount_income_total` dari `besar ke kecil`. (5pts)
# 6. Simpan kedalam bentuk `.csv` dengan nama `homework_3_result.csv`. (5pts)
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_3_result.png)

# In[53]:


#data email dan tidak duplikatt
df_email = df2[df2['flag_email'] == 1]
df_email1 = df_email.drop_duplicates() #untuk menghapus duplikat
print(df_email1)

#kolum baru
df_email1['has_car_and_property'] = (df_email1['flag_own_car'] & df_email1['flag_own_property']).astype(int)

#3
df_email1 = df_email1[['id', 'gender', 'has_car_and_property', 'income_type', 'education_type', 'family_status', 'housing_type', 'occupation_type', 'amount_income_total']]

# Melakukan filter
df_email1 = df_email1[(df_email1['has_car_and_property'] == 1) & (df_email1['occupation_type'].notnull()) & (df_email1['occupation_type'].str.contains('staff'))]

# Melakukan pengurutan
df_email1 = df_email1.sort_values(by=['income_type', 'amount_income_total'], ascending=[True, False])

# Menyimpan DataFrame dalam format .csv
df_email1.to_csv('homework_3_result.csv', index=False)

pp_df = pd.read_csv('homework_3_result.csv')
print(pp_df)


# # B.DataFrame Aggregation (25pts)

# ## Intermediate

# ### 4. Group By and Aggregate (10pts)
# 
# Dengan menggunakan data `titanic.csv`, buatlah dataframe untuk melihat informasi `max` dan `min` pada column `Age` dan juga informasi `mean` dan `median` pada column `Fare` pada masing-masing PassengerClass atau `Pclass`.
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_4_result.png)

# In[54]:


#import data

df3 = pd.read_csv('titanic.csv')
print(df3)
new_df3 = df3.groupby('Pclass').agg({'Age' : ['max', 'min'],
                                    'Fare' : ['mean', 'median']})
print(new_df3)


# ### 5. Memanfaatkan Pivot Tabel (15pts)
# 
# Buatlah dataframe baru menggunakan fungsi pivot table untuk melihat `Embarked` apa saja yang `average_female_ticket_price` lebih besar daripada `average_male_ticket_price`. Informasi `average_female_ticket_price` dan `average_male_ticket_price` didapatkan dari rata-rata pada column `Fare`.
# 
# **Hint:**
# 1. menggunakan pivot table
# 2. dapat dilihat pada topik `DataFrame Aggregation` bagian `Pivot Table | Reshape Columns and Rows`
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_5_result.png)

# In[55]:


#no.5
df3_pivot = pd.pivot_table(df3,
                           index = ['Embarked'],
                           values = ['Fare'],
                           columns = ['Sex'],
                           aggfunc = ['mean'])
print(df3_pivot)

#filter_pivot = df3_pivot[df3_pivot[('mean', 'Fare', 'female')] > df3_pivot[('mean', 'Fare', 'male')]]
#print(filter_pivot)

#ubah kolom
df3_pivot.columns =['avg_female_ticket_price', 'avg_male_ticket_price'] 

#filter pivot
pivot_filtering = df3_pivot[df3_pivot['avg_female_ticket_price'] > df3_pivot['avg_male_ticket_price']]
pivot_filtering


# # C. DataFrame Combination (30pts)

# ## 6. Melakukan Append pada DataFrame (5pts)
# 
# Buatlah DataFrame seperti pada soal `no.1`. Kemudian tambahkan data tersebut dengan data users yang baru seperti gambar dibawah berikut.
# 
# **New Users Data:**
# 
# ![Expected Result](assets/homework_exercise_6_new.png)
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_6_result.png)

# In[56]:


#no.6
df4 = ({'name' : ['ali', 'adit'],
        'age' : [37, 32],
        'phone_number' : ['None', '+62152155'],
        'ielts_score' : [5.5, 6.0]})
df4 = pd.DataFrame(df4)

#Append

data_append = df.append(df4).reset_index(drop=True)
print(data_append)


# ### 7. Merge DataFrame (25pts)
# 
# Buatlah 2 dataframe mengikuti petunjuk berikut:
# 
# df_1 :  Filter dataset 01 telecom_revenue.csv dengan multiple kondisi (5pts)
# - MonthlyRevenue > 10 
# - Occupation terdiri dari Professional, Student, and Crafts
# 
# df_2 :  Filter dataset 02 telecom_usage.csv dengan multiple kondisi (5pt)
# - nilai UnansweredCalls > BlockedCalls
# 
# Jawablah pertanyaan berikut ini:
# 1. Hitunglah total CustomerID dan rata-rata DroppedCalls untuk masing-masing occupation. (10 Points)
# 2. Pada occupation apa, rata-rata DroppedCalls paling besar? (5 Points)
# 
# **Expected Result:**
# 
# ![Expected Result](assets/homework_exercise_7_result.png)

# In[57]:


#no.7
#import data
df5 = pd.read_csv('01 telecom_revenue.csv')
df6 = pd.read_csv('02 telecom_usage.csv')

#filtering df5
df5_filtering = df5[(df5['MonthlyRevenue'] > 10) &
                  (df5['Occupation'].isin(['Professional', 'Student', 'Crafts']))]
print(df5_filtering)

#filtering df6
df6_filtering = df6[df6['UnansweredCalls'] > df6['BlockedCalls']]
print(df6_filtering)

#merge data
data_merge = pd.merge(df5_filtering, df6_filtering, on='CustomerID', how='left')
print(data_merge)

#hitung total_ID
jawaban_1 = data_merge.groupby('Occupation').agg({'CustomerID' : ['nunique'],
                                                'DroppedCalls' : ['mean']})
print(jawaban_1)

#hitung total id with pivot
pivot_id = pd.pivot_table(data_merge, 
                         index = ['Occupation'],
                         values = ['CustomerID', 'DroppedCalls'],
                         aggfunc ={'CustomerID':'count', 'DroppedCalls':'mean'})
print(pivot_id) #data yang ditampilkan menggunakan pivot sama ddengan total id yang dilakukan dengan sintaks jawaban_1 menggunakan groupby

#jawaban_2
jawaban_2 = jawaban_1['DroppedCalls']['mean'].idxmax()
print(jawaban_2)

#jawaban_2 menggunakan numpy
import numpy as np
max_occupation = np.argmax(jawaban_1['DroppedCalls']['mean'])
print(max_occupation) #hasil menunjukkan index ke-2, berarti occupation student. Hasil itu sama dengan sintaks sebelumnya.


# In[ ]:




