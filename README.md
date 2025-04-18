# Flight ML AI Predictor

> A proof-of-concept project exploring how machine learning can help optimize flight search queries by predicting the airline most likely to return the cheapest fare.

## ✈️ What It Does
This project trains a machine learning model using real-world flight search data from multiple providers (e.g. Google Flights, Amadeus) to predict which airline will most likely offer the lowest fare for a specific route, date, and trip type.

## 🔍 Why This Matters
Flight search is computationally heavy. For a single query, hundreds of options may exist depending on dates, stops, carriers, and channels. Commercial travel platforms split queries to reduce response time—but it’s often done based on static rules.

This project explores a smarter way: **using historical search results to learn which airlines are worth querying first**.

---

## 🚦 Status
- [x] Data Collection (multiple providers)
- [x] Feature Engineering
- [x] Basic Random Forest Model (91% test accuracy)
- [x] Prediction Pipeline
- [ ] Azure ML Integration (coming soon!)
- [ ] UI / Visualization (optional)

---

## 🧠 How It Works

1. **Fetch Flight Search Results** from APIs (Google, Amadeus, integrate yours 😉)
2. **Parse & Normalize Offers**
3. **Identify Cheapest Offer per Route/Date**
4. **Prepare Dataset** for training
5. **Train Model** (Random Forest Classifier)
6. **Use Model** to predict likely cheapest airline

---

## 📂 Project Structure
```bash
backend/
├── api/                        # API-related scripts and endpoints
├── data/                       # Raw and processed datasets
├── data_collection/            # Scripts for collecting flight offers
|   ├── credentials.py          # API credentials loader
│   ├── fetch_batch_data.py     # Collect flight offers from external APIs
│   ├── flight_search.py        # Core flight search logic
├── data_processing/            # Scripts for feature engineering and data preparation
│   ├── prepare_model_data.py   # Feature engineering & labeling
|   ├── explore_data.py         # Scripts to get quick insights on collected data
├── model/                      # Saved models (pickle)
├── modeling/                   # Model training and evaluation scripts
│   ├── train_initial_model.py  # Model training pipeline
├── models/                     # Additional model-related utilities
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📊 Example Results
Test accuracy on sample dataset: **91%**

```txt
Label       Precision   Recall   F1-score   Support
B6          0.92       1.00     0.96       12
CX          0.90       1.00     0.95        9
TK          1.00       1.00     1.00        6
...
accuracy                           0.91       82
```

### 🔥 Top Features
```
booking_lead_time          0.0808
route_NYC_LON              0.0689
source_google_flights      0.0411
route_MIA_BOD              0.0349
```

---

## 🚀 Try It Yourself
1. Clone the repo:
```bash
git clone https://github.com/yourname/flight-ml-ai-predictor.git
cd flight-ml-ai-predictor
```

2. Create a virtual environment and install requirements:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.PS1 on Windows
pip install -r requirements.txt
```

3. Run data collection:
```bash
python fetch_batch_data.py
```

4. Prepare the dataset:
```bash
python prepare_model_data.py
```

5. Train the model:
```bash
python train_initial_model.py
```

---

## 🧠 Next Steps
- Integrate with Azure ML for large-scale training
- Use predictions to dynamically drive search orchestration
- Explore branded fares, customer profiles, and fare families

---

## 🛠 Built With
- Python + Pandas
- Scikit-learn
- Google Flights, Amadeus APIs

---

## 📄 License
MIT License

---

## 👨‍💻 Author
Julien Meiffren – [@julioMeif](https://github.com/julioMeif)

---

_This is just the beginning. The sky isn’t the limit—it’s just our training data._ 🚀
