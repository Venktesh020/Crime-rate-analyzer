
# AI-Powered Crime Intelligence System - Top 1% Evaluation Build

## Project Title
AI-Powered Crime Intelligence System with District-Level Risk Prediction and Geo-Spatial Visualization

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## Important Features for Evaluation

1. District-wise crime analysis
2. Crime categories:
   - Violent Crimes
   - Property Crimes
   - Crimes Against Women
3. AI prediction using Random Forest
4. Model comparison with Linear Regression
5. Risk Score formula:
   Risk Score = 0.5 × Violent + 0.3 × Property + 0.2 × Crimes Against Women
6. Risk classification:
   - Low Risk
   - Medium Risk
   - High Risk
7. Geo-spatial map visualization using Leaflet
8. Smart AI insight generation
9. Top risk district ranking
10. Interactive dashboard

## Dataset Format

Replace `data/crime_data.csv` with real NCRB district data using this column format:

```text
state,district,year,violent_crimes,property_crimes,crimes_against_women,latitude,longitude
```

## Demo Script

Say this during project evaluation:

"This project analyzes Indian district-level crime data using AI. It categorizes crimes into violent crimes, property crimes, and crimes against women. The system calculates a weighted risk score, predicts future crime using Random Forest, compares model performance, and displays district-wise risk on a map dashboard. This helps in identifying high-risk districts and supports data-driven crime prevention planning."

## Note

The included dataset is sample/demo data. For final submission, replace it with verified NCRB district-level data.
