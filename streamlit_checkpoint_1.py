import streamlit as st
import pandas as pd
import numpy as np
from  ydata_profiling import ProfileReport
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def app_checkpoint():
 df = pd.read_csv(r'C:\Users\Hp\Desktop\dataset\Streamlit\Churn_encoded.csv')
 # use a random features to execute the python file
 df_encoder = df.sample(n=5000, axis=0, random_state=42)
# Generate Profile Report :
 report_encoded = ProfileReport(df_encoder, title = 'report espresso churn dropping columns')
 report_path = r"C:\Users\Hp\Desktop\dataset\Streamlit\report.html" 
 report_encoded.to_file(report_path)
    # Streamlit app
 st.title("CHURN ESPRESSO")
 st.title("Random forrest classifier with Streamlit : CHURN ESPRESSO")
 st.write("Data Frame :")
 if st.button('Data Head') :
    st.write(df_encoder.head())

 if st.button('Describe') :
    st.write(df_encoder.describe())

 if st.button('Correlation'): 
    st.write(df_encoder.corr(method='spearman'))

 # Display Profile Report in Streamlit 
 if st.button('Pandas report : html file save') :
     st.write("Profile Report") 
     st.components.v1.iframe(report_path, width=700, height=1000, scrolling=True)
 random_forest = RandomForestClassifier(n_estimators=10, random_state=42)
 le = LabelEncoder()
 X = df_encoder.drop(columns=['CHURN'])
 y = df_encoder['CHURN']
 X_train, X_test, y_train,y_test = train_test_split(X,y, test_size=0.2, random_state=42)
 
 le.fit(df_encoder['REGION'])
 if st.button('Random forest classifier train'):
    # Train the classifier
    random_forest.fit(X_train, y_train)
    
    # Make predictions
    y_pred = random_forest.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    st.write("Model Accuracy", accuracy)
       
    st.write("Classification Report")
    st.write(report)
    y_pred_tree = random_forest.predict(X_test)

    # Evaluate the model
    accuracy_tree = accuracy_score(y_test, y_pred)
    report_tree = classification_report(y_test, y_pred_tree, output_dict=True)
    st.write("# Model Accuracy")
    st.write(accuracy_tree)
    
    st.write("# Classification Report")
    st.write(report_tree)


 st.write("# Input Features for Prediction")
# Input fields for features
 region_input = st.selectbox('Region', df_encoder['REGION'].unique())
 tenure_input = st.number_input('Tenure', min_value=int(df_encoder['TENURE'].min()), max_value=int(df_encoder['TENURE'].max()))
 regularity_input = st.selectbox('Regularity', df_encoder['REGULARITY'].unique())

 # Capture additional features if they exist
 additional_columns = set(X.columns) - {'REGION', 'TENURE', 'REGULARITY'}

 additional_inputs = {}
 for col in additional_columns:
    additional_inputs[col] = st.number_input(col, value=df_encoder[col].mean())

# Encoding the region input
 region_encoded = le.transform([region_input])[0]

# Create input data for prediction
 input_data_dict = {'REGION': region_encoded, 'TENURE': tenure_input, 'REGULARITY': regularity_input}
 input_data_dict.update(additional_inputs)  # Add additional inputs to the dictionary

 input_data = pd.DataFrame(input_data_dict, index=[0])

 if st.button('Validate Prediction'):
    # Make prediction for the input data
    prediction = random_forest.predict(input_data)
    st.write("## Prediction Result")
    st.write("The prediction for the input data is:", "Churn" if prediction[0] else "No Churn")


if __name__ == '__main__' :
    app_checkpoint()
    