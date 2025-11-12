import streamlit as st
import pandas as pd
import time # Utile pour simuler un temps de chargement

# --- Configuration de la Page et Titre ---
st.set_page_config(
    page_title="Prédiction Cardiovasculaire",
    layout="wide" # Utilise la largeur maximale de l'écran
)

st.image("730181fc-ea6a-4bb0-a0dd-9ac0f187ba12-1-1.jpeg", width=150)
st.title("🩺 Outil de Prédiction des Maladies Cardiovasculaires")


introduction_text = "Les maladies cardiovasculaires (MCV) représentent aujourd’hui la première cause de mortalité dans le monde, avec près de 17,9 millions de décès chaque année, soit environ 31 % de l’ensemble des décès globaux. Ces affections regroupent un ensemble de troubles touchant le cœur et les vaisseaux sanguins, parmi lesquels figurent les crises cardiaques, les accidents vasculaires cérébraux (AVC) et l’insuffisance cardiaque. Alourdis par des facteurs de risque comme l’hypertension, le tabagisme, le diabète ou encore le cholestérol élevé, ces troubles peuvent conduire à des décès prématurés, notamment chez les personnes de moins de 70 ans"

st.markdown(
    f"""
    <div style="color: #19e5e6; font-size: 16px; margin-bottom: 20px;">
        {introduction_text}
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
st.write("Veuillez saisir les paramètres du patient pour le diagnostic.")


# --- 1. Initialisation du Session State pour le stockage des données ---
if 'submissions' not in st.session_state:
    # Cette liste stockera un dictionnaire pour chaque soumission de formulaire
    st.session_state.submissions = []
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None

# --- Configuration des options catégorielles pour une meilleure ergonomie ---
SEX_OPTIONS = {0: "Femme (0)", 1: "Homme (1)"}
FASTINGBS_OPTIONS = {0: "Non (< 120 mg/dl)", 1: "Oui (≥ 120 mg/dl)"}
EXERCISEANGINA_OPTIONS = {0: "Non (0)", 1: "Oui (1)"}

CHEST_PAIN_OPTIONS = {
    0: "0 - Douleur Angineuse Typique (TA)",
    1: "1 - Douleur Angineuse Atypique (ATA)",
    2: "2 - Douleur Non-Angineuse (NAP)",
    3: "3 - Asymptomatique (ASY)"
}

ECG_OPTIONS = {
    0: "0 - Normal",
    1: "1 - Anormalité de l'onde ST-T",
    2: "2 - Hypertrophie Ventriculaire Gauche"
}

ST_SLOPE_OPTIONS = {
    0: "0 - Pente Ascendante (Up)",
    1: "1 - Plat (Flat)",
    2: "2 - Pente Descendante (Down)"
}

# --- 2. Interface Utilisateur et Formulaire ---

# --- Démarrer le Formulaire ---
with st.form(key='prediction_form'):
    st.header("Saisie des données du patient")

    col1, col2, col3 = st.columns(3)

    # Ligne 1 : Variables de base
    with col1:
        Age = st.number_input('Age', min_value=18, max_value=120, value=50, step=1)
        FastingBS = st.radio('FastingBS (> 120 mg/dl)', options=list(FASTINGBS_OPTIONS.keys()), format_func=lambda x: FASTINGBS_OPTIONS[x])
    
    with col2:
        Sex = st.radio('Sex', options=list(SEX_OPTIONS.keys()), format_func=lambda x: SEX_OPTIONS[x])
        RestingECG = st.selectbox('RestingECG', options=list(ECG_OPTIONS.keys()), format_func=lambda x: ECG_OPTIONS[x])

    with col3:
        RestingBP = st.number_input('RestingBP (mmHg)', min_value=80, max_value=200, value=120, step=5)
        MaxHR = st.number_input('MaxHR', min_value=60, max_value=220, value=150, step=1)
        
    st.markdown("---")
    
    # Ligne 2 : Douleur et Cholestérol
    col4, col5 = st.columns(2)
    
    with col4:
        ChestPainType = st.selectbox('ChestPainType', options=list(CHEST_PAIN_OPTIONS.keys()), format_func=lambda x: CHEST_PAIN_OPTIONS[x])
        Oldpeak = st.number_input('Oldpeak', min_value=0.0, max_value=6.2, value=1.0, step=0.1)

    with col5:
        Cholesterol = st.number_input('Cholesterol (mg/dl)', min_value=0, max_value=600, value=200, step=5)
        ExerciseAngina = st.radio('ExerciseAngina', options=list(EXERCISEANGINA_OPTIONS.keys()), format_func=lambda x: EXERCISEANGINA_OPTIONS[x])

    # Ligne 3 : Pente ST
    ST_Slope = st.selectbox('ST_Slope', options=list(ST_SLOPE_OPTIONS.keys()), format_func=lambda x: ST_SLOPE_OPTIONS[x])
    
    # Bouton de soumission
    submit_button = st.form_submit_button(label='Faire la Prédiction')

# --- 3. Traitement après soumission ---
if submit_button:
    # Affiche un message de chargement
    with st.spinner('Analyse des données et exécution du modèle...'):
        #time.sleep(2) # Ligne à décommenter pour simuler un temps de chargement

        # 3.1. Collecte des données
        input_data = {
            'Age': Age, 'Sex': Sex, 'ChestPainType': ChestPainType, 'RestingBP': RestingBP,
            'Cholesterol': Cholesterol, 'FastingBS': FastingBS, 'RestingECG': RestingECG,
            'MaxHR': MaxHR, 'ExerciseAngina': ExerciseAngina, 'Oldpeak': Oldpeak,
            'ST_Slope': ST_Slope,
        }
        
        # 3.2. Intégration du Modèle (Exemple de Simulation)
        # REMPLACEZ TOUT CE BLOC PAR VOTRE CODE DE CHARGEMENT ET D'APPEL DU MODÈLE DE ML
        if Age > 60 and Cholesterol > 240 and FastingBS == 1:
             resultat_prediction = 1 # Risque élevé
        elif ChestPainType == 3 and MaxHR < 100:
             resultat_prediction = 1 # Risque élevé
        else:
             resultat_prediction = 0 # Faible risque
             
        # Stocke le résultat pour l'affichage immédiat
        st.session_state.last_prediction = resultat_prediction
        
        # 3.3. Stockage des données soumises et du résultat dans le session state
        submission_record = input_data.copy()
        submission_record['Prediction'] = resultat_prediction
        submission_record['Timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.submissions.append(submission_record)
        
        # Efface la barre de chargement
        st.success("Prédiction terminée.")


# --- 4. Affichage des Résultats et Historique ---

if st.session_state.last_prediction is not None:
    st.markdown("---")
    st.header("Résultat de la Prédiction")

    if st.session_state.last_prediction == 1:
        st.error("💔 **RISQUE ÉLEVÉ DE MALADIE CARDIAQUE (1)** : Une évaluation médicale est fortement recommandée.")
    else:
        st.success("✅ **FAIBLE RISQUE DE MALADIE CARDIAQUE (0)** : Les indicateurs actuels sont favorables.")
        st.balloons()

st.markdown("---")
st.header("Historique des Soumissions de Session")

if st.session_state.submissions:
    # Crée un DataFrame pour une belle visualisation
    df_submissions = pd.DataFrame(st.session_state.submissions)
    
    # Affichage des 10 dernières soumissions
    st.dataframe(df_submissions.tail(10))
    
    # Bouton pour télécharger les données
    csv_data = df_submissions.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger toutes les données de session (CSV)",
        data=csv_data,
        file_name='historique_predictions_session.csv',
        mime='text/csv',
    )
else:
    st.info("Aucune donnée n'a encore été soumise dans cette session. L'historique des soumissions apparaît ici après la première prédiction.")
