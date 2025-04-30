import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score
from xgboost import XGBRegressor, XGBClassifier

st.set_page_config(page_title="🌿 Hydroponics Growth Dashboard", layout="wide")

# -------------------- Load & Preprocess Data --------------------
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "hydroponics_system_dataset.csv")
    data = pd.read_csv(path)

    # Handle missing values
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = data.select_dtypes(include=['object']).columns

    data[numeric_cols] = SimpleImputer(strategy='median').fit_transform(data[numeric_cols])
    for col in categorical_cols:
        if col not in ['plant_id', 'timestamp']:
            data[col].fillna(data[col].mode()[0], inplace=True)

    # Create separate LabelEncoders
    le_plant = LabelEncoder()
    le_system = LabelEncoder()

    data['plant_type'] = le_plant.fit_transform(data['plant_type'])
    data['recommended_system'] = le_system.fit_transform(data['recommended_system'])

    plant_types = le_plant.classes_.tolist()

    # Convert boolean to int for classification
    data['is_failure'] = data['is_failure'].astype(int)

    return data, le_plant, le_system, plant_types

data, le_plant, le_system, plant_types = load_data()

# -------------------- Train Models --------------------
def train_regression_models(X, y):
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(random_state=42, n_estimators=100),
        'XGBoost': XGBRegressor(random_state=42)
    }
    trained_models = {}
    for name, model in models.items():
        model.fit(X, y)
        trained_models[name] = model
    return trained_models

def train_classification_models(X, y):
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'XGBoost': XGBClassifier(random_state=42)
    }
    trained_models = {}
    for name, model in models.items():
        model.fit(X, y)
        trained_models[name] = model
    return trained_models

# -------------------- Sidebar --------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Task", [
    "🌱 Growth Prediction",
    "💧 System Recommendation",
    "🥗 Nutrient Mix Recommender",
    "🌡️ Environmental Condition Optimizer",
    "🤝 Plant Compatibility Analyzer"
])

