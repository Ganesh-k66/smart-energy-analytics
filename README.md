# Smart Energy Analytics

**Hourly kWp analysis with a tariff, an alert rule and a simple forecast model.**

Analyses one day of hourly kWp readings (23 rows after cleaning). It flags high readings, costs each hour, and flags readings that don't fit a straight-line forecast.

---

## Run it

```bash
pip install -r requirements.txt
python app.py                           # analysis and charts
python -m streamlit run dashboard.py    # dashboard in the browser
```

---

## Verified behaviour

Measured on the sample data:

| Check | Result |
|---|---|
| Rows after cleaning | 23 (10:00 removed) |
| Alert threshold | 1.88 (average × 1.5) |
| Flagged hours | 18:00 to 23:00 |
| Unusual readings, original data | 0 |
| Unusual readings, 14:00 set to 4.0 | 1 (gap 2.38) |

---

## Method

- **Threshold:** average kWp × 1.5. Readings above it are alerts.
- **Cost:** 4 per unit before 18:00, 8 from 18:00, multiplied by kWp.
- **Model:** linear regression predicts kWp from the hour. A gap above 0.5 is unusual.

---

## Limitations

- One day of data with a straight-line pattern, so the model fits it almost perfectly.
- kWp is a solar capacity unit, but the cost assumes kWh. Treat the cost figures as an estimate.
