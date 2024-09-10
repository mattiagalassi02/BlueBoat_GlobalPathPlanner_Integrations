import src.coordinate_conversion as cc
import src.map_preparation as mp
import src.util_functions as uf
import matplotlib.pyplot as plt
import src.plot as pl
import numpy as np
import os
import csv

# Identifiers and paths for the logs
identifier_astar = input('Enter identifier for A*: ')
identifier_rrtstar = input('Enter identifier for RRT*: ')

# identifier_astar = "22_08_2024_18_07_08"
# identifier_rrtstar = "22_08_2024_17_45_34"

mapdata_path_astar = f'{os.getcwd()}/map_data/'
mapdata_path_rrtstar = f'{os.getcwd()}/map_data/'
setting_path_astar = f'{os.getcwd()}/map_settings.yaml'
setting_path_rrtstar = f'{os.getcwd()}/map_settings.yaml'
logging_path_astar = f'{os.getcwd()}/mission_logs/'
logging_path_rrtstar = f'{os.getcwd()}/mission_logs/'

# Extract the execution times for A* and RRT*
time_astar = None
time_rrtstar = None

# Construct the filenames based on the identifier (without the seconds)
# The filenames are derived by removing the last three characters from the identifier (removing the seconds)
filename_astar = f'mission_log_time_{identifier_astar[:-3]}.csv'
filename_rrtstar = f'mission_log_time_{identifier_rrtstar[:-3]}.csv'

# Define the path to the files
# The files are assumed to be in the same logging path directory
timefile_path_astar = os.path.join(logging_path_astar, filename_astar)
timefile_path_rrtstar = os.path.join(logging_path_rrtstar, filename_rrtstar)

# Read the execution time from the A* log
# The file is expected to have a single row with the format: "astar;0.4055"
with open(timefile_path_astar, 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        # The second element in the row contains the execution time in seconds
        time_astar = float(row[1])

# Read the execution time from the RRT* log
# The file is expected to have a single row with the format: "rrtstar;0.4055"
with open(timefile_path_rrtstar, 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        # The second element in the row contains the execution time in seconds
        time_rrtstar = float(row[1])

# Generate the comparison plot for execution times
# This plot will display a bar chart comparing the execution times of A* and RRT*
plt.figure()
bars = plt.bar(['A*', 'RRT*'], [time_astar, time_rrtstar], color=['blue', 'orange'])
plt.title('Comparison of Execution Times (in seconds [s])')
plt.ylabel('Time (seconds)')

# Add value labels on top of the bars for clarity
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), ha='center', va='bottom')

# Remove the Y-axis scale to make the chart cleaner and focus on the bar labels
plt.gca().get_yaxis().set_visible(False)

plt.show()

# Reading configuration logs for A* and RRT*
size_a, center_a, algo_a, target_a, note_a = pl.read_config(identifier_astar, logging_path_astar)
size_r, center_r, algo_r, target_r, note_r = pl.read_config(identifier_rrtstar, logging_path_rrtstar)

# Reading position logs for A* and RRT*
position_astar = pl.read_position(identifier_astar, logging_path_astar)
position_rrtstar = pl.read_position(identifier_rrtstar, logging_path_rrtstar)

# Converting positions from UTM to grid coordinates
grid_position_astar_x = []
grid_position_astar_y = []
for i in range(len(position_astar['x'])):
    utm_coordinate = [position_astar['x'][i], position_astar['y'][i]]
    grid_coordinate = cc.utm33_to_grid(utm_coordinate[0], utm_coordinate[1], size_a, center_a)
    grid_position_astar_x.append(grid_coordinate[0])
    grid_position_astar_y.append(grid_coordinate[1])

grid_position_rrtstar_x = []
grid_position_rrtstar_y = []
for i in range(len(position_rrtstar['x'])):
    utm_coordinate = [position_rrtstar['x'][i], position_rrtstar['y'][i]]
    grid_coordinate = cc.utm33_to_grid(utm_coordinate[0], utm_coordinate[1], size_r, center_r)
    grid_position_rrtstar_x.append(grid_coordinate[0])
    grid_position_rrtstar_y.append(grid_coordinate[1])

# Compare the number of positions traversed
num_positions_astar = len(grid_position_astar_x)
num_positions_rrtstar = len(grid_position_rrtstar_x)

plt.figure()
bars = plt.bar(['A*', 'RRT*'], [num_positions_astar, num_positions_rrtstar], color=['blue', 'orange'])
plt.title('Comparison of the number of positions traversed')
plt.ylabel('Number of positions')

# Add value labels on top of the bars for clarity
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), ha='center', va='bottom')

plt.show()

# Reading and converting waypoints for A* and RRT*
waypoints_astar = pl.read_waypoints(identifier_astar, logging_path_astar)
waypoints_rrtstar = pl.read_waypoints(identifier_rrtstar, logging_path_rrtstar)

grid_waypoints_astar_x = []
grid_waypoints_astar_y = []
for i in range(len(waypoints_astar['seq'])):
    if waypoints_astar['seq'][i] == 1:
        continue
    utm_coordinate = [waypoints_astar['x'][i], waypoints_astar['y'][i]]
    grid_coordinate = cc.utm33_to_grid(utm_coordinate[0], utm_coordinate[1], size_a, center_a)
    grid_waypoints_astar_x.append(grid_coordinate[0])
    grid_waypoints_astar_y.append(grid_coordinate[1])

