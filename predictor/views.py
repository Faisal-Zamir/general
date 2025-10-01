from django.shortcuts import render
from predictor.M_Files.titanic_predict import predict_passenger, get_model_performance
from .forms import PassengerForm
import pandas as pd
from django.http import JsonResponse

data_dict = {
    'Pclass': 3,
    'Age': 190,
    'SibSp': 0,
    'Parch': 0,
    'Fare': 1.25,
    'HasCabin': 1,
    'Sex_mapped': 1,   # 1 = male, 0 = female (example)
    'FamilySize': 1,
    'IsAlone': 1,
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
def homepage(request):
    feature_dict = None
    survived = None
    prob = None
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            # get raw POST data from form
            data = request.POST  
            # 2. Feature engineering

            # 1. Base fields directly from form
            pclass = int(data.get('pclass'))
            age = float(data.get('age'))
            sibsp = int(data.get('sibsp'))
            parch = int(data.get('parch'))
            fare = float(data.get('fare'))
            cabin_deck = data.get('cabin_deck')

            # HasCabin
            has_cabin = 0 if cabin_deck == "Unknown" else 1

            gender = data.get('gender')
            # Gender mapping
            sex = 1 if gender.lower() == "male" else 0

            # Family size
            family_size = sibsp + parch + 1
            # IsAlone
            is_alone = 1 if family_size == 1 else 0
            title = data.get('title')   # make sure you have this in your form
            embarked = data.get('embarked')
            cabin_deck = data.get('cabin_deck')

            # Title one-hot
            title_features = {
                "Title_Miss": 1 if title == "Miss" else 0,
                "Title_Mr": 1 if title == "Mr" else 0,
                "Title_Mrs": 1 if title == "Mrs" else 0,
                "Title_Rare": 1 if title == "Rare" else 0,
            }
            # Embarked one-hot
            embarked_features = {
                "Embarked_C": 1 if embarked == "C" else 0,
                "Embarked_Q": 1 if embarked == "Q" else 0,
                "Embarked_S": 1 if embarked == "S" else 0,
            }

            # CabinDeck one-hot
            cabin_features = {
                "CabinDeck_A": 1 if cabin_deck == "A" else 0,
                "CabinDeck_B": 1 if cabin_deck == "B" else 0,
                "CabinDeck_C": 1 if cabin_deck == "C" else 0,
                "CabinDeck_D": 1 if cabin_deck == "D" else 0,
                "CabinDeck_E": 1 if cabin_deck == "E" else 0,
                "CabinDeck_F": 1 if cabin_deck == "F" else 0,
                "CabinDeck_G": 1 if cabin_deck == "G" else 0,
                "CabinDeck_T": 1 if cabin_deck == "T" else 0,
                "CabinDeck_Unknown": 1 if cabin_deck == "Unknown" else 0,
            }



            # 3. Final feature dict
            feature_dict = {
                "Pclass": pclass,
                "Age": age,
                "SibSp": sibsp,
                "Parch": parch,
                "Fare": fare,
                "HasCabin": has_cabin,
                "Sex_mapped": sex,
                "FamilySize": family_size,
                "IsAlone": is_alone,
                **title_features,
                **embarked_features,
                **cabin_features,
                
            }

            # print for debugging
            # print("Final features for model:", feature_dict)
            try:
                pred_class, pred_prob = predict_passenger(feature_dict)
                survived = pred_class
                survived = int(survived)  # Convert numpy.int64 to Python int
                prob = round(pred_prob[0] * 100, 2)
                
                # Check if it's an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # Return JSON for AJAX
                    prob_survived = prob if survived == 1 else (100 - prob)
                    prob_not_survived = (100 - prob) if survived == 1 else prob
                    prob_survived = float(prob_survived)
                    prob_not_survived = float(prob_not_survived) 
                    return JsonResponse({
                        'survived': survived,
                        'prob_surv': prob_survived,
                        'prob_not': prob_not_survived,
                        'success': True
                    })
                    
                    
            except Exception as e:
                print(f"Prediction error: {e}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'error': 'Prediction failed'})
                survived = None
                prob = None

        else:
            print("Form errors:", form.errors)  # this prints to console
    else:
        form = PassengerForm()

    # X = pd.DataFrame([feature_dict])   # list of dict → DataFrame (2D)
    # pred_class , pred_prob = predict_passenger(X)
    # survived = pred_class   # 0 = did not survive, 1 = survived
    # prob = round(pred_prob[0] * 100, 2)
    # print("Result in view section")
    # print(survived)
    # print(prob)
    

    various_metrics = get_model_performance()
    # Convert to percentage + round
    formatted_metrics = {
        key: f"{round(value * 100, 2)}" for key, value in various_metrics.items()
    }

    # Debug print
    # for key, value in formatted_metrics.items():
    #     print(f"{key}: {value}")
    print("Before context")
    print("Survived:", survived, "Prob:", prob)
    context = {
        "metrics": formatted_metrics,
        "survived": survived,
        "prob": prob,
        "form": form,
               }
    return render(request, "predictor/index.html", context)


