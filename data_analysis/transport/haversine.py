import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

def find_closest_schools(bus_stops, schools, city):
    """
    Find the closest school for each bus stop and save the results to a CSV file.

    Parameters:
    bus_stops (pandas.DataFrame): DataFrame containing bus stop data.
    schools (pandas.DataFrame): DataFrame containing school data.
    city (str): The city name ('Santiago' or 'Copiapó').

    Returns:
    pandas.DataFrame: DataFrame containing the closest school for each bus stop and the distance.
    """
    # Prepare a list to store the results
    results = []

    # Define the starting value for COD_COM_RBD based on the city
    if city == 'Santiago':
        cod_com_rbd_start = 13
        csv_filename = 'closest_schools_santiago.csv'
    elif city == 'Copiapó':
        cod_com_rbd_start = 31
        csv_filename = 'closest_schools_copiapo.csv'
    else:
        raise ValueError("Invalid city name. Please provide 'Santiago' or 'Copiapó'.")

    print('Finding closest schools...')

    # Filter the schools based on COD_COM_RBD
    valid_schools = schools[schools['COD_COM_RBD'].astype(str).str.startswith(str(cod_com_rbd_start))]

    # Convert school coordinates to radians for use with BallTree
    school_coords = np.radians(valid_schools[['LATITUD', 'LONGITUD']].values)

    # Create a BallTree
    tree = BallTree(school_coords, leaf_size=15, metric='haversine')

    # For each bus stop, find the closest school
    # For each bus stop, find the closest school
    for i, bus_stop in bus_stops.iterrows():
        bus_stop_coords = np.radians([[bus_stop['stop_lat'], bus_stop['stop_lon']]])
        dist, ind = tree.query(bus_stop_coords, k=1)  # k=1 means find only the nearest neighbor
        closest_school = schools.iloc[ind[0][0]]  # Access the first element of ind[0]
        results.append([bus_stop['stop_id'], bus_stop['stop_name'], closest_school['RBD'], closest_school['NOM_RBD'], dist[0][0] * 6367])
              
    # Convert the results to a DataFrame
    results_df = pd.DataFrame(results, columns=['stop_id', 'stop_name', 'school_RBD', 'school_name', 'distance'])

    # Save the results to a CSV file
    results_df.to_csv(csv_filename, index=False)

    return results_df

def main():
    # bus_stops_santiago = pd.read_csv('santiago/stops.csv')
    bus_stops_copiapo = pd.read_csv('copiapó/stops.csv')
    schools = pd.read_csv('../colegios.csv')
    print('Data loaded.')

    # Find closest schools for Copiapó
    find_closest_schools(bus_stops_copiapo, schools, 'Copiapó')

if __name__ == "__main__":
    main()
