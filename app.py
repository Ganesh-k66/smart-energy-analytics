import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("24_hours_kwp_increasing.csv")
print(df.head())                          # shows the first 5 rows
print(df.isna().sum())                     # counts missing values in each column
print(df[df["kwp"].isna()])                # shows the rows where kWp is empty.

#clean the data
df = df.dropna(subset=["kwp"])               # remove the row with the missing value
df["hour_num"] = df["hour"].str[:2].astype(int)  # "13:00" becomes 13

print(len(df))                               # how many rows are left
print(df["kwp"].describe())                  # count, average, min, max      

threshold = df["kwp"].mean() * 1.5           # 1.5 times the average
df["alert"] = df["kwp"] > threshold          # True if above the threshold
print(df[df["alert"]])                       # show only the flagged hours


#chart thereshols 
df[df["alert"]].to_csv("flagged_readings.csv", index=False)   # save alerts to a file

plt.plot(df["hour_num"], df["kwp"], marker="o", label="kWp")
plt.axhline(threshold, color="red", linestyle="--", label="threshold")
plt.xlabel("Hour of day")
plt.ylabel("kWp")
plt.title("Hourly values with alert threshold")
plt.scatter(df[df["alert"]]["hour_num"], df[df["alert"]]["kwp"], color="red", zorder=3, label="alert")
plt.legend()
plt.savefig("hourly_chart.png")
plt.show()

hourly_avg = df.groupby("hour_num")["kwp"].mean()   # average kWp for each hour
print(hourly_avg)


df["cost"] = df["kwp"] * df["hour_num"].apply(lambda h: 4 if h < 18 else 8)
print(df[["hour", "kwp", "cost"]])

#chart cost
plt.figure()
plt.bar(df["hour_num"], df["cost"], color="green")
plt.xlabel("Hour of day")
plt.ylabel("Cost (rate per unit × kWp)")
plt.title("Cost per hour")
plt.savefig("cost_chart.png")
plt.show()



from sklearn.linear_model import LinearRegression

X = df[["hour_num"]]     # inputs: the hour (double brackets keep it as a table)
y = df["kwp"]            # output: the kWp value we want to predict

model = LinearRegression()   # create an empty model
model.fit(X, y)              # learn the pattern from the data

df["predicted"] = model.predict(X)   # predicted kWp for each hour
print(df[["hour", "kwp", "predicted"]])

df["error"] = df["kwp"] - df["predicted"]     # actual minus predicted
df["error"] = df["error"].abs()               # make all errors positive (ignore direction)
print(df[["hour", "kwp", "predicted", "error"]])

error_limit = 0.5                            # gap bigger than this is unusual
df["unusual"] = df["error"] > error_limit     # True if the gap is too big
print(df[df["unusual"]])                      # show the unusual rows
print("unusual readings:", df["unusual"].sum())  # count the True values
