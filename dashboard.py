import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("Smart Energy Analytics")

# load and clean
df = pd.read_csv("24_hours_kwp_increasing.csv")
df = df.dropna(subset=["kwp"])
df["hour_num"] = df["hour"].str[:2].astype(int)

# alerts
threshold = df["kwp"].mean() * 1.5
df["alert"] = df["kwp"] > threshold

# cost
df["cost"] = df["kwp"] * df["hour_num"].apply(lambda h: 4 if h < 18 else 8)

# model and unusual readings
X = df[["hour_num"]]
y = df["kwp"]
model = LinearRegression()
model.fit(X, y)
df["predicted"] = model.predict(X)
df["error"] = (df["kwp"] - df["predicted"]).abs()
df["unusual"] = df["error"] > 0.5

st.subheader("Hourly data")
st.dataframe(df[["hour", "kwp", "cost", "alert", "unusual"]])

st.subheader("kWp with threshold")
fig, ax = plt.subplots()
ax.plot(df["hour_num"], df["kwp"], marker="o", label="kWp")
ax.axhline(threshold, color="red", linestyle="--", label="threshold")
ax.scatter(df[df["alert"]]["hour_num"], df[df["alert"]]["kwp"], color="red", zorder=3, label="alert")
ax.set_xlabel("Hour of day")
ax.set_ylabel("kWp")
ax.legend()
st.pyplot(fig)

st.subheader("Cost per hour")
st.bar_chart(df.set_index("hour")["cost"])

st.subheader("Unusual readings (model gap above 0.5)")
st.dataframe(df[df["unusual"]][["hour", "kwp", "predicted", "error"]])