

```python
# Dependencies
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```


```python
# Create engine
engine = create_engine("sqlite:///database/hawaii.sqlite")

# Declare Base
Base = automap_base()

# Use Base class to reflect database tables
Base.prepare(engine, reflect=True)
```


```python
# Check out tables
Base.classes.keys()
```




    ['measurements', 'stations']




```python
# Assign measurements class to variable
Measurement = Base.classes.measurements

# Assign stations class to variable
Station = Base.classes.stations
```


```python
# Create a session
session = Session(engine)
```


```python
# Display the row's columns and data in dictionary format
first_row = session.query(Measurement).first()
first_row.__dict__
```




    {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState at 0x1f05b33d518>,
     'date': '2010-01-01',
     'id': 1,
     'prcp': 0.08,
     'station': 'USC00519397',
     'tobs': 65}




```python
# Show top 10 rows of measurement table
session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).limit(10).all()
```




    [(1, 'USC00519397', '2010-01-01', 0.08, 65),
     (2, 'USC00519397', '2010-01-02', 0, 63),
     (3, 'USC00519397', '2010-01-03', 0, 74),
     (4, 'USC00519397', '2010-01-04', 0, 76),
     (5, 'USC00519397', '2010-01-07', 0.06, 70),
     (6, 'USC00519397', '2010-01-08', 0, 64),
     (7, 'USC00519397', '2010-01-09', 0, 68),
     (8, 'USC00519397', '2010-01-10', 0, 73),
     (9, 'USC00519397', '2010-01-11', 0.01, 64),
     (10, 'USC00519397', '2010-01-12', 0, 61)]



# Precipitation Analysis


```python
# See latest dates
session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).\
    order_by(Measurement.date.desc()).limit(5).all()
```




    [(2685, 'USC00519397', '2017-08-23', 0, 81),
     (7318, 'USC00514830', '2017-08-23', 0, 82),
     (10915, 'USC00519523', '2017-08-23', 0.08, 82),
     (18103, 'USC00516128', '2017-08-23', 0.45, 76),
     (2684, 'USC00519397', '2017-08-22', 0, 82)]




```python
# Query date for the past 12 months
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Query for precipitation
prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= query_date).all()
    
# Create dataframe from query
prcp_df = pd.DataFrame(prcp_data)

# Change column types
prcp_df["date"] = pd.to_datetime(prcp_df["date"])
prcp_df["prcp"] = pd.to_numeric(prcp_df["prcp"])

# Set date as index
prcp_df = prcp_df.set_index(["date"])
prcp_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-23</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>0.08</td>
    </tr>
    <tr>
      <th>2016-08-25</th>
      <td>0.08</td>
    </tr>
    <tr>
      <th>2016-08-26</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2016-08-27</th>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Seaborn default
ax = sns.set()

# Use DataFrame.plot() in order to create a bar chart of the data
prcp_df.plot(kind="line", color="dodgerblue", linewidth=5, figsize=(14, 10), fontsize=18, ax=ax)

# Set a title for the chart
plt.title("Precipitation (Past 12 Months)", fontsize=18)
plt.xlabel("Date", fontsize=18)
plt.ylabel("Precipitation (in)", fontsize=18)
plt.legend(fontsize=18)

# Show
plt.show()
```


![png](images/output_10_0.png)



```python
# Summary statistics
prcp_df.describe()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2021.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.177279</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.461190</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.130000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.700000</td>
    </tr>
  </tbody>
</table>
</div>



# Station Analysis


```python
# Check out table columns
session.query(Station).first().__dict__
```




    {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState at 0x1f05b1452b0>,
     'elevation': 3.0,
     'id': 1,
     'latitude': 21.2716,
     'longitude': -157.8168,
     'name': 'WAIKIKI 717.2, HI US',
     'station': 'USC00519397'}




```python
# Query to calculate the total number of stations
num_stations = session.query(Station.id).count()
print(f"Number of stations: {num_stations}")
```

    Number of stations: 9
    


```python
# Query to find the most active stations
session.query(Measurement.station, Station.name, func.count(Measurement.id)).\
    filter(Measurement.station == Station.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.id).desc()).all()
```




    [('USC00519281', 'WAIHEE 837.5, HI US', 2772),
     ('USC00513117', 'KANEOHE 838.1, HI US', 2696),
     ('USC00519397', 'WAIKIKI 717.2, HI US', 2685),
     ('USC00519523', 'WAIMANALO EXPERIMENTAL FARM, HI US', 2572),
     ('USC00516128', 'MANOA LYON ARBO 785.2, HI US', 2484),
     ('USC00514830', 'KUALOA RANCH HEADQUARTERS 886.9, HI US', 1937),
     ('USC00511918', 'HONOLULU OBSERVATORY 702.2, HI US', 1932),
     ('USC00517948', 'PEARL CITY, HI US', 683),
     ('USC00518838', 'UPPER WAHIAWA 874.3, HI US', 342)]



###### USC00519281, WAIHEE 837.5, HI US has the highest number of observations of 2772.


```python
# Query date for the past 12 months
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Query to retrieve the last 12 months of temperature observation data (tobs)
tobs_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                filter(Measurement.date > query_date).\
                filter(Measurement.station == "USC00519281").all()

