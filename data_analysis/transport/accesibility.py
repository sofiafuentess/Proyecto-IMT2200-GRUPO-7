import pandas as pd

def calculate_accessibility_score(city):
    """
    Calculate the accessibility score for each stop in the given city.

    Parameters:
    - city (str): The name of the city for which to calculate the accessibility score.

    Raises:
    - ValueError: If an invalid city name is provided.

    Returns:
    - None: The function saves the accessibility scores as a CSV file.
    """
    print(f'Calculating accessibility score for {city}')

    # Get the path to the data
    if city == 'Copiapó':
        data_path = 'copiapó'
    elif city == 'Santiago':
        data_path = 'santiago'
    else:
        raise ValueError('Invalid city name')
    
    # Load the data
    trips = pd.read_csv(f'{data_path}/trips.csv')
    stop_times = pd.read_csv(f'{data_path}/stop_times.csv')
    routes = pd.read_csv(f'{data_path}/routes.csv')
    calendar = pd.read_csv(f'{data_path}/calendar.csv')

    # Merge the data
    merged = pd.merge(stop_times, trips, on='trip_id')
    merged = pd.merge(merged, routes, on='route_id')
    merged = pd.merge(merged, calendar, on='service_id')

    # Count the frequency and number of routes for each stop
    stop_counts = merged['stop_id'].value_counts()
    route_counts = merged.groupby('stop_id')['route_id'].nunique()

    # Min-Max normalization
    stop_counts = (stop_counts - stop_counts.min()) / (stop_counts.max() - stop_counts.min())
    route_counts = (route_counts - route_counts.min()) / (route_counts.max() - route_counts.min())

    # Combine the counts to get the accessibility score for each stop
    accessibility = (stop_counts + route_counts) / 2

    # Create a DataFrame with the accessibility scores
    accessibility_df = pd.DataFrame({'stop_id': accessibility.index, 'score': accessibility.values})

def main():
    calculate_accessibility_score('Copiapó')
    calculate_accessibility_score('Santiago')
    print('Accessibility scores saved as CSV files')

if __name__ == "__main__":
    main()

def main():
    calculate_accessibility_score('Copiapó')
    calculate_accessibility_score('Santiago')
    print('Accessibility scores saved as CSV files')

if __name__ == "__main__":
    main()


