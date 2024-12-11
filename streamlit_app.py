import streamlit as st 
import pandas as pd
import joblib
import json 


st.title("Classifiers pets")
st.write("Clasificador de mascotas. Introduzca los datos de su mascota y le diremos a que clase pertenece.")
st.image("img/gato.webp")
# Cargar el modelo entrenado y las asignaciones para el color de ojos y el largo del pelo . 
modelo = joblib.load("model/pets_model.joblib")
with open("model/category_mapping.json") as f:
    category_mapping = json.load(f)

# Extraer los valores categoricos. 

eye_color_values = category_mapping["eye_color"]
fur_length_values = category_mapping["fur_length"]

# Crear los elementos para la entrada de datos.
st.write("Introduzca los datos de su mascota")
weight = st.number_input("Peso (Kg)", min_value=0.0, max_value=10.0, value=10.0)
height = st.number_input("Altura (cm)", min_value=10.0, max_value=200.0, value=10.0)
eye_color = st.selectbox("Color de ojos", ["Azul", "Marrón", "Gris", "Verde", ])
fur_length = st.selectbox("Largo del pelo", ["Largo", "Medio", "Corto"])

# Mapeo de la selección de color de ojos y largo del pelo al español 

eye_color_map = {"Azul": "blue", "Marrón": "brown", "Gris": "gray", "Verde": "green"}
fur_length_map = {"Largo": "long", "Medio": "medium", "Corto": "short"}

selected_eye_color = eye_color_map[eye_color]
selected_fur_length = fur_length_map[fur_length]

# Generar las columans binarias para eye_color y fur_length.
eye_color_binary = [(color == selected_eye_color) for color in eye_color_values]
fur_length_binary = [(length == selected_fur_length) for length in fur_length_values]

# Crear un DataFrame con los datos de la mascota.
input_data = [weight, height] + eye_color_binary + fur_length_binary
columnas = columns=["weight_kg", "height_cm"] + [f"eye_color_{color}" for color in eye_color_values] + [f"fur_length_{length}" for length in fur_length_values]
input_df = pd.DataFrame([input_data], columns=columnas)


# Realizar la predicción. 
if st.button("Predecir"):
    prediccion = modelo.predict(input_df)[0]
    prediction_map = {"dog": "Perro", "cat": "Gato", "rabbit": "Conejo"}
    st.success(f'La mascota es un {prediction_map[prediccion]} ', icon="✅")
    st.balloons()
