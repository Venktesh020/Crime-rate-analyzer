
from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
import os

app = Flask(__name__)
DATA_PATH = "data/crime_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["total_crimes"] = df["violent_crimes"] + df["property_crimes"] + df["crimes_against_women"]
    df["risk_score"] = (
        0.5 * df["violent_crimes"] +
        0.3 * df["property_crimes"] +
        0.2 * df["crimes_against_women"]
    )
    q1 = df["risk_score"].quantile(0.33)
    q2 = df["risk_score"].quantile(0.66)

    def risk_level(score):
        if score <= q1:
            return "Low Risk"
        elif score <= q2:
            return "Medium Risk"
        return "High Risk"

    df["risk_level"] = df["risk_score"].apply(risk_level)
    return df

def train_model():
    df = load_data()
    X = pd.get_dummies(df[["state", "district", "year", "violent_crimes", "property_crimes", "crimes_against_women"]], drop_first=True)
    y = df["total_crimes"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    lr = LinearRegression()

    rf.fit(X_train, y_train)
    lr.fit(X_train, y_train)

    rf_pred = rf.predict(X_test)
    lr_pred = lr.predict(X_test)

    os.makedirs("models", exist_ok=True)
    joblib.dump(rf, "models/random_forest_model.pkl")
    joblib.dump(X.columns.tolist(), "models/model_columns.pkl")

    return {
        "Random Forest": {
            "R2 Score": round(float(r2_score(y_test, rf_pred)), 3),
            "MAE": round(float(mean_absolute_error(y_test, rf_pred)), 2)
        },
        "Linear Regression": {
            "R2 Score": round(float(r2_score(y_test, lr_pred)), 3),
            "MAE": round(float(mean_absolute_error(y_test, lr_pred)), 2)
        }
    }

@app.route("/")
def home():
    df = load_data()
    latest_year = df["year"].max()
    latest = df[df["year"] == latest_year]

    cards = {
        "total_districts": df["district"].nunique(),
        "total_states": df["state"].nunique(),
        "latest_year": int(latest_year),
        "total_crimes": int(latest["total_crimes"].sum()),
        "high_risk": int((latest["risk_level"] == "High Risk").sum())
    }

    districts = sorted(df["district"].unique())
    states = sorted(df["state"].unique())
    latest_records = latest.sort_values("risk_score", ascending=False).head(10).to_dict(orient="records")

    return render_template(
        "index.html",
        cards=cards,
        districts=districts,
        states=states,
        latest_records=latest_records
    )

@app.route("/api/chart-data")
def chart_data():
    df = load_data()
    district = request.args.get("district", "New Delhi")
    data = df[df["district"] == district].sort_values("year")
    return jsonify({
        "years": data["year"].tolist(),
        "violent": data["violent_crimes"].tolist(),
        "property": data["property_crimes"].tolist(),
        "women": data["crimes_against_women"].tolist(),
        "total": data["total_crimes"].tolist()
    })

@app.route("/api/map-data")
def map_data():
    df = load_data()
    latest = df[df["year"] == df["year"].max()].copy()
    return jsonify(latest[[
        "state", "district", "latitude", "longitude", "total_crimes", "risk_score", "risk_level"
    ]].to_dict(orient="records"))

@app.route("/api/category-share")
def category_share():
    df = load_data()
    district = request.args.get("district", "New Delhi")
    latest = df[(df["district"] == district) & (df["year"] == df["year"].max())].iloc[0]
    return jsonify({
        "labels": ["Violent Crimes", "Property Crimes", "Crimes Against Women"],
        "values": [
            int(latest["violent_crimes"]),
            int(latest["property_crimes"]),
            int(latest["crimes_against_women"])
        ]
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    df = load_data()
    payload = request.get_json()
    state = payload.get("state")
    district = payload.get("district")
    year = int(payload.get("year"))

    district_df = df[df["district"] == district].sort_values("year")
    latest = district_df.iloc[-1]

    if not os.path.exists("models/random_forest_model.pkl"):
        train_model()

    model = joblib.load("models/random_forest_model.pkl")
    columns = joblib.load("models/model_columns.pkl")

    input_df = pd.DataFrame([{
        "state": state,
        "district": district,
        "year": year,
        "violent_crimes": latest["violent_crimes"],
        "property_crimes": latest["property_crimes"],
        "crimes_against_women": latest["crimes_against_women"]
    }])

    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=columns, fill_value=0)

    prediction = int(model.predict(input_encoded)[0])

    trend = "increasing" if district_df["total_crimes"].iloc[-1] > district_df["total_crimes"].iloc[-3] else "stable/decreasing"

    return jsonify({
        "predicted_total_crime": prediction,
        "current_risk_score": round(float(latest["risk_score"]), 2),
        "current_risk_level": latest["risk_level"],
        "trend": trend,
        "smart_insight": f"{district} is classified as {latest['risk_level']}. The recent crime trend is {trend}. Preventive planning should focus on the highest contributing crime category."
    })

@app.route("/api/train")
def train():
    return jsonify(train_model())

if __name__ == "__main__":
    app.run(debug=True)
