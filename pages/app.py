import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
import random
import google.generativeai as genai
import os
import plotly.graph_objects as go
from PIL import Image

# Configure API key for Google Generative AI
os.environ["AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"] = "AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"
genai.configure(api_key=os.environ["AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"])
# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model_path = os.path.join('E:', 'Nutrition assistance',
                          'models', 'random_forest_model.pkl')
# Function to load pre-saved models


def load_model(model_file):
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    return model


# Load your pre-saved models
rf_model = load_model(r'D:\Nutrition assistance\models\random_forest_model.pkl')
xgb_model = load_model(r'D:\Nutrition assistance\models\XGBoost.pkl')
gb_model = load_model(r'D:\Nutrition assistance\models\gradient_boosting.pkl')
catboost_model = load_model(r'D:\Nutrition assistance\models\cat_boost.pkl')

# Load the training data for preprocessing
# Update with your dataset path
data = pd.read_csv(r'D:\Nutrition assistance\data\nndb_flat.csv')
data_cleaned = data.drop(
    columns=['ID', 'ShortDescrip', 'Descrip', 'CommonName', 'MfgName'])
df1 = pd.get_dummies(data_cleaned, columns=[
                     'FoodGroup', 'ScientificName'], drop_first=True)
df1.fillna(0, inplace=True)

# Fit the scaler on the training data
scaler = StandardScaler()
X = df1.drop(columns=['Energy_kcal'])
X_scaled = scaler.fit_transform(X)

# Define each page as a function


