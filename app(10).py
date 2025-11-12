
st.title("Prédiction des maladies cardiovasculaires")
st.write("Veuillez saisir les paramètres du patient pour la prédiction.")
st.markdown("---") 

# Démarrer le Formulaire
# Utiliser st.form garantit que la prédiction ne se lance qu'après le clic sur le bouton
with st.form(key='prediction_form'):
    st.header("Saisie des données du patient")

    # Utilisation de colonnes pour une mise en page plus compacte
    col1, col2, col3 = st.columns(3)

    # Ligne 1 : Variables de base (Age, Sex, RestingBP)
    with col1:
        # Age (Numérique, valeur par défaut 50)
        Age = st.number_input('Age', min_value=18, max_value=120, value=50, step=1)
        
        # FastingBS (Booléen/Catégoriel binaire)
        FastingBS = st.radio(
            'FastingBS (> 120 mg/dl)', 
            (0, 1), 
            format_func=lambda x: 'Oui (1)' if x == 1 else 'Non (0)'
        )
    
    with col2:
        # Sex (Catégoriel binaire)
        Sex = st.radio('Sex', (0, 1), format_func=lambda x: 'Homme (1)' if x == 1 else 'Femme (0)')
        
        # RestingECG (Catégoriel)
        RestingECG = st.selectbox(
            'RestingECG', 
            options=[0, 1, 2],
            format_func=lambda x: f"Valeur {x}" # Adaptez ici si vous avez les significations (Normal, ST-T, Hypertrophie)
        )

    with col3:
        # RestingBP (Tension artérielle au repos)
        RestingBP = st.number_input('RestingBP (mmHg)', min_value=80, max_value=200, value=120, step=5)
        
        # MaxHR (Fréquence cardiaque maximale)
        MaxHR = st.number_input('MaxHR', min_value=60, max_value=220, value=150, step=1)
        
    st.markdown("---")
    
    # Ligne 2 : Variables de type douleur et angine
    col4, col5 = st.columns(2)
    
    with col4:
        # ChestPainType (Catégoriel)
        ChestPainType = st.selectbox(
            'ChestPainType', 
            options=[0, 1, 2, 3], # Les options réelles dépendent de votre encodage (ex: TA, ASY, NAP, etc.)
            format_func=lambda x: f"Type {x}" # À modifier si vous connaissez la signification de 0, 1, 2, 3
        )
        
        # Oldpeak (Numérique/Float)
        # Note : st.number_input accepte les floats si 'step' est un float
        Oldpeak = st.number_input('Oldpeak', min_value=0.0, max_value=6.2, value=1.0, step=0.1)

    with col5:
        # Cholesterol (Numérique)
        Cholesterol = st.number_input('Cholesterol (mg/dl)', min_value=0, max_value=600, value=200, step=5)
        
        # ExerciseAngina (Catégoriel binaire)
        ExerciseAngina = st.radio(
            'ExerciseAngina', 
            (0, 1), 
            format_func=lambda x: 'Oui (1)' if x == 1 else 'Non (0)'
        )

    # Ligne 3 : Variables finales
    ST_Slope = st.selectbox(
        'ST_Slope', 
        options=[0, 1, 2],
        format_func=lambda x: f"Pente {x}" # À modifier si vous avez les significations (Up, Flat, Down)
    )
    
    # Le bouton de soumission DOIT être le dernier élément du bloc with st.form
    submit_button = st.form_submit_button(label='Faire la Prédiction')

# --- Traitement après soumission ---
if submit_button:
    st.success("Données saisies. Calcul de la prédiction...")
    
    # Créez un dictionnaire ou un tableau NumPy/Pandas pour votre modèle
    input_data = {
        'Age': Age,
        'Sex': Sex,
        'ChestPainType': ChestPainType,
        'RestingBP': RestingBP,
        'Cholesterol': Cholesterol,
        'FastingBS': FastingBS,
        'RestingECG': RestingECG,
        'MaxHR': MaxHR,
        'ExerciseAngina': ExerciseAngina,
        'Oldpeak': Oldpeak,
        'ST_Slope': ST_Slope,
        # 'HeartDisease' est la variable cible (output), elle n'est pas saisie
    }
    
    # --- Intégration de votre modèle ---
    # Ici, vous chargerez votre modèle et passerez 'input_data' pour obtenir la prédiction.
    # Exemple: prediction = mon_modele.predict(pd.DataFrame([input_data]))
    
    # Affichage des résultats (Exemple)
    st.subheader("Résultat de la prédiction (Exemple)")
    
    # Simuler le résultat (0 ou 1)
    resultat_prediction = 1 # Remplacez ceci par le résultat de votre modèle
    
    if resultat_prediction == 1:
        st.error("💔 **Risque Élevé de Maladie Cardiaque (1)** : Une évaluation médicale est recommandée.")
    else:
        st.balloons()
        st.success("✅ **Faible Risque de Maladie Cardiaque (0)** : Les indicateurs sont favorables.")
