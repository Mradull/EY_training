##########START####################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("urban_mobility.csv")

##########A1####################
print(df.head())

##########A2####################
df["Energy_Per_Km"] = df["Energy_Used_kWh"] / df["Distance_Km"]
print(df["Energy_Per_Km"])

##########A3####################

print(df[(df["Vehicle_Type"] == "Electric Van") & (df["Maintenance_Flag"] == "Yes")])

##########A4####################

result = df.groupby("Vehicle_Type").agg(
    Average_Distance = ("Distance_Km", "mean"),
    Total_trip = ("Trips_Count", "sum"),
)
print(result)

##########A5####################

mean_energy_used = np.mean(df["Energy_Used_kWh"])
max_energy_used = np.max(df["Energy_Used_kWh"])
min_energy_used = np.min(df["Energy_Used_kWh"])
print("Mean Energy Used = ", mean_energy_used)
print("Max Energy Used = ", max_energy_used)
print("Min Energy Used = ", min_energy_used)

##########A6####################

avg_energy = df.groupby("Vehicle_Type")["Energy_Used_kWh"].mean()
plt.figure(figsize=(10, 10))
avg_energy.plot(kind="bar")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Energy Used (kWh)")
plt.title("Average Energy Used (kWh) by Vehicle Type")
plt.show()

##########A7####################

df = pd.read_json("equipment_events.json")
print(df[["event_id" , "asset"  , "severity"]])

##########A8####################

result = df[df["temperature"] > 70]
result["actions"] = result["actions"].fillna("No actions recorded")
print(result)
##########A9####################

with open("coastal_monitoring_log.txt" , "r") as f:
    text = f.read()
total_wrods = len(text.split())
count = text.count("inspection")
print("Total words" , total_wrods)
print("Number of times inspection appears" , count)
##########A10####################
lines = text.splitlines("\n")
for line in lines:
    if"boardwalk" in line.lower() or "maintenance" in line.lower() or "wind" in line.lower():
        print(line)
        
##########END####################