def home():
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
    }

    .stButton button {
        font-size: 50px; /* Adjusted font size for buttons */
        font-weight: bold;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif;
        font-size: 30px;
    }

    p, li {
        font-family: 'Roboto', sans-serif;
        font-size: 24px; /* Adjusted font size for markdown text */
    }

    </style>
    """,
    unsafe_allow_html=True
    )

    st.title("Welcome to NUTRIFLEX!")

    # Introduction
    st.write(
        "In today's fast-paced world, maintaining a balanced diet is essential for overall health and well-being. "
        "NUTRIFLEX is designed to make personalized nutrition accessible and engaging for everyone."
    )

    # Image
    st.image(r"D:\Nutrition assistance\image\Wearble1.jpg", use_column_width=True)  # Update with your image path

    # What We Offer Section
    st.header("What We Offer")

    st.subheader("Calorie Prediction")
    st.write(
        "Accurately estimate calorie content based on your nutritional input using advanced machine learning models."
    )

    st.subheader("Personalized Meal Planning")
    st.write(
        "Generate customized meal plans that align with your Basal Metabolic Rate (BMR) and Total Energy Expenditure (TEE), "
        "ensuring you meet your dietary goals.")

    st.subheader("Recipe Recommendations")
    st.write(
        "Discover delicious recipes that cater to your preferences, dietary restrictions, and caloric requirements."
    )

    st.subheader("Gamified Experience")
    st.write(
        "Engage with our interactive features that turn food tracking into a rewarding game, encouraging healthier eating habits."
    )

    st.subheader("AI-Based Recipe Suggestions for Specific Health Conditions")
    st.write(
        "Receive AI-generated recipe suggestions designed for specific health conditions, such as managing stress and improving mood. "
        "Enjoy meals that promote relaxation, focus, and emotional balance."
    )

    st.subheader("Gut Health Meal Plans")
    st.write(
        "Generate personalized meal plans based on your gut microbiome data. By understanding your unique gut health, "
        "we help you make dietary choices that improve digestion, support immunity, and optimize overall well-being."
    )

    # Our Mission Section
    st.header("Our Mission")
    st.write(
        "At NutriFLEX, our mission is to empower individuals to make informed dietary choices through the use of technology. "
        "We believe that everyone deserves access to personalized nutrition assistance that is both effective and enjoyable."
        )

    # Call to Action
    st.write(
        "Use the navigation menu to explore different features of the app. "
        "Let's embark on this journey towards better nutrition together!"
        )
    st.markdown("---")
    st.write("© 2024 NutriFLEX. All rights reserved.")
# BMR Calculation (Mifflin-St Jeor Equation)


def calculate_bmr(age, gender, weight, height):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

# Gamify Experience


def game_fy():
    # Extract food items (assuming there's a column named 'FoodName')
    food_items = data['ShortDescrip'].unique()

    # Create a title for the app
    st.title("Food Intake Game")

    # Checkbox selection for food items
    selected_foods = st.multiselect("Select your food intake:", food_items)

    # Reward system
    reward_points = 0
    if selected_foods:
        # Example: 10 points per food item selected
        reward_points = len(selected_foods) * 10

    # Display rewards
    st.write("You have selected:", selected_foods)
    st.success(f"Total Reward Points: {reward_points}")

    # Optional: Display a message based on the total points
    if reward_points > 0:
        st.success("Great job! Keep up the healthy eating!")
    else:
        st.warning("Please select some food items to earn rewards.")

# Calculate TEE based on activity level


def calculate_tee(bmr, activity_level):
    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "super active": 1.9
    }
    return bmr * activity_factors.get(activity_level, 1.2)

# Generate meal plan based on TEE


def generate_meal_plan(tee, dataset):
    daily_kcal = tee

    # Define a balanced macro distribution: 50% carbs, 20% protein, 30% fat
    total_protein = 0.2 * daily_kcal / 4
    total_fat = 0.3 * daily_kcal / 9
    total_carbs = 0.5 * daily_kcal / 4

    # Filter food items from dataset based on macronutrient content
    filtered_data = dataset[['ShortDescrip', 'Energy_kcal',
                             'Protein_g', 'Fat_g', 'Carb_g']].dropna()

    meal_plan = pd.DataFrame(
        columns=['ShortDescrip', 'Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g'])
    total_energy, total_protein_g, total_fat_g, total_carb_g = 0, 0, 0, 0

    # Iteratively add food items until the goal is reached
    for index, row in filtered_data.iterrows():
        if (total_energy < daily_kcal) and (total_protein_g < total_protein) and (total_fat_g < total_fat) and (total_carb_g < total_carbs):
            meal_plan = pd.concat([meal_plan, row.to_frame().T], ignore_index=True)
            total_energy += row['Energy_kcal']
            total_protein_g += row['Protein_g']
            total_fat_g += row['Fat_g']
            total_carb_g += row['Carb_g']

    return meal_plan

# Function to calculate BMR and generate meal plan


def calculate_BMR():
    st.title("Meal Planner based on Physique")

    age = st.number_input("Enter your age:", min_value=10,
                          max_value=100, value=25)
    gender = st.selectbox("Select gender:", ['Male', 'Female'])
    weight = st.number_input("Enter weight (in kg):",
                             min_value=20.0, max_value=800.0)
    height = st.number_input("Enter height (in cm):",
                             min_value=100.0, max_value=700.0)
    activity_level = st.selectbox("Select activity level:",
                                  ['sedentary', 'lightly active', 'moderately active', 'very active', 'super active'])

    if st.button("Generate Meal Plan"):
        bmr = calculate_bmr(age, gender, weight, height)
        tee = calculate_tee(bmr, activity_level)

        # Check if TEE is valid before generating meal plan
        if tee <= 0:
            st.error("Calculated TEE value is invalid. Please check your input.")
            return

        meal_plan = generate_meal_plan(tee, data)

        st.write(f"Your BMR: {bmr:.2f} kcal")
        st.write(f"Your TEE: {tee:.2f} kcal")
        st.write("\n### Meal Plan based on your TEE:\n")

        if meal_plan.empty:
            st.write("No meal plan could be generated based on the provided TEE.")
        else:
            st.dataframe(meal_plan)

# Define a function to generate the recipe based on calorie input


def smart_recipe_recommendation():
    st.title("Smart Recipe Recommendation")

    # Input: Take desired calorie count from the user
    calorie_input = st.number_input(
        "Enter your desired calorie count:", min_value=100, max_value=2000, step=50, value=500)

    # Input: Take desired protein intake from the user
    protein_input = st.text_input("Enter your protein intake:")

    # Input: Take allergy (if their of certain ingredients)
    allergy_inputs = st.text_input("Enter allergy ingredient (if any): ")

    # Button to trigger recipe generation
    generate_button = st.button("Generate Recipe")

    # Function to generate the recipe based on calorie input
    def generate_recipe(calories, protein, allergy):
        prompt = f"""
        I want to generate a recipe for a healthy meal that contains around {calories} calories.
        The meal should include the following:
        - Protein: {protein}
        - Vegetables: broccoli, spinach
        - Healthy fats: olive oil or avocado
        - Allergy:{allergy}
        Provide a step-by-step recipe, including ingredients and instructions,excluding {allergy} ingredient and the estimated calorie breakdown.
        """

        try:
            # Define the generative model with the selected configuration
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            # Start a chat session and send the prompt to the model
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)

            # Return the response text if valid
            return response.text if response else "No response from AI model. Please try again."

        except Exception as e:
            # Handle potential errors
            return f"An error occurred: {str(e)}"

    # Generate and display the recipe when the button is clicked
    if generate_button:
        if protein_input:  # Ensure protein input is provided
            recipe = generate_recipe(
                calorie_input, protein_input, allergy_inputs)
            st.write(recipe)
        else:
            st.error("Please provide the protein intake value.")


def Smart_health():
    st.title("Generate AI-based recipe suggestions for specific health conditions")

    # Input : Take an update of patients past or present Health condition
    health_input = st.text_input("Enter the Health Condition of patient:")
    stress_level_input = st.slider("Stress Level (1-10)", 1, 10)
    dietary_preferences_input = st.text_input("Dietary Preferences (e.g., vegan, vegetarian, gluten-free)", "")

    # Button to trigger recipe generation
    generate_button1 = st.button("Get Meal Suggestions and Recipe")

    def generate_health(health, stress_level, dietary_preferences):
        prompt1 = f"""You are a nutritionist specializing in dietary plans for people with {health}.
        Based on the user's current preferences:
        Stress Level: {stress_level} 
        Dietary Preferences: {dietary_preferences}
        
        Please create a healthy recipe that takes into account the necessary dietary restrictions for this condition. 
        Make sure the recipe is nutritious, balanced, and easy to prepare. Include the ingredients and preparation steps.
        """

        # Define the generative model with the selected configuration
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start a chat session and send the prompt to the model
        chat_session1 = model.start_chat(history=[])
        response1 = chat_session1.send_message(prompt1)

        return response1.text

    if generate_button1:
        recipe1 = generate_health(
            health_input, stress_level_input, dietary_preferences_input)
        st.write(recipe1)


def gut_bacterial_anal():
    st.title("Generate a personalized meal plan based on gut microbiome data.")
    st.write("The AI recommends foods to balance the gut flora, support digestion, and improve overall gut health.")

    lactobacillus_input = st.selectbox(
        "Lactobacillus Level", ["low", "normal", "high"])
    bifidobacterium_input = st.selectbox(
        "Bifidobacterium Level", ["low", "normal", "high"])
    firmicutes_input = st.selectbox(
        "Firmicutes Level", ["low", "normal", "high"])
    bacteroidetes_input = st.selectbox(
        "Bacteroidetes Level", ["low", "normal", "high"])
    akkermansia_input = st.selectbox(
        "Akkermansia Level", ["low", "normal", "high"])
    clostridium_difficile_input = st.selectbox(
        "Clostridium difficile Presence", ["present", "absent"])
    generate_button2 = st.button("Generate Plan")

    # Function to call OpenAI API and generate meal plan
    def generate(lactobacillus, bifidobacterium, firmicutes, bacteroidetes, akkermansia, clostridium_difficile):
        prompt2 = f"""
        You are a nutritionist specialized in gut health. Based on the following microbiome data:
        Lactobacillus: {lactobacillus}
        Bifidobacterium: {bifidobacterium}
        Firmicutes: {firmicutes}
        Bacteroidetes: {bacteroidetes}
        Akkermansia: {akkermansia}
        Clostridium difficile: {clostridium_difficile}
        
        Please create a personalized meal plan to improve gut health, focusing on:
        1. Increasing beneficial bacteria like Lactobacillus and Bifidobacterium.
        2. Reducing harmful bacteria like Clostridium difficile.
        3. Enhancing microbial diversity.
        
        Include breakfast, lunch, dinner, and snacks, with detailed nutritional recommendations.
        """
        # Define the generative model with the selected configuration
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start a chat session and send the prompt to the model
        chat_session2 = model.start_chat(history=[])
        response2 = chat_session2.send_message(prompt2)

        return response2.text

    if generate_button2:
        # Call the generate_meal_plan function and display the result
        plan = generate(lactobacillus_input, bifidobacterium_input, firmicutes_input,
                        bacteroidetes_input, akkermansia_input, clostridium_difficile_input)
        st.write(plan)


def mental_health_insights():
    st.title("Personalized Food and Activity Suggestions Based on Your Mood")
    st.write("The AI recommends foods and activities that can help improve your mental well-being.")

    # Collect mood score from the user
    mood_input = st.selectbox(
        "How do you feel today? (Mood score)", ["Very Bad (1-2)", "Bad (3-4)", "Okay (5-6)", "Good (7-8)", "Very Good (9-10)"]
    )
    generate_button2 = st.button("Generate Suggestions")

    # Function to call OpenAI API and generate suggestions
    def generate_suggestions(mood_score):
        # Set the appropriate prompt based on mood_score
        if mood_score in ["Very Bad (1-2)", "Bad (3-4)"]:
            prompt = f"""
        The user is feeling down with a mood score of {mood_score}. 
        Suggest comforting foods that can improve mental well-being, and activities that can help the user relax and feel better.
        """
        elif mood_score in ["Okay (5-6)"]:
            prompt = f"""
        The user has a mood score of {mood_score}. 
        Suggest energizing and mood-boosting foods, and recommend activities that can uplift the user's spirits.
        """
        else:
            prompt = f"""
        The user is feeling great with a mood score of {mood_score}. 
        Suggest foods and activities that can help maintain the user's positive mood and keep their energy high.
        """

        # Define the generative model with the selected configuration
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,)

        # Start a chat session and send the prompt to the model
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        return response.text

    if generate_button2:
        suggestions = generate_suggestions(mood_input)
        st.write(suggestions)


def calorie_prediction():
    st.title("Calorie Prediction Model Comparison")
    st.write(
        "This app compares the performance of various models for predicting calorie content.")

    # User input section
    st.header("Input Nutritional Values")
    protein_g = st.number_input("Protein (g)", min_value=0.0, step=0.1)
    fat_g = st.number_input("Fat (g)", min_value=0.0, step=0.1)
    sugar_g = st.number_input("Sugar (g)", min_value=0.0, step=0.1)
    vitamin_a_mcg = st.number_input("Vitamin A (mcg)", min_value=0.0, step=1.0)
    vitamin_b6_mg = st.number_input(
        "Vitamin B6 (mg)", min_value=0.0, step=0.01)
    vitamin_b12_mcg = st.number_input(
        "Vitamin B12 (mcg)", min_value=0.0, step=0.1)
    vitamin_c_mg = st.number_input("Vitamin C (mg)", min_value=0.0, step=0.1)
    vitamin_e_mg = st.number_input("Vitamin E (mg)", min_value=0.0, step=0.01)
    thiamin_mg = st.number_input("Thiamin (mg)", min_value=0.0, step=0.01)
    calcium_mg = st.number_input("Calcium (mg)", min_value=0.0, step=1.0)
    copper_mcg = st.number_input("Copper (mcg)", min_value=0.0, step=0.1)
    iron_mg = st.number_input("Iron (mg)", min_value=0.0, step=0.01)
    magnesium_mg = st.number_input("Magnesium (mg)", min_value=0.0, step=0.1)
    manganese_mg = st.number_input("Manganese (mg)", min_value=0.0, step=0.01)

    # Prepare the input data for the model
    input_data = {
        'Protein_g': protein_g,
        'Fat_g': fat_g,
        'Sugar_g': sugar_g,
        'VitaminA_mcg': vitamin_a_mcg,
        'VitaminB6_mg': vitamin_b6_mg,
        'VitaminB12_mcg': vitamin_b12_mcg,
        'VitaminC_mg': vitamin_c_mg,
        'VitaminE_mg': vitamin_e_mg,
        'Thiamin_mg': thiamin_mg,
        'Calcium_mg': calcium_mg,
        'Copper_mcg': copper_mcg,
        'Iron_mg': iron_mg,
        'Magnesium_mg': magnesium_mg,
        'Manganese_mg': manganese_mg
    }

    # Create a DataFrame from the input data
    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df)  # One-hot encode
    # Match original features
    input_df = input_df.reindex(columns=X.columns, fill_value=0)

    # Prediction button
    if st.button("Predict"):
        # Initialize prediction variables
        rf_prediction = xgb_prediction = gb_prediction = catboost_prediction = None

        # Predict using each model
        gb_prediction = gb_model.predict(input_df)[0]

        # Display predictions
        st.subheader("Predicted Calorie Content")
        st.write(f"Predicted Calorie: {gb_prediction:.2f} kcal")


def recipe_recommendation():
    st.title("Recipe Recommendation")
    st.write(
        "Get personalized recipe recommendations based on your predicted calorie content.")

    # User input section for manual calorie input or predicted value
    predicted_calories = st.number_input(
        "Enter Predicted Calorie Content (kcal)", min_value=0.0, step=1.0)

    # Provide recommendation based on calorie content
    if predicted_calories > 0:
        if predicted_calories < 200:
            recommendation = "This is a low-calorie meal. Ideal for light snacks or diet-friendly meals."
            recipe_links = [
                "https://www.bbcgoodfood.com/recipes/super-veg-salad",
                "https://www.eatingwell.com/recipe/268000/quinoa-salad/"
            ]
        elif 200 <= predicted_calories < 500:
            recommendation = "This is a moderately calorie-dense meal. Great for balanced nutrition."
            recipe_links = [
                "https://www.delish.com/cooking/recipe-ideas/a32890269/easy-buddha-bowl-recipe/",
                "https://www.loveandlemons.com/grain-bowls/"
            ]
        else:
            recommendation = "This is a high-calorie meal. Best for energy-dense meals or post-workout recovery."
            recipe_links = [
                "https://www.foodnetwork.com/recipes/high-calorie-smoothie",
                "https://www.thespruceeats.com/quick-beef-stroganoff-4783575"
            ]

        st.subheader("Recommendation")
        st.write(recommendation)

        # Provide a random recipe link
        st.subheader("Suggested Recipe")
        selected_recipe = random.choice(recipe_links)
        st.write(f"Check out this recipe: [Click here]({selected_recipe})")

    else:
        st.write("Please enter a valid calorie content to get a recommendation.")


def personalized_form():
    st.header("Display personalized meal suggestions based on user input.")
    # Filter relevant columns for analysis
    relevant_columns = ['ShortDescrip',
                        'Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g']
    filtered_data1 = data[relevant_columns]

    # Ensure numeric columns are converted properly
    filtered_data1['Energy_kcal'] = pd.to_numeric(
        filtered_data1['Energy_kcal'], errors='coerce')
    filtered_data1['Protein_g'] = pd.to_numeric(
        filtered_data1['Protein_g'], errors='coerce')
    filtered_data1['Fat_g'] = pd.to_numeric(
        filtered_data1['Fat_g'], errors='coerce')
    filtered_data1['Carb_g'] = pd.to_numeric(
        filtered_data1['Carb_g'], errors='coerce')

    # Total calorie intake calculation
    total_calories = filtered_data1['Energy_kcal'].sum()
    st.write(f"Total Calories Consumed: {total_calories}")

    # User input for health goals
    target_calories = st.number_input(
        "Enter your target daily calorie intake:", value=2000)

    # Function to suggest meals based on current intake
    def suggest_meals(current_calories, target_calories, filtered_data):
        if current_calories > target_calories:
            # Suggest lower-calorie meals
            suggestions = filtered_data[filtered_data['Energy_kcal'] < (
                target_calories / 3)]
        else:
            # Suggest higher-calorie meals for muscle gain
            suggestions = filtered_data[filtered_data['Energy_kcal'] > (
                target_calories / 3)]
        return suggestions

    # Suggest meals based on user input
    meal_suggestions = suggest_meals(
        total_calories, target_calories, filtered_data1)

    # Display meal suggestions
    st.subheader("Meal Suggestions Based on Your Intake")
    st.write(meal_suggestions)

    # Assuming nutrient_sums is already defined as you have in your code
    nutrient_sums = filtered_data1[[
        'Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g']].sum()

    # Create a Plotly bar chart
    fig = go.Figure()

    # Add data to the figure
    fig.add_trace(go.Bar(
        x=nutrient_sums.index,
        y=nutrient_sums.values,
        marker_color='blue'  # You can customize the color
    ))

    # Update the layout of the figure
    fig.update_layout(
        title="Nutrient Intake Overview",
        xaxis_title="Nutrients",
        yaxis_title="Total Intake",
        plot_bgcolor='rgba(255, 255, 255, 0.8)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # No background color for paper
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)


def about():
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
    }

    .stButton button {
        font-size: 50px; /* Adjusted font size for buttons */
        font-weight: bold;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif;
        font-size: 30px;
    }

    p, li {
        font-family: 'Roboto', sans-serif;
        font-size: 24px; /* Adjusted font size for markdown text */
    }

    </style>
    """,
    unsafe_allow_html=True
    )

    # Set the title of the app
    st.title("About the Creator")

    # Add the image (make sure to replace the image path accordingly)
    image = Image.open(r"D:\Nutrition assistance\image\A_professional-looking_portrait_of_a_tech-savvy_cr.webp")
    st.image(image, caption="The Creator behind NUTRIFLEX", use_column_width=True)

    # Write the About section
    st.write("""
The creator behind **NutriFLEX** is a passionate innovator with expertise in data science, AI, and health technology. 
Dedicated to improving how people interact with nutrition and wellness, they combine machine learning, predictive 
analytics, and human-centered design to develop practical, user-friendly tools that make everyday life healthier and more manageable.

With a strong foundation in nutrition science and technology, the creator has worked on various AI-driven projects, including personalized 
health tracking, AI-powered meal planners, and mental well-being integration. Their vision is to empower individuals with smart tools that 
adapt to their unique needs, helping them achieve their health goals and maintain a balanced lifestyle. **NutriFLEX** reflects this mission 
by offering an intuitive platform that adjusts to user goals, provides personalized meal suggestions, and integrates modern technologies like 
voice assistance and wearables.

Beyond their work on health tech, the creator enjoys exploring the latest in food science, psychology, and fitness. They share their insights, 
progress, and wellness tips with a vibrant community online.
             
Stay connected to learn more about cutting-edge health tech and AI-driven wellness solutions!
""")
     
    st.header(" Follow the creator on social media:")
    # Add social media links
    st.markdown("""
[![Instagram](https://img.shields.io/badge/Instagram-@py_rex_47-%23E4405F?style=for-the-badge&logo=instagram)](https://instagram.com/py_rex_47)
[![Twitter](https://img.shields.io/badge/Twitter-@Patil5432-%231DA1F2?style=for-the-badge&logo=twitter)](https://x.com/Patil5432)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-YourLinkedInProfile-%230A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/rahul-patil-4bb533209)
""")
    # Join Us Section
    st.header("Join Us on Your NutriFLEX Journey")
    st.write(
        "Whether you're looking to lose weight, gain muscle, or simply eat healthier, NutriFlex is here to support you every step of the way. "
        "Our user-friendly interface and expert-backed recommendations will help you achieve your nutrition goals."
    )

    # Get in Touch Section
    st.header("Get in Touch")
    st.write(
        "We would love to hear from you! If you have any questions, feedback, or suggestions, please reach out to us at rp3252154@gmail.com.")
    st.image("https://images.pexels.com/photos/7564224/pexels-photo-7564224.jpeg?auto=compress&cs=tinysrgb&w=600",use_column_width=True)  # Replace with your image URL

    # Footer
    st.markdown("---")
    st.write("© 2024 NutriFLEX. All rights reserved.")
 

