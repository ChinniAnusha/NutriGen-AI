import streamlit as st
import requests
import json

# ----------- CONFIG -------------
st.set_page_config(page_title="NutriGen AI", layout="wide")

API_KEY = st.secrets["GEMINI_API_KEY"]

st.sidebar.title("NutriGen AI 🥗")
page = st.sidebar.radio("Navigate", [
    "Home",
    "Meal Planner",
    "Nutrition Analyzer",
    "Virtual Coach" 
])

MODEL_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key="

# ----------- FUNCTION TO CALL GEMINI -------------
def generate_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(MODEL_URL + API_KEY, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.json()}"

# ----------- HOME -------------
if page == "Home":
    st.title("NutriGen AI 🍎")
    st.write("Advancing Nutrition Science through GeminiAI")
    st.write("Your Personal AI Nutrition Assistant")

# ----------- MEAL PLANNER -------------
elif page == "Meal Planner":
    st.title("Personalized Meal Planner")

    goal = st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
    restrictions = st.text_input("Dietary Restrictions (e.g., vegetarian, keto)")
    allergies = st.text_input("Allergies")
    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

    if st.button("Generate Meal Plan"):
        prompt = f"""
        Create a 7-day meal plan for:
        Goal: {goal}
        Dietary restrictions: {restrictions}
        Allergies: {allergies}
        Activity Level: {activity}

        Include:
        - Breakfast, Lunch, Dinner
        - Calories per meal
        - Grocery list at the end
        """
        output = generate_response(prompt)
        st.write(output)

# ----------- NUTRITION ANALYZER -------------
elif page == "Nutrition Analyzer":
    st.title("Food Nutrition Analyzer")

    food = st.text_area("Enter food items")

    if st.button("Analyze"):
        prompt = f"""
        Analyze the following food items: {food}

        Return ONLY valid JSON in this format:

        {{
            "calories": number,
            "protein_g": number,
            "carbs_g": number,
            "fat_g": number,
            "vitamins": ["list of key vitamins"],
            "minerals": ["list of key minerals"],
            "health_rating": number (1-10),
            "summary": "short health summary"
        }}
        """

        output = generate_response(prompt)
        
        import re

        try:
            # Remove markdown code blocks if present
            cleaned_output = re.sub(r"```json|```", "", output).strip()

            data = json.loads(cleaned_output)

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Calories", f"{data['calories']} kcal")
            col2.metric("Protein", f"{data['protein_g']} g")
            col3.metric("Carbs", f"{data['carbs_g']} g")
            col4.metric("Fat", f"{data['fat_g']} g")

            st.subheader("Vitamins")
            st.write(", ".join(data["vitamins"]))

            st.subheader("Minerals")
            st.write(", ".join(data["minerals"]))

            st.subheader("Health Rating")
            st.progress(data["health_rating"] / 10)

            st.subheader("Summary")
            st.write(data["summary"])

        except Exception as e:
            st.error("JSON parsing failed. Showing raw output:")
            st.write(output)
        

     

# ----------- VIRTUAL COACH -------------
elif page == "Virtual Coach":
    st.title("Virtual Nutrition Coach")

    user_question = st.text_area("Ask your nutrition question")

    if st.button("Ask Coach"):
        prompt = f"You are a professional certified nutritionist. Answer clearly and practically: {user_question}"
        output = generate_response(prompt)
        st.write(output)