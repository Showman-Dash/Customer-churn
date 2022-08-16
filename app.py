import pandas as pd
import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras

tf_model = keras.models.load_model("tf_model.h5")


def predict(age, partner, dependents, tenure, internet, online_security, online_backup, device_protection,
            technical_support, contract, paperless_billing, payment_method, monthly_charges):
    senior_citizen = 0
    if age > 60:
        senior_citizen = 1
    else:
        senior_citizen = 0

    if partner == 'yes':
        partner = 1
    else:
        partner = 0

    if dependents == 'yes':
        dependents = 1
    else:
        dependents = 0

    if internet == 'DSL':
        internet = 0
    elif internet == 'Fiber optic':
        internet = 1
    else:
        internet = 2

    if online_security == 'No':
        online_security = 0
    elif online_security == 'No internet service':
        online_security = 1
    else:
        online_security = 2

    if online_backup == 'No':
        online_backup = 0
    elif online_backup == 'No internet service':
        online_backup = 1
    else:
        online_backup = 2

    if device_protection == 'No':
        device_protection = 0
    elif device_protection == 'No internet service':
        device_protection = 1
    else:
        device_protection = 2

    if technical_support == 'No':
        technical_support = 0
    elif technical_support == 'No internet service':
        technical_support = 1
    else:
        technical_support = 2

    if contract == 'Month-to-month':
        contract = 0
    elif contract == 'One year':
        contract = 1
    else:
        contract = 2

    if paperless_billing == 'No':
        paperless_billing = 0

    else:
        paperless_billing = 1

    if payment_method == 'Bank transfer (automatic)':
        payment_method = 0
    elif payment_method == 'Credit card (automatic)':
        payment_method = 1
    elif payment_method == 'Electronic check':
        payment_method = 2
    else:
        payment_method = 3

    tenure = (tenure - 1) / 71
    monthly_charges = (monthly_charges - 18.25) / 100.5
    internet = internet / 2
    online_security = online_security / 2
    online_backup = online_backup / 2
    device_protection = device_protection / 2
    technical_support = technical_support / 2
    contract = contract / 2
    payment_method = payment_method / 3

    data_dict = {'SeniorCitizen': senior_citizen,
                 'Partner': partner,
                 'Dependents': dependents,
                 'tenure': tenure,
                 'InternetService': internet,
                 'OnlineSecurity': online_security,
                 'OnlineBackup': online_backup,
                 'DeviceProtection': device_protection,
                 'TechSupport': technical_support,
                 'Contract': contract,
                 'PaperlessBilling': paperless_billing,
                 'PaymentMethod': payment_method,
                 'MonthlyCharges': monthly_charges}
    df = pd.DataFrame(data_dict, columns=['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'InternetService',
                                          'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                          'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges'],
                      index=np.array(range(1)))

    churn_pred_temp = tf_model.predict(df)
    if churn_pred_temp > 0.5:
        churn_pred = 1
    else:
        churn_pred = 0

    return churn_pred


st.title('[XYZ] Company Survey')
st.header('Is the work environment of our company good enough for you?')
st.text('We will predict whether you are happy enough to stay in our company or not!')
st.text("(Fill in the options below)")

col1, col2 = st.columns(2)
with col1:
    name=st.text_input('Enter your name:')

with col2:
    gender = st.selectbox(
        'Enter your gender:',
        ('Male', 'Female'))

col1, col2 = st.columns(2)
with col1:
    age = st.number_input('Enter your age:')

with col2:
    partner = st.selectbox(
        'Do you have a partner ?',
        ('Yes', 'No'))

col1, col2 = st.columns(2)
with col1:
    dependents = st.selectbox(
        'Do you have dependent(s) ?',
        ('Yes', 'No'))

with col2:
    tenure = st.number_input('Enter your tenure (in months):')

col1, col2 = st.columns(2)
with col1:
    st.selectbox(
        'Do you have a phone service ?',
        ('Yes', 'No'))

with col2:
    st.selectbox(
        'Do you have multiple lines ?',
        ('Yes', 'No', 'No phone service'))

col1, col2 = st.columns(2)
with col1:
    internet = st.selectbox(
        'Your internet service provider: ',
        ('DSL', 'Fibre Optic', 'No Internet service'))

with col2:
    online_security = st.selectbox(
        'Do you have online security ?',
        ('Yes', 'No', 'No Internet Service'))

col1, col2 = st.columns(2)
with col1:
    online_backup = st.selectbox(
        'Do you have online backup ?',
        ('Yes', 'No', 'No Internet Service'))

with col2:
    device_protection = st.selectbox(
        'Do you have device protection ?',
        ('Yes', 'No', 'No Internet Service'))

col1, col2 = st.columns(2)
with col1:
    technical_support = st.selectbox(
        'Do you have technical support ?',
        ('Yes', 'No', 'No Internet Service'))

with col2:
    TV_Streaming = st.selectbox(
        'Do you have TV Streaming ?',
        ('Yes', 'No', 'No Internet Service'))

col1, col2 = st.columns(2)
with col1:
    movie_Streaming = st.selectbox(
        'Do you have Movie Streaming ?',
        ('Yes', 'No', 'No Internet Service'))

with col2:
    contract = st.selectbox(
        'Enter your contract term: ',
        ('Month-to-month', '1 year', '2 year'))

col1, col2 = st.columns(2)
with col1:
    paperless_billing = st.selectbox(
        'Do you have paperless billing ?',
        ('Yes', 'No'))

with col2:
    payment_method = st.selectbox(
        'Enter your payment method: ',
        ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'))

col1, col2 = st.columns(2)
with col1:
    monthly_charges = st.number_input('Enter your monthly charges (in $):')

with col2:
    total_charges = st.number_input('Enter your total charges (in $):')

if st.button('Click'):

    churn_pred = predict(age, partner, dependents, tenure, internet, online_security, online_backup, device_protection,
                         technical_support, contract, paperless_billing, payment_method, monthly_charges)
    if (churn_pred == 1):
        st.write('Sorry ', name, ' ,Our work environment is not suitable for you :(')
        st.write('We hope you will find a company where the work environment is good for you.')

    elif (churn_pred == 0):
        st.write('Amazing!! Our work environment is perfectly fine for you ',name,'!')
        st.write('We hope you will have a great time with us ahead :))')