# Create tobs datafram
tobs_df = pd.DataFrame(tobs_data)
tobs_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519281</td>
      <td>2016-08-24</td>
      <td>77</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519281</td>
      <td>2016-08-25</td>
      <td>80</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519281</td>
      <td>2016-08-26</td>
      <td>80</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519281</td>
      <td>2016-08-27</td>
      <td>75</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519281</td>
      <td>2016-08-28</td>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Seaborn default
ax = sns.set()

# Plot
tobs_df.plot(kind="hist", color="dodgerblue", bins=12, figsize=(10, 8), fontsize=18, ax=ax)

# Labels
plt.title("WAIHEE 837.5, HI US Temperature Observation Data (Past 12 Months)", fontsize=18)
plt.xlabel("Temperature (F)", fontsize=16)
plt.ylabel("Frequency", fontsize=16)
plt.legend(fontsize=16)

# Show plot
plt.show()
```


![png](images/output_18_0.png)


# Temperature Analysis


```python
new_start_date = dt.datetime.strptime("2018-01-01", "%Y-%m-%d") - dt.timedelta(days=365)
print(new_start_date)

new_start_date = dt.datetime.strftime(new_start_date, "%Y-%m-%d")
print(new_start_date)
```

    2017-01-01 00:00:00
    2017-01-01
    


```python
def calc_temps(start_date, end_date):
    # Convert dates to datetime objects and use previous year's dates
    new_start_date = dt.datetime.strptime(start_date, "%Y-%m-%d") - dt.timedelta(days=365)
    new_end_date = dt.datetime.strptime(end_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Convert dates back to strings
    new_start_date = dt.datetime.strftime(new_start_date, "%Y-%m-%d")
    new_end_date = dt.datetime.strftime(new_end_date, "%Y-%m-%d")
    
    # Query to filter data for those dates
    temp = session.query(Measurement.tobs).\
                filter(Measurement.date >= new_start_date).\
                filter(Measurement.date <= new_end_date).all()
    
    # Convert list of tuples into normal list
    temp = list(np.ravel(temp))
    
    # Calculate minimum temperature
    min_temp = min(temp)
    
    # Calculate average temperature
    avg_temp = np.mean(temp)
    
    # Calculate maximum temperature
    max_temp = max(temp)
    
    return min_temp, avg_temp, max_temp
```


```python
# Get min, avg, and max temp for date range
min_temp, avg_temp, max_temp = calc_temps("2018-04-14", "2018-04-22")

# Print to console
print("Trip Temperature Range")
print("-"*12)
print(f"Minimum temp: {min_temp}")
print(f"Average temp: {avg_temp:.1f}")
print(f"Maximum temp: {max_temp}")
```

    Trip Temperature Range
    ------------
    Minimum temp: 67
    Average temp: 72.8
    Maximum temp: 83
    


```python
# Set figure size
plt.figure(figsize=(2.5,6))

# Calculate tmin and tmax of yerr
yerr_min = abs(avg_temp - min_temp)
yerr_max = abs(avg_temp - max_temp)

# Create bar plot
plt.bar("", avg_temp, yerr=([yerr_min], [yerr_max]), color="lightcoral")

# Increase y tick labelsize
plt.tick_params(axis='y', which='major', labelsize=16)

# Labels
plt.title("Trip Average Temperature", fontsize=18)
plt.ylabel("Temperature (F)", fontsize=18)

# Show plot
plt.show()
```


![png](images/output_23_0.png)


# Rainfall Analysis


```python
# Query date for the past 12 months
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Calcualte the rainfall per weather station using the previous year's matching dates
precip_data = session.query(Station.name, func.sum(Measurement.prcp)).\
                filter(Measurement.station == Station.station).\
                filter(Measurement.date >= query_date).\
                group_by(Station.name).\
                order_by(func.sum(Measurement.prcp).desc()).all()

# Create dataframe
precip_df = pd.DataFrame(precip_data, columns=['Station Name', 'Total Precipitation (Past 12 Months)'])
precip_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Station Name</th>
      <th>Total Precipitation (Past 12 Months)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>147.81</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WAIHEE 837.5, HI US</td>
      <td>70.03</td>
    </tr>
    <tr>
      <th>2</th>
      <td>KANEOHE 838.1, HI US</td>
      <td>48.51</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>38.01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>33.24</td>
    </tr>
  </tbody>
</table>
</div>




```python
def daily_normals(a_date):
    """
    Grab min, avg, max temperatures for historic dates.
    """
    
    # Query to grab all historic temperatures by date
    temps = session.query(Measurement.tobs).\
                filter(Measurement.date.like(f"%{a_date}")).all()
    
    # Convert list of tuples into normal list
    temps = list(np.ravel(temps))
    
    # Calculate min, avg, and max temps
    min_temp = min(temps).astype(np.float)
    avg_temp = np.mean(temps).round(1).astype(np.float)
    max_temp = max(temps).astype(np.float)
    
    return min_temp, avg_temp, max_temp
```


```python
# Check daily_normals function
daily_normals("8-23")
```




    (67.0, 76.799999999999997, 87.0)




```python
def calc_trip_temps(start_date, end_date):
    """
    Returns dataframe of min, avg, and max temps for each day of trip.
    """
    # Calculate trip duration in days
    trip_duration =  (dt.datetime.strptime(end_date, "%Y-%m-%d") - dt.datetime.strptime(start_date, "%Y-%m-%d")).days
    
    # Instantiate trip_datetime
    trip_datetime = dt.datetime.strptime(start_date, "%Y-%m-%d")
    
    # List to hold all dates for trip, start with start date
    trip_date_list = [start_date]
    
    # List to hold month-day to loop through for daily_normals function
    month_day_list = [f"{dt.datetime.strftime(trip_datetime, '%m-%d')}"]
    
    for day in range(trip_duration):
        
        # Convert date to datetime, add one day
        trip_datetime += dt.timedelta(days=1)
        
        # Convert datetime to string
        trip_date = dt.datetime.strftime(trip_datetime, "%Y-%m-%d")
        
        # Grab only month and day
        month_day = f"{trip_datetime.month}-{trip_datetime.day}"
        
        # Append trip date to list of trip dates
        trip_date_list.append(trip_date)
        month_day_list.append(month_day)
    
    # Create lists to hold min, avg, and max temperatures
    min_temp_list = []
    avg_temp_list = []
    max_temp_list = []
        
    # Loop through each date in trip date list
    for date in month_day_list:
        
        # Pass date into daily_normals function
        min_temp, avg_temp, max_temp = daily_normals(date)
        
        # Append returns to lists
        min_temp_list.append(min_temp)
        avg_temp_list.append(avg_temp)
        max_temp_list.append(max_temp)

    # Create dataframe from lists
    trip_temp_df = pd.DataFrame({"Date": trip_date_list, 
                                 "Min Temp": min_temp_list, 
                                 "Avg Temp": avg_temp_list, 
                                 "Max Temp": max_temp_list})
    
    # Reorder columns
    trip_temp_df = trip_temp_df[["Date", "Min Temp", "Avg Temp", "Max Temp"]]
    
    # Set date as index
    trip_temp_df = trip_temp_df.set_index(["Date"])
    
    return trip_temp_df
```


```python
trip_duration =  (dt.datetime.strptime("2018-04-22", "%Y-%m-%d") - dt.datetime.strptime("2018-04-14", "%Y-%m-%d")).days
# trip_duration = trip_duration.days
print(trip_duration)
```

    8
    


```python
# Pass in trip start and end dates into calc_trip_temps to return min, avg, and max temps for each day
trip_temps = calc_trip_temps("2018-04-14", "2018-04-22")
trip_temps
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Min Temp</th>
      <th>Avg Temp</th>
      <th>Max Temp</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-04-14</th>
      <td>65.0</td>
      <td>72.7</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>2018-04-15</th>
      <td>61.0</td>
      <td>71.9</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>2018-04-16</th>
      <td>63.0</td>
      <td>71.6</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>2018-04-17</th>
      <td>65.0</td>
      <td>71.8</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2018-04-18</th>
      <td>67.0</td>
      <td>72.4</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2018-04-19</th>
      <td>65.0</td>
      <td>72.2</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th>2018-04-20</th>
      <td>64.0</td>
      <td>72.4</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>2018-04-21</th>
      <td>66.0</td>
      <td>72.3</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>2018-04-22</th>
      <td>65.0</td>
      <td>72.8</td>
      <td>84.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Set colors
pal = sns.color_palette("pastel")

# Plot lines
fig = trip_temps.plot(kind='area', stacked=False, color=pal, linewidth=6, alpha= 0.4, 
                     figsize=(12, 8), fontsize=18)

# Rotate dates
# plt.tick_params(axis='x', which='major', rotation=45, right=True)
fig.set_xticklabels(trip_temps.index.values, rotation=45, ha='right')

# Limit
plt.ylim(0, 90)

# Gridlines
plt.grid(color="lightslategrey", alpha=0.3)

# Labels
plt.title("Trip Forecast", fontsize=18)
plt.xlabel("Date", fontsize=18)
plt.ylabel("Temperature (F)", fontsize=18)
plt.legend(frameon=True, fontsize=14)

# Show
plt.show()
```


![png](images/output_31_0.png)