# -------------------- Growth Prediction --------------------
if page == "🌱 Growth Prediction":
    st.title("🌱 Predict Plant Growth Rate")
    
    with st.expander("ℹ️ About this tool"):
        st.write("""
        This tool predicts plant growth rate in hydroponic systems based on environmental parameters.
        The model uses multiple algorithms (XGBoost, Random Forest, etc.) trained on historical hydroponic growth data.
        """)

    with st.form("growth_form"):
        cols = st.columns(2)
        user_input = {
            'plant_type': cols[0].selectbox("Plant Type", plant_types),
            'temperature_c': cols[0].slider("Temperature (°C)", 10.0, 30.0, 22.0),
            'humidity_percent': cols[0].slider("Humidity (%)", 30.0, 90.0, 60.0),
            'ph_level': cols[0].slider("pH Level", 4.0, 8.0, 6.0),
            'ec_level': cols[0].slider("EC Level (mS/cm)", 0.5, 3.0, 1.6),
            'light_hours': cols[1].slider("Light Hours (per day)", 8, 20, 12),
            'co2_ppm': cols[1].slider("CO₂ Concentration (ppm)", 300, 1500, 800),
            'nitrogen_ppm': cols[1].slider("Nitrogen (ppm)", 50, 300, 150),
            'phosphorus_ppm': cols[1].slider("Phosphorus (ppm)", 30, 120, 50),
            'potassium_ppm': cols[1].slider("Potassium (ppm)", 100, 300, 200)
        }
        submitted = st.form_submit_button("Predict Growth")

    if submitted:
        try:
            # Create DataFrame
            input_df = pd.DataFrame([user_input])
            input_df['plant_type'] = le_plant.transform(input_df['plant_type'])
            
            # Get features
            features = [col for col in input_df.columns if col in data.columns]
            input_df = input_df[features]
            
            # Prepare training data
            X = data[features]
            y = data['growth_rate']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            input_scaled = scaler.transform(input_df)
            
            # Train models
            models = train_regression_models(X_train_scaled, y_train)
            
            # Predict and evaluate
            st.subheader("Prediction Results")
            model_comparison = []
            for name, model in models.items():
                predicted_growth = model.predict(input_scaled)[0]
                y_pred = model.predict(X_test_scaled)
                st.write(f"**{name}**")
                st.success(f"📈 Predicted Growth Rate: {predicted_growth:.2f} cm/day")
                col1, col2, col3 = st.columns(3)
                col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
                col2.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
                col3.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.3f}")
                
                model_comparison.append({
                    'Model': name,
                    'R²': r2_score(y_test, y_pred),
                    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'MAE': mean_absolute_error(y_test, y_pred),
                    'Prediction': predicted_growth
                })
            
            with st.expander("📊 Understanding Your Growth Prediction Results", expanded=True):
                st.write(f"""
                **Interpreting the Growth Prediction Results**
                
                1. **Growth Rate Predictions**:
                - The predicted growth rate indicates how fast your plant should grow under these conditions.
                - Compare this to typical growth rates for your plant type (leafy greens: 0.5-2cm/day, vines: 1-3cm/day).
                
                2. **Model Performance**:
                - R² Score: Higher values indicate better model fit.
                - RMSE/MAE: Lower values indicate more accurate predictions.
                
                3. **Optimization Recommendations**:
                - For high growth: Maintain 22-26°C, 14-18 hours light, and optimal NPK ratios.
                - If predictions are lower than expected, adjust parameters like temperature or nutrients.
                
                Monitor actual growth and adjust conditions as needed.
                """)
                
            # Final recommendation
            st.subheader("📊 Final Recommendation Based on Model Comparison")
            df_comparison = pd.DataFrame(model_comparison)
            st.dataframe(df_comparison.sort_values('R²', ascending=False))
            
            best_model = df_comparison.loc[df_comparison['R²'].idxmax()]
            st.success(f"""
            **Recommended Action**: 
            - Best performing model: {best_model['Model']} (R²: {best_model['R²']:.3f})
            - Trust the prediction from {best_model['Model']}: {best_model['Prediction']:.2f} cm/day
            - For robust decision-making, consider the average of top 2 models: {np.mean(df_comparison.nlargest(2, 'R²')['Prediction']):.2f} cm/day
            
            **Implementation Guidance**:
            1. If Random Forest or XGBoost is top performer, trust their robustness for complex data.
            2. If Linear Regression performs well, conditions are likely in optimal linear ranges.
            3. Large discrepancies between models suggest complex interactions - monitor closely.
            """)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# -------------------- System Recommendation --------------------
