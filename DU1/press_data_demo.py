import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

PATH = "DU1/Press_oil_data.csv"

# --------------------------
# Load & prepare data
data = pd.read_csv(PATH, sep=";", quotechar='"', parse_dates=["timestamp"])

data.rename(
    columns={
        "timestamp": "Date_time",
        "deviceId": "Device_id",
        "valueInt": "Oil_temperature",
    },
    inplace=True,
)

data = (
    data.dropna(subset=["Date_time", "Oil_temperature"])
    .sort_values("Date_time")
    .reset_index(drop=True)
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
# Visualization with Plotly (static)
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

# --------------------------
# Visualization with Plotly (animated growth, hourly average)
data_hour = data.copy()
data_hour["Hour"] = data_hour["Date_time"].dt.floor("h")

hourly = (
    data_hour.groupby(["Device_id", "Hour"], as_index=False)["Oil_temperature"]
    .mean()
    .rename(columns={"Hour": "Date_time"})
    .sort_values("Date_time")
    .reset_index(drop=True)
)

hourly["frame"] = hourly["Date_time"].rank(method="dense").astype(int) - 1
max_frame = int(hourly["frame"].max())

frames = []
for f in range(max_frame + 1):
    df_f = hourly[hourly["frame"] <= f].copy()
    df_f["frame"] = f
    frames.append(df_f)

anim_hourly = pd.concat(frames, ignore_index=True)

fig_anim = px.line(
    anim_hourly,
    x="Date_time",
    y="Oil_temperature",
    color="Device_id",
    animation_frame="frame",
    animation_group="Device_id",
    title="Hourly average of press oil temperature",
)

fig_anim.update_yaxes(range=[0, 50])
fig_anim.update_xaxes(
    range=[hourly["Date_time"].min(), hourly["Date_time"].max()]
)

fig_anim.update_layout(
    xaxis_title="Date and time",
    yaxis_title="Oil temperature [°C]",
    transition={"duration": 0},
)

fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["redraw"] = False

fig_anim.show()
