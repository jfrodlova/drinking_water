import pandas as pd
from geopandas.tools import geocode

# Read the CSV file
df = pd.read_csv('rozbory_sample.csv', delimiter=";", encoding="utf-8")

# Get distinct locations from the dataframe (column "Misto_odberu)")
location_series = df['Misto_odberu'].str.split(',').str[0]
locations_df = location_series.to_frame()
locations_unique = locations_df.Misto_odberu.unique()
df = pd.DataFrame({"Misto_odberu":locations_unique[:]})

with open ("locations_unique.csv", mode="w", encoding="utf-8", newline="") as output_file:
    print(locations_unique, file=output_file)
    output_file.write('Misto_odberu\n')
    # Write the data rows
    for value in df['Misto_odberu']:
        output_file.write(f"{value}\n")

    