elif page == "💧 System Recommendation":
    st.title("💧 Recommend Hydroponic System")
    
    with st.expander("ℹ️ About this tool"):
        st.write("""
        This tool recommends the best hydroponic system for your plant based on environmental conditions.
        """)

    with st.form("system_form"):
        cols = st.columns(2)
        user_input = {
            'plant_type': cols[0].selectbox("Plant Type", plant_types),
            'temperature_c': cols[0].slider("Temperature (°C)", 10.0, 30.0, 20.0),
            'humidity_percent': cols[0].slider("Humidity (%)", 40.0, 90.0, 65.0),
            'ph_level': cols[0].slider("pH Level", 4.0, 8.0, 6.0),
            'ec_level': cols[1].slider("EC Level (mS/cm)", 0.5, 3.0, 1.5),
            'light_hours': cols[1].slider("Light Hours (per day)", 10, 20, 14),
            'co2_ppm': cols[1].slider("CO₂ Concentration (ppm)", 800, 1500, 1000)
        }
        submitted = st.form_submit_button("Recommend System")

    if submitted:
        try:
            input_df = pd.DataFrame([user_input])
            input_df['plant_type'] = le_plant.transform(input_df['plant_type'])
            
            features = [col for col in input_df.columns if col in data.columns]
            input_df = input_df[features]
            
            X = data[features]
            y = data['recommended_system']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            input_scaled = scaler.transform(input_df)
            
            models = train_regression_models(X_train_scaled, y_train)
            
            st.subheader("Recommendation Results")
            system_counts = {}
            model_details = []
            for name, model in models.items():
                predicted_system = le_system.inverse_transform([int(round(model.predict(input_scaled)[0]))])[0]
                system_counts[predicted_system] = system_counts.get(predicted_system, 0) + 1
                st.write(f"**{name}**")
                st.success(f"🧪 Recommended System: {predicted_system}")
                
                # Metrics
                y_pred = model.predict(X_test_scaled)
                col1, col2, col3 = st.columns(3)
                col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
                col2.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
                col3.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.3f}")
                
                model_details.append({
                    'Model': name,
                    'System': predicted_system,
                    'R²': r2_score(y_test, y_pred),
                    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'MAE': mean_absolute_error(y_test, y_pred)
                })
            
            with st.expander("🔍 Analyzing System Recommendations", expanded=True):
                st.write(f"""
                **Understanding the System Suitability Results**
                
                1. **Why These Systems Were Recommended**:
                - The systems scored based on:
                  * Plant type requirements
                  * Environmental conditions (temperature/humidity)
                  * Nutrient delivery needs
                - For your {user_input['plant_type']}, these systems balance:
                  * Oxygenation (critical for root health)
                  * Nutrient absorption efficiency
                  * Maintenance requirements
                
                2. **Implementation Tips**:
                - Monitor EC/pH daily when first transitioning systems.
                - Expect 1-2 week adaptation period for plants.
                - Adjust lighting to match the new system's water flow characteristics.
                """)
                
            # Final recommendation
            st.subheader("🛠️ Final System Selection Guidance")
            model_df = pd.DataFrame(model_details).sort_values('R²', ascending=False)
            st.write("**Model Performance Comparison**:")
            st.dataframe(model_df)
            
            st.write("**Model Agreement**:")
            for system, count in system_counts.items():
                st.write(f"- {system}: {count}/{len(models)} models recommend")
            
            recommended_system = max(system_counts, key=system_counts.get)
            confidence = system_counts[recommended_system] / len(models)
            
            if confidence > 0.75:
                confidence_level = "High"
                recommendation_icon = "✅"
            elif confidence > 0.5:
                confidence_level = "Moderate"
                recommendation_icon = "⚠️"
            else:
                confidence_level = "Low"
                recommendation_icon = "❓"
            
            st.success(f"""
            {recommendation_icon} **Recommended System**: {recommended_system}
            
            **Selection Rationale**:
            - **Consensus**: Chosen by {system_counts[recommended_system]}/{len(models)} models ({confidence_level} confidence)
            - **Performance**: Best average R² score of {model_df[model_df['System'] == recommended_system]['R²'].mean():.3f} for this system
            - **Accuracy**: Average error of ±{model_df[model_df['System'] == recommended_system]['MAE'].mean():.2f} system units
            
            **Implementation Guide**:
            1. **Setup Requirements**:
               - Prepare {recommended_system} equipment according to manufacturer specifications.
               - Calibrate sensors for pH, EC, and temperature monitoring.
            
            2. **Initial Parameters**:
               - Temperature: {user_input['temperature_c']}°C (adjust ±2°C based on plant response).
               - pH Level: Maintain {user_input['ph_level']} (±0.3).
               - Lighting: {user_input['light_hours']} hours daily.
            
            3. **Monitoring Protocol**:
               - Week 1: Check system parameters daily.
               - Week 2-4: Monitor every 3 days.
               - After stabilization: Weekly checks.
            
            **Troubleshooting Tips**:
            - If plant shows stress in first 7 days:
              - Verify EC levels match recommendation.
              - Check for proper oxygenation.
              - Ensure stable temperature (±1°C daily variation).
            
            **Alternative Options**:
            {', '.join([sys for sys in system_counts.keys() if sys != recommended_system]) or 'None strongly recommended'}
            """)
            
            if confidence <= 0.5:
                st.warning("""
                **Note**: Models show significant disagreement. Consider:
                - Running a small-scale test with top 2 recommended systems.
                - Adjusting environmental parameters toward middle ranges.
                - Consulting plant-specific hydroponic guides for {user_input['plant_type']}.
                """)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# -------------------- Nutrient Mix Recommender --------------------
