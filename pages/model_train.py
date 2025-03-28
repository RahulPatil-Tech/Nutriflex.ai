import random
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load and preprocess data
def load_data():
    # Load your dataset here
    data = pd.read_csv(r'E:\Nutrition assistance\data\nndb_flat.csv')  # Update with the correct path to your file
    data_cleaned = data.drop(columns=['ID', 'ShortDescrip', 'Descrip', 'CommonName', 'MfgName'])
    df1 = pd.get_dummies(data_cleaned, columns=['FoodGroup', 'ScientificName'], drop_first=True)
    df1.fillna(0, inplace=True)
    return df1

data = load_data()

# Splitting and scaling the data
X = data.drop(columns=['Energy_kcal'])
y = data['Energy_kcal']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training function
def train_models():
    models = {
        'Random Forest': RandomForestRegressor(random_state=42),
        'XGBoost': XGBRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'CatBoost': CatBoostRegressor(random_state=47, verbose=0)  # Suppress verbose logging for CatBoost
    }
    results = {}

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        results[name] = {'Model': model, 'MSE': mse, 'RMSE': rmse}

    return results

# Initialize the results as None
results = None

# Streamlit app layout
st.title("Calorie Prediction Model Comparison")
st.write("This app compares the performance of Random Forest, XGBoost, Gradient Boosting, and CatBoost for predicting calorie content.")

# Train models and display results
if st.button("Train Models"):
    with st.spinner("Training models..."):
        results = train_models()

    st.subheader("Model Performance")
    results_df = pd.DataFrame({k: v for k, v in results.items() if isinstance(v, dict)}).T.drop(columns=['Model'])
    st.write(results_df)

    st.bar_chart(results_df['RMSE'])

# User input section for predictions
st.subheader("Predict Calorie Content")

# Create input fields for user to enter nutritional values
nutritional_values = {
    'Protein_g': st.number_input('Protein (g)', min_value=0.0, step=0.1),
    'Fat_g': st.number_input('Fat (g)', min_value=0.0, step=0.1),
    'Sugar_g': st.number_input('Sugar (g)', min_value=0.0, step=0.1),
    'Carb_g': st.number_input('Carbohydrates (g)', min_value=0.0, step=0.1),
    'VitA_mcg': st.number_input('Vitamin A (mcg)', min_value=0.0, step=0.1),
    'VitB6_mg': st.number_input('Vitamin B6 (mg)', min_value=0.0, step=0.1),
    'VitB12_mcg': st.number_input('Vitamin B12 (mcg)', min_value=0.0, step=0.1),
    'VitC_mg': st.number_input('Vitamin C (mg)', min_value=0.0, step=0.1),
    'VitE_mg': st.number_input('Vitamin E (mg)', min_value=0.0, step=0.1),
    'Thiamin_mg': st.number_input('Thiamin (mg)', min_value=0.0, step=0.1),
    'Calcium_mg': st.number_input('Calcium (mg)', min_value=0.0, step=0.1),
    'Copper_mcg': st.number_input('Copper (mcg)', min_value=0.0, step=0.1),
    'Iron_mg': st.number_input('Iron (mg)', min_value=0.0, step=0.1),
    'Magnesium_mg': st.number_input('Magnesium (mg)', min_value=0.0, step=0.1),
    'Manganese_mg': st.number_input('Manganese (mg)', min_value=0.0, step=0.1)
}

# Prepare the input for prediction
input_data = {key: value for key, value in nutritional_values.items()}

# Convert the input data into a DataFrame to match the feature set
input_df = pd.DataFrame([input_data])

# Ensure the DataFrame has the same columns as X
input_full_df = pd.DataFrame(columns=X.columns)  # Create an empty DataFrame with the same columns as X
input_full_df = pd.concat([input_full_df, input_df], ignore_index=True)  # Append the user input data

# Scale the input data
input_data_scaled = scaler.transform(input_full_df)

# Make predictions with the selected model
model_choice = st.selectbox('Choose a model for prediction', ['Random Forest', 'XGBoost', 'Gradient Boosting', 'CatBoost'])

if st.button("Predict Calorie Content"):
    if results is None:
        st.warning("Models are not trained yet. Training models now...")
        with st.spinner("Training models..."):
            results = train_models()

    # Use the selected model for prediction
    model = results[model_choice]['Model']
    prediction = model.predict(input_data_scaled)
    st.write(f"Predicted Calorie Content: {prediction[0]:.2f} kcal")

    # Add recommendation based on predicted calorie content
    if prediction[0] < 200:
        recommendation = "This is a low-calorie meal. It can be great for a light snack or a healthy meal option if you're aiming to reduce your calorie intake."
        recipe_links = [
            "https://www.bbcgoodfood.com/recipes/super-veg-salad",
            "https://www.eatingwell.com/recipe/268000/quinoa-salad/"
        ]
    elif 200 <= prediction[0] < 500:
        recommendation = "This meal has a moderate calorie content. It's suitable for a balanced meal without exceeding daily intake recommendations."
        recipe_links = [
            "https://www.delish.com/cooking/recipe-ideas/a32890269/easy-buddha-bowl-recipe/",
            "https://www.loveandlemons.com/grain-bowls/"
        ]
    else:
        recommendation = "This is a high-calorie meal. It's ideal if you're looking for an energy-dense option but be cautious if you're watching your calorie intake."
        recipe_links = [
            "https://www.foodnetwork.com/recipes/high-calorie-smoothie",
            "https://www.thespruceeats.com/quick-beef-stroganoff-4783575"
        ]

    st.subheader("Recommendation")
    st.write(recommendation)

    # Provide random recipe links from the list
    st.subheader("Suggested Recipes")
    selected_recipe = random.choice(recipe_links)
    st.write(f"Check out this recipe: [Click here]({selected_recipe})")
