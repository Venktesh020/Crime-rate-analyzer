# Crime Rate Analyzer

This project is a web application for analyzing crime data across states and districts in India. It uses Python, Flask, and machine learning to display crime statistics, compare crime categories, classify districts by risk score, and estimate total crime counts.

## Features

* View crime statistics by district and year.
* Analyze violent crimes, property crimes, and crimes against women.
* Compare Random Forest and Linear Regression models.
* View crime trends through charts.
* Display district-level information on a map.
* Calculate a crime risk score and classify districts as Low, Medium, or High Risk.
* Generate a prediction for a selected district and year.

## Technologies Used

* Python
* Flask
* Pandas and NumPy
* Scikit-learn
* Joblib
* HTML, CSS, and JavaScript
* Leaflet for map visualization

## Project Structure

```text
ai_crime_rate_analyzer_top_1_percent/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── final_crime_data_full_states_districts_2001_2024.csv
├── models/
├── static/
│   ├── css/
│   └── js/
└── templates/
    └── index.html
```

## How to Run the Project

### 1. Install Python

Install Python and make sure it is available from the command line.

### 2. Clone the repository

```bash
git clone https://github.com/Venktesh020/Crime-rate-analyzer.git
cd Crime-rate-analyzer
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

On Windows, activate it with:

```bash
.venv\Scripts\activate
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

### 5. Check the dataset path

The application reads the dataset from `data/crime_data.csv`.

The dataset included in this repository has a different filename. Either rename it to `crime_data.csv` or update the `DATA_PATH` variable in `app.py` to match the existing filename.

### 6. Start the application

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## Machine Learning

The project uses a Random Forest Regressor to estimate total crime counts and Linear Regression for comparison. The models are evaluated using R² score and Mean Absolute Error (MAE).

The application also calculates a risk score using the following weights:

* Violent crimes: 50%
* Property crimes: 30%
* Crimes against women: 20%

Risk levels are assigned using thresholds calculated from the dataset's risk scores. These categories are defined by the project and are not official government classifications.

## Dataset

The dataset is stored in the `data` folder and contains state, district, year, crime-category counts, and geographic coordinates.

The source and accuracy of the data should be verified before using the results for research or reporting. Historical data and model predictions should not be treated as official crime forecasts.

## Limitations

The quality of the results depends on the data provided to the application. The model's predictions may not reflect actual future crime counts and should be evaluated further before practical use.

This project was developed for educational and analytical purposes.

## Author

Venktesh Kumar

GitHub: https://github.com/Venktesh020
