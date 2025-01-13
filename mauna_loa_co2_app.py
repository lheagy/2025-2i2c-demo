import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import ipywidgets

from matplotlib import rcParams
rcParams["font.size"]=14

co2_data_source = "https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/monthly/monthly_in_situ_co2_mlo.csv"

# read data and do some data cleaning
co2_data = pd.read_csv(
    co2_data_source, skiprows=np.arange(0, 64), na_values="-99.99",
    header=None
)

co2_data.columns = [
    "year", "month", "date (excel)", "date", "co2", "seasonally adjusted",
    "fit", "seasonally adjusted fit", "co2 filled", "seasonally adjusted filled",
    "station"
]

def plot_co2_data(data=co2_data, ax=None, xlim=None, ylim=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.plot(
        data["date"], data["co2"],
        label="CO$_2$ [ppm]"
    )
    ax.plot(
        data["date"], data["seasonally adjusted"],
        label="seasonally adjusted",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("CO$_2$ Concentration (ppm)")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid()
    return ax

def moving_average(data, window_size=1):
    n_data = len(data)
    average = np.full(n_data, np.nan)
    if window_size == 1:
        return data
    half_window = window_size // 2
    for i in range(half_window, n_data - half_window):
        average[i] = np.mean(data[i - half_window: i + half_window])
    return average

def plot_co2_average(window_size=1, xmin=None, xmax=None, ymin=None, ymax=None):
    averaged_co2 = moving_average(co2_data["co2"], window_size)

    ax=plot_co2_data(co2_data)
    ax.plot(
        co2_data["date"], averaged_co2,
        label=f"moving average: {window_size}"
    )
    ax.legend()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

def co2_app():
    return ipywidgets.interactive(
        plot_co2_average,
        window_size=ipywidgets.IntSlider(min=1, max=24, value=1),
        xmin=ipywidgets.FloatText(value=1955),
        xmax=ipywidgets.FloatText(value=2026),
        ymin=ipywidgets.FloatText(value=310),
        ymax=ipywidgets.FloatText(value=450)
    )
