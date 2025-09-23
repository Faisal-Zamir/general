# forms.py
from django import forms

class PassengerForm(forms.Form):
    PCLASS_CHOICES = [
        (1, "First Class"),
        (2, "Second Class"),
        (3, "Third Class"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    EMBARKED_CHOICES = [
        ("C", "Cherbourg"),
        ("Q", "Queenstown"),
        ("S", "Southampton"),
    ]
    CABIN_CHOICES = [
        ("A", "Deck A"),
        ("B", "Deck B"),
        ("C", "Deck C"),
        ("D", "Deck D"),
        ("E", "Deck E"),
        ("F", "Deck F"),
        ("G", "Deck G"),
        ("Unknown", "No Cabin"),
    ]
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
        ('Rare', 'Rare / Other'),
    ]

    pclass = forms.ChoiceField(choices=PCLASS_CHOICES, label="Passenger Class")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    age = forms.IntegerField(label="Age", min_value=0)
    fare = forms.FloatField(label="Fare ($)", min_value=0)
    sibsp = forms.IntegerField(label="Siblings/Spouses Aboard", min_value=0)
    parch = forms.IntegerField(label="Parents/Children Aboard", min_value=0)
    embarked = forms.ChoiceField(choices=EMBARKED_CHOICES, label="Port of Embarkation")
    cabin_deck = forms.ChoiceField(choices=CABIN_CHOICES, label="Cabin Deck", required=False)
    title = forms.ChoiceField(choices=TITLE_CHOICES, label='Title', required=True)