elif page == "🥗 Nutrient Mix Recommender":
    st.title("🥗 Nutrient Mix Recommender")
    
    with st.expander("ℹ️ About this tool"):
        st.write("""
        This tool recommends optimal nutrient levels (Nitrogen, Phosphorus, Potassium) for your selected plant
        based on environmental conditions using multiple machine learning models.
        """)

    with st.form("env_form"):
        cols = st.columns(2)
        user_input = {
            'plant_type': cols[0].selectbox("Plant Type", plant_types),
            'nitrogen_ppm': cols[0].slider("Nitrogen (ppm)", 50, 300, 150),
            'phosphorus_ppm': cols[0].slider("Phosphorus (ppm)", 30, 120, 50),
            'potassium_ppm': cols[0].slider("Potassium (ppm)", 100, 300, 200)
        }
        submitted = st.form_submit_button("Recommend Conditions")

    if submitted:
        try:
            input_df = pd.DataFrame([user_input])
            input_df['plant_type'] = le_plant.transform(input_df['plant_type'])
            
            features = [col for col in input_df.columns if col in data.columns]
            targets = ['temperature_c', 'humidity_percent', 'ph_level', 'ec_level', 'light_hours', 'co2_ppm']
            
            X = data[features]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            input_scaled = scaler.transform(input_df)
            
            st.subheader("Recommended Environmental Conditions")
            env_results = {target: [] for target in targets}
            for target in targets:
                y = data[target]
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                models = train_regression_models(X_train, y_train)
                
                st.write(f"**{target.replace('_c', ' (°C)').replace('_percent', ' (%)').replace('_ppm', ' (ppm)')}:**")
                for name, model in models.items():
                    predicted_value = model.predict(input_scaled)[0]
                    st.write(f"- {name}: {predicted_value:.2f}")
                    
                    y_pred = model.predict(X_test)
                    col1, col2, col3 = st.columns(3)
                    col1.metric(f"R² Score ({name})", f"{r2_score(y_test, y_pred):.3f}")
                    col2.metric(f"RMSE ({name})", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
                    col3.metric(f"MAE ({name})", f"{mean_absolute_error(y_test, y_pred):.3f}")
                    
                    env_results[target].append({
                        'Model': name,
                        'R²': r2_score(y_test, y_pred),
                        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
                        'MAE': mean_absolute_error(y_test, y_pred),
                        'Prediction': predicted_value
                    })
            
            with st.expander("🌡️ Understanding Environmental Recommendations", expanded=True):
                st.write("""
                **Interpreting the Environmental Condition Results**
                
                1. **Environmental Conditions**:
                - The predicted values are optimal settings for temperature, humidity, pH, EC, light hours, and CO₂.
                - These are tailored to the nutrient levels and plant type provided.
                
                2. **Model Performance**:
                - R² Score: Higher values indicate better model fit.
                - RMSE/MAE: Lower values indicate more accurate predictions.
                
                3. **Optimization Tips**:
                - Adjust your hydroponic system to match these settings.
                - Maintain stable conditions to avoid plant stress.
                - Consider averaging predictions if models vary.
                
                Calibrate sensors regularly for accurate control.
                """)
                
            # Final recommendation
            st.subheader("🌡️ Recommended Nutrient Levels")
            for target in targets:
                df_comparison = pd.DataFrame(env_results[target])
                st.write(f"**{target.replace('_c', ' (°C)').replace('_percent', ' (%)').replace('_ppm', ' (ppm)')}:**")
                st.dataframe(df_comparison.sort_values('R²', ascending=False))
                
                best_model = df_comparison.loc[df_comparison['R²'].idxmax()]
                unit = '°C' if target == 'temperature_c' else '%' if target == 'humidity_percent' else 'ppm' if target == 'co2_ppm' else 'hours' if target == 'light_hours' else ''
                st.success(f"""
                **Recommended {target.replace('_c', '').replace('_percent', '').replace('_ppm', '')} Level**:
                - Best performing model: {best_model['Model']} (R²: {best_model['R²']:.3f})
                - Recommended level: {best_model['Prediction']:.2f} {unit}
                - For robust decision-making, consider the average of top 2 models: {np.mean(df_comparison.nlargest(2, 'R²')['Prediction']):.2f} {unit}
                
                **Implementation Guidance**:
                1. Adjust system to maintain {best_model['Prediction']:.2f} {unit} for {target.replace('_c', '').replace('_percent', '').replace('_ppm', '')}.
                2. Calibrate sensors to ensure stability (e.g., ±1°C for temperature, ±5% for humidity, ±100 ppm for CO₂).
                3. If Random Forest or XGBoost is the top performer, trust their robustness for complex environmental interactions.
                4. Monitor plants for stress (e.g., wilting, leaf curl) for 1-2 weeks after adjustments.
                5. If predictions vary, use the average and fine-tune based on observed plant health.
                """)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    

# -------------------- Environmental Condition Optimizer --------------------
elif page == "🌡️ Environmental Condition Optimizer":
    st.title("🌡️ Environmental Condition Optimizer")
    
    with st.expander("ℹ️ About this tool"):
        st.write("""
        This tool recommends optimal environmental conditions (Temperature, Humidity, pH, EC, Light Hours, CO₂)
        for your selected plant based on nutrient levels using multiple machine learning models.
        """)
    
    with st.form("nutrient_form"):
        cols = st.columns(2)
        user_input = {
            'plant_type': cols[0].selectbox("Plant Type", plant_types),
            'temperature_c': cols[0].slider("Temperature (°C)", 10.0, 30.0, 20.0),
            'humidity_percent': cols[0].slider("Humidity (%)", 40.0, 90.0, 65.0),
            'ph_level': cols[0].slider("pH Level", 4.0, 8.0, 6.0),
            'ec_level': cols[0].slider("EC Level (mS/cm)", 0.5, 3.0, 1.7),
            'light_hours': cols[1].slider("Light Hours (per day)", 8, 20, 16),
            'co2_ppm': cols[1].slider("CO₂ Concentration (ppm)", 500, 1500, 1000)
        }
        submitted = st.form_submit_button("Recommend Nutrients")

    if submitted:
        try:
            input_df = pd.DataFrame([user_input])
            input_df['plant_type'] = le_plant.transform(input_df['plant_type'])
            
            features = [col for col in input_df.columns if col in data.columns]
            targets = ['nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm']
            
            X = data[features]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            input_scaled = scaler.transform(input_df)
            
            st.subheader("Recommended Nutrient Levels")
            nutrient_results = {target: [] for target in targets}
            for target in targets:
                y = data[target]
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                models = train_regression_models(X_train, y_train)
                
                st.write(f"**{target.replace('_ppm', ' (ppm)')}:**")
                for name, model in models.items():
                    predicted_value = model.predict(input_scaled)[0]
                    st.write(f"- {name}: {predicted_value:.2f} ppm")
                    
                    y_pred = model.predict(X_test)
                    col1, col2, col3 = st.columns(3)
                    col1.metric(f"R² Score ({name})", f"{r2_score(y_test, y_pred):.3f}")
                    col2.metric(f"RMSE ({name})", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")
                    col3.metric(f"MAE ({name})", f"{mean_absolute_error(y_test, y_pred):.3f}")
                    
                    nutrient_results[target].append({
                        'Model': name,
                        'R²': r2_score(y_test, y_pred),
                        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
                        'MAE': mean_absolute_error(y_test, y_pred),
                        'Prediction': predicted_value
                    })
            
            with st.expander("🌡️ Understanding Environmental Recommendations", expanded=True):
                st.write("""
                **Interpreting the Nutrient Recommendation Results**
                
                1. **Nutrient Levels**:
                - The predicted values for Nitrogen, Phosphorus, and Potassium (NPK) represent the optimal concentrations (in ppm).
                - These are tailored to your plant type and environmental conditions.
                
                2. **Model Performance**:
                - R² Score: Higher values indicate better model fit.
                - RMSE/MAE: Lower values indicate more accurate predictions.
                
                3. **Optimization Tips**:
                - Adjust nutrient solutions to match the recommended NPK levels.
                - Monitor pH and EC closely for nutrient absorption.
                - Consider averaging predictions if models vary significantly.
                
                Check nutrient levels weekly to maintain optimal growth.
                """)
                
            # Final recommendation
            st.subheader("🌡️ Final Environmental Condition Recommendation")
            for target in targets:
                df_comparison = pd.DataFrame(nutrient_results[target])
                st.write(f"**{target.replace('_ppm', ' (ppm)')}:**")
                st.dataframe(df_comparison.sort_values('R²', ascending=False))
                
                best_model = df_comparison.loc[df_comparison['R²'].idxmax()]
                st.success(f"""
                **Recommended {target.replace('_ppm', '')} Level**:
                - Best performing model: {best_model['Model']} (R²: {best_model['R²']:.3f})
                - Recommended level: {best_model['Prediction']:.2f} ppm
                - For robust decision-making, consider the average of top 2 models: {np.mean(df_comparison.nlargest(2, 'R²')['Prediction']):.2f} ppm
                
                **Implementation Guidance**:
                1. Prepare nutrient solution to achieve {best_model['Prediction']:.2f} ppm for {target.replace('_ppm', '')}.
                2. Monitor EC ({user_input['ec_level']} ± 0.2 mS/cm) and pH ({user_input['ph_level']} ± 0.3) daily to ensure nutrient uptake.
                3. If Random Forest or XGBoost is the top performer, trust their robustness for complex nutrient interactions.
                4. Observe plant health weekly for signs of nutrient deficiency (e.g., yellowing leaves) or toxicity (e.g., leaf burn).
                5. If model predictions vary, start with the average and adjust based on plant response after 1-2 weeks.
                """)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    

# -------------------- Plant Compatibility Analyzer --------------------
elif page == "🤝 Plant Compatibility Analyzer":
    st.title("🤝 Plant Compatibility Analyzer")
    
    with st.expander("ℹ️ About this tool"):
        st.write("""
        This tool analyzes whether selected plants can be grown together based on their environmental
        and nutrient requirements using classification models. It predicts the likelihood of failure for each plant.
        """)

    with st.form("compatibility_form"):
        selected_plants = st.multiselect("Select Plants to Check Compatibility", plant_types)
        submitted = st.form_submit_button("Analyze Compatibility")

    if submitted:
        if len(selected_plants) < 2:
            st.warning("Please select at least two plants to analyze compatibility.")
        else:
            try:
                features = ['temperature_c', 'humidity_percent', 'ph_level', 'ec_level',
                           'light_hours', 'co2_ppm', 'nitrogen_ppm', 'phosphorus_ppm',
                           'potassium_ppm', 'plant_type']
                X = data[features]
                y = data['is_failure']
                
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                
                models = train_classification_models(X_train, y_train)
                
                st.subheader("Compatibility Analysis")
                compatibility_results = []
                for plant in selected_plants:
                    plant_id = le_plant.transform([plant])[0]
                    plant_data = data[data['plant_type'] == plant_id][features]
                    avg_conditions = plant_data.mean().values
                    input_scaled = scaler.transform([avg_conditions])
                    
                    predictions = {}
                    for name, model in models.items():
                        pred = model.predict(input_scaled)[0]
                        predictions[name] = pred
                    
                    compatibility_results.append((plant, predictions))
                    
                    st.write(f"**{plant}:**")
                    for name, pred in predictions.items():
                        status = "Compatible (Low Failure Risk)" if pred == 0 else "Incompatible (High Failure Risk)"
                        st.write(f"- {name}: {status}")
                        
                        y_pred = models[name].predict(X_test)
                        col1, col2 = st.columns(2)
                        col1.metric(f"Accuracy ({name})", f"{accuracy_score(y_test, y_pred):.3f}")
                
                st.subheader("Recommendation")
                failure_risks = [sum(preds.values()) for _, preds in compatibility_results]
                if sum(failure_risks) == 0:
                    st.success(f"The selected plants ({', '.join(selected_plants)}) are likely compatible.")
                    st.write("""
                    **Final Recommendation**: These plants can be grown together safely. Monitor for:
                    - Consistent growth rates across all plants.
                    - No signs of nutrient deficiencies.
                    - Balanced resource consumption.
                    """)
                else:
                    incompatible_plants = [plant for plant, preds in compatibility_results if sum(preds.values()) > 0]
                    st.warning(f"Potential incompatibility detected with: {', '.join(incompatible_plants)}")
                    st.write("""
                    **Final Recommendation**: Consider these adjustments:
                    - Separate incompatible plants into different systems.
                    - Find compromise conditions that work for all plants.
                    - Prioritize plants with similar requirements.
                    - Monitor closely for signs of stress.
                    """)
                
                with st.expander("🤝 Understanding Compatibility Analysis", expanded=True):
                    st.write("""
                    **Interpreting the Compatibility Results**
                    
                    1. **Compatibility Predictions**:
                    - Each plant is evaluated for failure risk based on average conditions.
                    - "Low Failure Risk" indicates thriving under shared conditions.
                    - "High Failure Risk" suggests issues with nutrient or environmental needs.
                    
                    2. **Model Performance**:
                    - Accuracy: Higher values indicate reliable predictions.
                    
                    3. **Optimization Tips**:
                    - Focus on plants with similar requirements (e.g., leafy greens).
                    - Adjust conditions to align with all plants' needs.
                    - Separate incompatible plants if needed.
                    
                    Monitor plant health to detect stress or incompatibility early.
                    """)
                    
                # Final recommendation
                st.subheader("🤝 Final Compatibility Recommendation")
                model_comparison = []
                for plant, predictions in compatibility_results:
                    for name, pred in predictions.items():
                        y_pred = models[name].predict(X_test)
                        status = 0 if pred == 0 else 1
                        model_comparison.append({
                            'Plant': plant,
                            'Model': name,
                            'Accuracy': accuracy_score(y_test, y_pred),
                            'Prediction': 'Compatible' if status == 0 else 'Incompatible'
                        })
                
                df_comparison = pd.DataFrame(model_comparison)
                st.dataframe(df_comparison.sort_values('Accuracy', ascending=False))
                
                compatible_plants = [plant for plant, preds in compatibility_results if sum(preds.values()) == 0]
                if len(compatible_plants) == len(selected_plants):
                    st.success(f"""
                    **Recommended Action**:
                    - All selected plants ({', '.join(selected_plants)}) are predicted compatible by most models.
                    - Best performing model: {df_comparison.loc[df_comparison['Accuracy'].idxmax()]['Model']} (Accuracy: {df_comparison['Accuracy'].max():.3f})
                    
                    **Implementation Guidance**:
                    1. Grow these plants together in the same system.
                    2. Monitor for uniform growth and nutrient uptake.
                    3. If using Random Forest or XGBoost, trust their robust predictions.
                    """)
                else:
                    best_model = df_comparison.loc[df_comparison['Accuracy'].idxmax()]
                    incompatible_plants = [plant for plant, preds in compatibility_results if sum(preds.values()) > 0]
                    st.warning(f"""
                    **Recommended Action**:
                    - Incompatible plants detected: {', '.join(incompatible_plants)}
                    - Best performing model: {best_model['Model']} (Accuracy: {best_model['Accuracy']:.3f})
                    - Consider separating incompatible plants or adjusting conditions.
                    
                    **Implementation Guidance**:
                    1. Prioritize compatible plants: {', '.join(compatible_plants) if compatible_plants else 'None'}.
                    2. If Random Forest or XGBoost is top performer, trust their robustness.
                    3. Monitor incompatible plants closely for stress signs.
                    """)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
