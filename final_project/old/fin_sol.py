# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:42:10 2018

@author: Florian Ulrich Jehn
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Task 1
# Read in
dem = pd.read_table("location_height_landcover.txt", sep=" ", header=None)
dem.columns  = ["Latitude", "Longitude", "Elevation", "Landcover_old"]
# Rewrite the landcover
dem["Landcover"] = np.nan
dem["Landcover_old"] = dem["Landcover_old"].astype('str')
dem["Landcover_old"] = dem["Landcover_old"].str[:-2]
# Set the new landcover
dem.loc[dem["Landcover_old"].str.startswith("2"), "Landcover"] = "Crops"
dem.loc[dem["Landcover_old"].str.startswith("3"), "Landcover"] = "Wood"
dem.loc[dem["Landcover_old"].str.startswith("231"), "Landcover"] = "Grassland"
# The rest can be filled with 1
dem.fillna("Cities_Other", inplace=True)
# Remove the old column before saving
del(dem["Landcover_old"])
dem.to_csv("location_height_landcover_new.txt", sep=" ", index=False)


# Task 2
dem = pd.read_table("location_height_landcover_new.txt", sep=" ")
rain = pd.read_table("interpolated_rainfall.txt", sep=" ", header=None)
# Fix the decimal point error
for column in rain.columns:
    rain[column] = round(rain[column] / 10, 2)
dem_rain = pd.merge(dem, rain, how="outer", left_index=True, right_index=True)
# Save the new file
dem_rain.to_csv("dem_rain.txt", sep=" ", index=False)


# Task 3
dem_rain = pd.read_table("dem_rain.txt", sep=" ", header=0)
# Create a column with the two height categories
dem_rain["Height_Cat"] = np.nan
dem_rain.loc[dem_rain["Elevation"] > 500, "Height_Cat"] = "High"
dem_rain.loc[dem_rain["Elevation"] < 500, "Height_Cat"] = "Low"

# Get all the combinations to calculate with them
grouped_dem_rain = dem_rain.groupby(["Landcover", "Height_Cat"])
for combi, combi_df in grouped_dem_rain:
    # Get only the rainfall columns 
    rain = combi_df.iloc[:, 5:-1]
    # Calculate the daily mean and save the series seperately
    rain = rain.mean(axis=0)
    rain.name = combi
    rain.to_csv("{}_{}_rain.csv".format(combi[0], combi[1]), sep=";", index=False)
    

# Task 4
fig, subplots = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True)
for i, landcover in enumerate(["Crops", "Grassland", "Wood", "Cities_Other"]):
    for j, height in enumerate(["Low", "High"]):
        ax = subplots[i, j]
        df = pd.read_csv("{}_{}_rain.csv".format(landcover, height), sep=";", header=None)
        ax = sns.boxplot(data=df, ax=ax, orient="h", whis="range")
        ax.set_facecolor("white")
        ax.grid(color="grey", alpha=0.3)
        if j == 0:
            ax.set_ylabel(landcover, rotation=90)
        if i == 0:
            ax.set_title(height)
        ax.set_yticklabels([])
        if i == 3:
            ax.set_xlabel("Rainfall [mm]")
    fig.suptitle("Rainfall Distribution", fontsize=14)
    fig.tight_layout()

plt.savefig("boxplots.png", dpi=200, bbox_inches="tight")
plt.show()







    
