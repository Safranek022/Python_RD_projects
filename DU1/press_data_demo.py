import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

PATH = "DU1/Press_oil_data.csv"

data = pd.read_csv(PATH, sep=";", quotechar='"', parse_dates=["timestamp"])

data.rename(
    columns={
        "timestamp": "Date_time",
        "deviceId": "Device_id",
        "valueInt": "Oil_temperature",
    },
    inplace=True,
)

x_axis = data["Date_time"]
y_axis = data["Oil_temperature"]
hue = data["Device_id"]

# --------------------------
# Visualization with Seaborn
plt.figure(figsize=(20, 10))
seabornGraph = sns.lineplot(
    data=data, hue=hue, x=x_axis, y=y_axis, palette="Set2"
)
seabornGraph.set_title("Press oil temperature", fontsize=20)
seabornGraph.set_xlabel("Date and time", fontsize=15)
seabornGraph.set_ylabel("Oil temperature [°C]", fontsize=15)
seabornGraph.set_ylim(30, 45)

plt.show()

# --------------------------
# Visualization with Plotly
plotlyGraph = px.line(
    data,
    x="Date_time",
    y="Oil_temperature",
    color="Device_id",
    title="Press oil temperature",
)
plotlyGraph.update_layout(
    xaxis_title="Date and time", yaxis_title="Oil temperature [°C]"
)
plotlyGraph.show()
