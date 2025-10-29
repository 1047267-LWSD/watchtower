import pickle as pkl
import numpy as np
import pandas as pd
import shap
import os

# Resolve project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Saved model paths
model_path = os.path.join(project_root, 'saved-models', 'spam-detector.pkl')
categorizer_path = os.path.join(project_root, 'saved-models', 'spam-categorizer.pkl')
detector_vectorizer_path = os.path.join(project_root, 'saved-models', 'detector-vectorizer.pkl')
categorizer_vectorizer_path = os.path.join(project_root, 'saved-models', 'categorizer-vectorizer.pkl')

# Load models + vectorizers
with open(model_path, 'rb') as f:
    spam_model = pkl.load(f)
with open(detector_vectorizer_path, 'rb') as f:
    spam_vec = pkl.load(f)
with open(categorizer_path, 'rb') as f:
    cat_model = pkl.load(f)
with open(categorizer_vectorizer_path, 'rb') as f:
    cat_vec = pkl.load(f)

# SHAP background setup
dataset_path = os.path.join(project_root, "datasets", "hamspam.csv")

if os.path.exists(dataset_path):
    background = pd.read_csv(
        dataset_path,
        encoding="latin-1",
        on_bad_lines="skip"
    )["v2"]
    background = background.dropna()
    background = background[background != ""]
    background = background.astype(str)
else:
    background = [
        "hello",
        "thank you",
        "information",
        "good day",
        "meeting",
        "yes",
        "no",
        "okay"
    ]

# Limit rows → faster + avoids Render memory/timeouts
background_vec = spam_vec.transform(background[:200])
explainer = shap.LinearExplainer(spam_model, background_vec)

def spam_detect(text):
    result = {}
    text_in_array = [text]
    result['text'] = text

    # Vectorize
    vec_text = spam_vec.transform(text_in_array)

    # Prediction
    prediction = spam_model.predict(vec_text)[0]
    result['prediction'] = prediction

    # Confidence
    spam_prob = spam_model.predict_proba(vec_text)[0][list(spam_model.classes_).index(prediction)]
    result['confidence'] = float(spam_prob)

    # SHAP word contributions
    shap_values = explainer.shap_values(vec_text)
    words = spam_vec.get_feature_names_out()
    feature_indices = vec_text.nonzero()[1]
    result['word_contributions'] = {words[idx]: float(shap_values[0][idx]) for idx in feature_indices}

    # Spam type classification if needed
    if prediction == "spam":
        vec_cat = cat_vec.transform(text_in_array)
        cat_pred = cat_model.predict(vec_cat)[0]
        result["spam_type"] = cat_pred
    else:
        result["spam_type"] = "not spam"

    return result
