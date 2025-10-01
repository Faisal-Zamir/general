import pandas as pd
import joblib
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

# Load model and scaler
model = joblib.load(os.path.join(BASE_DIR, "titanic_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

data_dict = {
    'Pclass': 3,
    'Age': 18,
    'SibSp': 1,
    'Parch': 0,
    'Fare': 200.25,
    'HasCabin': 0,
    'Sex_mapped': 1,   # 1 = male, 0 = female (example)
    'FamilySize': 1,
    'IsAlone': 0,
    'Title_Miss': 1,
    'Title_Mr': 0,
    'Title_Mrs': 0,
    'Title_Rare': 0,
    'Embarked_C': 0,
    'Embarked_Q': 0,
    'Embarked_S': 1,
    'CabinDeck_A': 1,
    'CabinDeck_B': 0,
    'CabinDeck_C': 0,
    'CabinDeck_D': 0,
    'CabinDeck_E': 0,
    'CabinDeck_F': 0,
    'CabinDeck_G': 0,
    'CabinDeck_T': 0,
    'CabinDeck_Unknown': 0
}

def predict_passenger(data_dict):
    print("Input data_dict:", data_dict)
    X_new = pd.DataFrame([data_dict])
    X_new = X_new[model.feature_names_in_]
    
    age_fare_values = X_new[['Age', 'Fare']].values
    scaled_values = scaler.transform(age_fare_values)
    X_new[['Age', 'Fare']] = scaled_values

    # Predict
    pred_class = model.predict(X_new)[0]
    pred_prob = model.predict_proba(X_new)
    
    print("Predicted class:", pred_class)
    print("Predicted probabilities shape:", pred_prob.shape)  # Check shape
    print("Predicted probabilities:", pred_prob)
    
    # Return the first element of probabilities
    return pred_class, pred_prob[0]  # This should be 1D array


def get_model_performance():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, "metrics.json"), "r") as f:
        metrics = json.load(f)   # loads into a Python dict
    return metrics

# Example usage
# print(get_model_performance())          # prints entire metrics.json as a dict
# print(get_model_performance()['accuracy'])  # prints accuracy from metrics.json
# print(get_model_performance()['precision'])  # prints precision from metrics.json
# print(get_model_performance()['recall'])     # prints recall from metrics.json
# print(get_model_performance()['f1'])         # prints f1 score from metrics.json

# This block will only run when executing this file directly (e.g. python titanic_predict.py)
if __name__ == "__main__":
    # test code (won’t run in Django)
    predict_passenger(data_dict)
    get_model_performance()