grid_waypoints_rrtstar_x = []
grid_waypoints_rrtstar_y = []
for i in range(len(waypoints_rrtstar['seq'])):
    if waypoints_rrtstar['seq'][i] == 1:
        continue
    utm_coordinate = [waypoints_rrtstar['x'][i], waypoints_rrtstar['y'][i]]
    grid_coordinate = cc.utm33_to_grid(utm_coordinate[0], utm_coordinate[1], size_r, center_r)
    grid_waypoints_rrtstar_x.append(grid_coordinate[0])
    grid_waypoints_rrtstar_y.append(grid_coordinate[1])

# Compare the number of waypoints generated
num_waypoints_astar = len(grid_waypoints_astar_x)
num_waypoints_rrtstar = len(grid_waypoints_rrtstar_x)

plt.figure()
bars = plt.bar(['A*', 'RRT*'], [num_waypoints_astar, num_waypoints_rrtstar], color=['blue', 'orange'])
plt.title('Comparison of the number of waypoints generated')
plt.ylabel('Number of waypoints')

# Add value labels on top of the bars for clarity
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), ha='center', va='bottom')

plt.show()

# Verifying that the starting point is the same
# The first waypoint is always the start position (see log file structure)
start_position_astar = (grid_waypoints_astar_x[0], grid_waypoints_astar_y[0])
start_position_rrtstar = (grid_waypoints_rrtstar_x[0], grid_waypoints_rrtstar_y[0])

if start_position_astar != start_position_rrtstar:
    raise ValueError("The starting point differs between A* and RRT*")

# Add the functionality of 'new_custom_plotter.py' to overlay the paths of RRT* and A*

identifier = identifier_astar # Needed only to generate the background. Comparing with the same map using both RRT* and A*, it should generate the same thing
mapdata_path = f'{os.getcwd()}/map_data/'
setting_path = f'{os.getcwd()}/map_settings.yaml'
logging_path = f'{os.getcwd()}/mission_logs/'

# Reading Configuration Mission Log
size, center, algo, target, note = pl.read_config(identifier, logging_path)
center_enc = [center[0] + size[0]/2, center[1] + size[1]/2]

# Extracting ENC data to get accurate background
uf.configure_enc(setting_path, center_enc, size)
mp.extract_map_data(mapdata_path, center, new_data=True)
land_grid, coords  = mp.occupancy_grid_map(mapdata_path, size, buffer_size=1, visualize=False, saveas='occupancy_grid', landshore='land')
shore_grid, coords = mp.occupancy_grid_map(mapdata_path, size, buffer_size=1, visualize=False, saveas='occupancy_grid', landshore='shore')

# It is necessary to rotate grids to match up with reality
land_grid_rotated = np.rot90(np.flip(np.array(land_grid), 0), 3)
shore_grid_rotated = np.rot90(np.flip(np.array(shore_grid), 0), 3)

# Defining the occupancy grids as the background image
backdrop = np.add(land_grid_rotated, shore_grid_rotated)
color_map = {0:'steelblue', 1:'skyblue', 2:'black'}
plt.imshow(backdrop, cmap=plt.cm.colors.ListedColormap([color_map[i] for i in sorted(color_map.keys())]))

# Plotting the RRT* and A* paths
plt.plot(grid_position_rrtstar_x, grid_position_rrtstar_y, markersize=12, linewidth=3, c='limegreen', alpha=0.75, label='RRT* Path')
plt.plot(grid_position_astar_x, grid_position_astar_y, markersize=12, linewidth=3, c='purple', alpha=0.75, label='A* Path')

# Highlighting all waypoints/position readings
plt.scatter(grid_waypoints_rrtstar_x, grid_waypoints_rrtstar_y, s=40, c='orange',  edgecolors='black', linewidths=1, label='Waypoints RRT*', zorder=2)
plt.scatter(grid_waypoints_astar_x, grid_waypoints_astar_y, s=40, c='white',  edgecolors='black', linewidths=1, label='Waypoints A*', zorder=2)

# Highlighting the start and end points for RRT* and A*
plt.scatter(grid_position_rrtstar_x[0], grid_position_rrtstar_y[0], s=50, c='limegreen', edgecolors='black', linewidths=1, label='RRT* Start', zorder=3)
plt.scatter(grid_position_rrtstar_x[-1], grid_position_rrtstar_y[-1], s=50, c='red', edgecolors='black', linewidths=1, label='RRT* End', zorder=3)
plt.scatter(grid_position_astar_x[0], grid_position_astar_y[0], s=50, c='purple', edgecolors='black', linewidths=1, label='A* Start', zorder=3)
plt.scatter(grid_position_astar_x[-1], grid_position_astar_y[-1], s=50, c='blue', edgecolors='black', linewidths=1, label='A* End', zorder=3)

plt.legend()
plt.title(f'Global Path Planner: RRT* and A*')

plt.xlabel('Meters from ENC center')
plt.ylabel('Meters from ENC center')

plt.show()
plt.savefig("./data/%s.png" % 'plot_combined_rrt_astar', dpi=300, bbox_inches='tight', pad_inches=0)
plt.close()