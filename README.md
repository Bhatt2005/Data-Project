
#  Sports Endurance Analytics Dashboard

An interactive dashboard for analyzing and predicting sports endurance performance using training data.


# Tech Stack
Python, Streamlit, Pandas, NumPy, Matplotlib



# Installation & Run

```bash
git clone https://github.com/your-username/sports-endurance-analytics.git
cd sports-endurance-analytics
pip install streamlit pandas numpy matplotlib
streamlit run app.py
```


# Dataset
Place `sports_training_dataset_expanded.csv` in the root directory with these columns:

| Column | Description |
|---|---|
| `Gender` | Athlete gender |
| `Sport_Type` | Type of sport |
| `Age` | Athlete age |
| `Session_Duration` | Training session length (minutes) |
| `Heart_Rate_Avg` | Average heart rate (bpm) |
| `Speed_Avg` | Average speed (km/h) |
| `Distance_Covered` | Distance covered (meters) |
| `Technique_Score` | Technique rating |
| `Endurance_Score` | Target endurance score |.
