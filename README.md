# NutriFLEX.AI
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Instagram](https://img.shields.io/badge/Instagram-follow%20me%20on%20Instagram-pink.svg)](https://instagram.com/py_rex_47)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect%20with%20me-blue.svg)](https://www.linkedin.com/in/rahul-patil-4bb533209/)

NutriFLEX is an AI-powered nutrition assistant designed to offer personalized solutions in nutrition management. The app leverages advanced machine learning algorithms to predict calorie content, assist in meal planning, and recommend recipes tailored to individual health needs. Built on a Streamlit framework, NutriFLEX provides a user-friendly interface for ease of use and interaction.

## Key Features

- **BMR and TEE Calculation**: Calculate Basal Metabolic Rate (BMR) and Total Energy Expenditure (TEE) to guide users in creating personalized meal plans.
- **Calorie Prediction**: Predict the calorie content of various foods using machine learning models like Random Forest, XGBoost, Gradient Boosting, and CatBoost.
- **Recipe Recommendations**: Get traditional and AI-generated smart recipe suggestions based on nutritional goals and preferences.
- **Gamification**: Gamify the nutrition experience by rewarding healthy food choices, encouraging long-term engagement.
- **Health Goal Tracking**: Dynamically adjust meal suggestions as users progress toward their personalized health goals.
- **Mood-Based Meal Suggestions**: Tailor meal suggestions based on user moods and dietary preferences.
- **Integration with Wearables**: Future integration with wearable devices for real-time activity tracking and personalized recommendations.

## Gut Health Features

NutriFLEX provides specialized features for promoting gut health, ensuring that users maintain a balanced and healthy digestive system:

1. **Microbiome Data Inputs**: Users can provide information about their gut bacteria levels (e.g., Lactobacillus, Bifidobacterium, Firmicutes, Bacteroidetes, Akkermansia) and any presence of Clostridium difficile. This profile helps the AI to generate personalized dietary recommendations.

2. **Meal Plan Generation**: The AI generates a full-day meal plan—breakfast, lunch, dinner, and snacks—based on microbiome data, focusing on enhancing microbial diversity and increasing beneficial bacteria while reducing harmful ones.

3. **Gut-Friendly Recipes**: Users receive suggestions for recipes that are specifically designed to support gut health, incorporating ingredients known for their probiotic and prebiotic benefits.

4. **Integration with Mood-Based Suggestions**: The gut health feature also considers the user's mood when suggesting meals, promoting foods that can improve overall mental well-being and digestive health.

## Installation

To run the application, clone this repository and install the required packages:

```bash
git clone https://github.com/yourusername/NutriFLEX.git
cd NutriFLEX
pip install -r requirements.txt
```

## Usage

Run the app using:
```bash
streamlit run app.py
```

## Project Structure
```
NutriFLEX/
├── app.py                # Your main Streamlit application
├── requirements.txt      # Required Python packages
├── models/               # Directory for your machine learning models
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── gradient_boost.pkl
│   └── catboost.pkl
├── data/                 # Directory for your datasets
├── README.md             # Description of your project
└── NUTRIFLEX_REPORT_V2.pdf # Your project report
```
## Future Recommendations and Issues

### Future Recommendations

As the NutriFLEX project continues to evolve, the following enhancements and features are recommended:

1. **Enhanced Gamification**: 
   - Expand the reward system to include achievements, badges, and community-based competitions to further motivate users.

2. **Wearable Integration**:
   - Incorporate real-time data from fitness trackers and smartwatches to allow automatic adjustments of Total Energy Expenditure (TEE) calculations, providing users with more accurate meal planning.

3. **Voice Interface**:
   - Implement full integration of voice commands for hands-free operation, enhancing user interaction with the app.

4. **Expanded Recipe Database**:
   - Include more local and international recipes to diversify meal options, while also integrating with food delivery services to improve accessibility.

5. **Dietary Preferences and Allergies**:
   - Further refine meal plans and recipes based on dietary restrictions, such as gluten-free, vegan, or keto options, ensuring a more tailored experience for users.

6. **Gut Microbiome Analysis**:
   - Develop features that allow users to provide data on their gut bacteria levels for personalized dietary recommendations that support digestive health.

7. **Mood-Based Meal Suggestions**:
   - Continue to enhance the system for mood-based meal suggestions to offer more personalized and holistic nutrition management.

### Issues

While NutriFLEX has made significant strides in personalized nutrition management, there are some current issues and challenges to address:

1. **Model Performance**:
   - Initial evaluations indicate that model performance can vary. User testing with real-world data is essential for fine-tuning and ensuring reliable predictions.

2. **User Feedback Integration**:
   - Early user feedback has highlighted the need for more customizable meal plans and the importance of integrating the app with wearable devices. Addressing these concerns will enhance user satisfaction.

3. **Data Privacy and Security**:
   - As the app handles personal health information, ensuring data privacy and security is paramount. Implementing robust security measures will protect user data and build trust.

4. **Scalability**:
   - As the user base grows, ensuring the app can scale effectively will be crucial. This may involve optimizing performance and server capabilities.

5. **Accessibility Features**:
   - Improving accessibility features for users with disabilities will enhance inclusivity and user experience.

### Feedback and Contributions

We welcome contributions and feedback to improve NutriFLEX. If you have suggestions, ideas, or would like to report an issue, please fill out the [Feedback Form](https://forms.gle/WZPKEa87Kdg8WdX76) or open an issue in this repository.

---

MIT License

Copyright (c) 2024 Rahul Patil

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</br>

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</br>

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