# Main App with Option Menu for Navigation
st.sidebar.image(r"D:\Nutrition assistance\image\NUTRIFLEX.jpg",
                 use_column_width=True)  # Add your logo here
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Calorie Prediction", "Meal Planner", "Gut Health","Mood Booster", "Recipe Recommendation",
                 "Smart Recipe Recommendation", "Smart Health", "Gamification", "Personalized Form", "About"],  # required
        icons=['house', 'calculator', 'book', 'clipboard-check','emoji-smile-fill', 'bag-heart',
               'bag', 'heart', 'controller', 'clipboard', 'info-circle'],
        menu_icon="app-indicator", default_index=0,
        orientation="vertical")

# Display the selected page
if selected == "Home":
    home()
elif selected == "Calorie Prediction":
    calorie_prediction()
elif selected == "Meal Planner":
    calculate_BMR()
elif selected == "Recipe Recommendation":
    recipe_recommendation()
elif selected == "Smart Recipe Recommendation":
    smart_recipe_recommendation()
elif selected == "Gut Health":
    gut_bacterial_anal()
elif selected == "Smart Health":
    Smart_health()
elif selected == "Mood Booster":
    mental_health_insights()
elif selected == "Gamification":
    game_fy()
elif selected == "Personalized Form":
    personalized_form()
elif selected == "About":
    about()