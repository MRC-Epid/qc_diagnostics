# QUALITY CONTROL ANALYSIS SCRIPT (STANDALONE)
# Copyright (C) 2019  MRC Epidemiology Unit, University of Cambridge
#   
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
#   
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

version = "v.1.0 09/05/2019"

###############################################################################################################

import numpy as np
from datetime import datetime, timedelta
import time
import sys, os
from pampro import data_loading, diagnostics, Time_Series, Channel, hdf5, channel_inference, Bout, Bout_Collection, batch_processing, triaxial_calibration, time_utilities, pampro_utilities, pampro_fourier
from collections import OrderedDict
import collections, re, copy
import json
import pandas as pd

################################################################################################################
# SETTINGS
################################################################################################################

# FOLDER & FILE SETTINGS
filetype = "Axivity"            # raw data file filetype ("GeneActiv" or "Axivity")

job_file_path = ""              # location of csv job file
charts_folder = ""              # location for plots (if required, else leave as "")
results_folder = ""             # location for meta results
anomalies_folder = ""           # location for anomaly records

# PROCESSING SETTINGS AND THRESHOLDS
Processing_epoch = 5            # processing epoch, in seconds, used for generating sample number statistic
noise_cutoff_mg = 13            # noise threshold in mg
discharge_hours = 24            # number of hours for the examination of the battery discharge rate
discharge_pct = 25              # maximum percentage of battery charge that can be discharged in "discharge_hours" without warning flag
battery_minimum = 10            # minimum percentage of battery charge, below which warning flag is triggered
axis_max = 1.2                    # upper threshold for each acceleration axis, above which there is an anomaly for that axis
axis_min = -1.2                    # lower threshold for each acceleration axis, below which there is an anomaly for that axis

# PLOTTING SETTINGS
PLOT = "YES"                    # Choose whether to produce plots, or not ("YES" or "NO")
enmo_max = 10000                # maximum value of enmo channel, for plotting (i.e. maximum value of the y-axis)
GA_battery_max = 4.3            # maximum value of GeneActiv battery, used to find percentage charged
AX_battery_max = 210            # maximum value of Axivity battery, used to find percentage charged

##################################################################################################################
# SCRIPT BEGINS BELOW
##################################################################################################################

job_num = int(sys.argv[1])
num_jobs = int(sys.argv[2])

# create a dataframe of the channels, channel minimum and maximum values to be plotted
channels_info = {'channel_name': ["ENMO", "Battery_percentage"],
                 'channel_min': [0,0],
                 'channel_max': [enmo_max, 100]}
plotting_df = pd.DataFrame.from_dict(channels_info)

# create a dictionary of statistics
stats = OrderedDict()           
stats["ENMO"] = [("generic", ["mean", "n", "missing", "sum"])]
stats["Battery"] = [("generic", ["mean"])]

anomaly_types = ["A", "B", "C", "D", "E", "F", "G"]     # A list of known anomaly types identified by pampro

def qc_analysis(job_details):

    id_num = str(job_details["pid"])
    filename = job_details["filename"]

    filename_short = os.path.basename(filename).split('.')[0]

    battery_max = 0
    if filetype == "GeneActiv":
        battery_max = GA_battery_max
    elif filetype == "Axivity":
        battery_max = AX_battery_max

    # Load the data from the hdf5 file
    ts, header = data_loading.fast_load(filename, filetype)

    header["QC_filename"] = os.path.basename(filename)

    x, y, z, battery, temperature = ts.get_channels(["X", "Y", "Z", "Battery", "Temperature"])
    
    # create a channel of battery percentage, based on the assumed battery maximum value 
    battery_pct = Channel.Channel.clone(battery)
    battery_pct.data = (battery.data / battery_max) * 100
    
    channels = [x, y, z, battery, temperature, battery_pct]
    
    anomalies = diagnostics.diagnose_fix_anomalies(channels, discrepancy_threshold=2)

    # create dictionary of anomalies types
    anomalies_dict = dict()
                        
    # check whether any anomalies have been found:
    if len(anomalies) > 0:
        anomalies_file = os.path.join(anomalies_folder, "{}_anomalies.csv".format(filename_short))
        df = pd.DataFrame(anomalies)
        
        for type in anomaly_types:
            anomalies_dict["QC_anomaly_{}".format(type)] = (df.anomaly_type.values == type).sum()
        
        df = df.set_index("anomaly_type")
        # print record of anomalies to anomalies_file
        df.to_csv(anomalies_file)
        
    else:
        for type in anomaly_types:
            anomalies_dict["QC_anomaly_{}".format(type)] = 0
        
    # check for axis anomalies
    axes_dict = diagnostics.diagnose_axes(x, y, z, noise_cutoff_mg=13)
    
    axis_anomaly = False
    
    for key, val in axes_dict.items():
        anomalies_dict["QC_{}".format(key)] = val
        if key.endswith("max"):
            if val > axis_max:
                axis_anomaly = True
        elif key.endswith("min"):
            if val < axis_min:
                axis_anomaly = True

    # create a "check battery" flag:
    check_battery = False

    # calculate first and last battery percentages
    first_battery_pct = round((battery_pct.data[1]),2)
    last_battery_pct = round((battery_pct.data[-1]),2)
    header["QC_first_battery_pct"] = first_battery_pct
    header["QC_last_battery_pct"] = last_battery_pct
    
    # calculate lowest battery percentage
    # check if battery.pct has a missing_value, exclude those values if they exist
    if battery_pct.missing_value == "None":
        lowest_battery_pct = min(battery_pct.data)
    else:
        test_array = np.delete(battery_pct.data, np.where(battery_pct.data == battery_pct.missing_value))
        lowest_battery_pct = min(test_array)
    
    header["QC_lowest_battery_pct"] = round(lowest_battery_pct,2)
    header["QC_lowest_battery_threshold"] = battery_minimum
        
    # find the maximum battery discharge in any 24hr period:    
    max_discharge = battery_pct.channel_max_decrease(time_period=timedelta(hours=discharge_hours))
    header["QC_max_discharge"] = round(max_discharge, 2)
    header["QC_discharge_time_period"] = "{} hours".format(discharge_hours)
    header["QC_discharge_threshold"] = discharge_pct

    # change flag if lowest battery percentage dips below battery_minimum at any point 
    # OR maximum discharge greater than discharge_pct over time period "hours = discharge_hours"
    if lowest_battery_pct < battery_minimum or max_discharge > discharge_pct:
        check_battery = True
        
    header["QC_check_battery"] = str(check_battery)
    header["QC_axis_anomaly"] = str(axis_anomaly)

    # Calculate the time frame to use
    start = time_utilities.start_of_day(x.timeframe[0])
    end = time_utilities.end_of_day(x.timeframe[-1])
    tp = (start, end)

    results_ts = Time_Series.Time_Series("")

    # Derive some signal features
    vm = channel_inference.infer_vector_magnitude(x, y, z)
    enmo = channel_inference.infer_enmo(vm)
    enmo.minimum = 0
    enmo.maximum = enmo_max

    # Infer nonwear
    nonwear_bouts = channel_inference.infer_nonwear_for_qc(x, y, z, noise_cutoff_mg=noise_cutoff_mg)
    # Use nonwear bouts to calculate wear bouts
    wear_bouts = Bout.time_period_minus_bouts(enmo.timeframe, nonwear_bouts)

    # Use wear bouts to calculate the amount of wear time in the file in hours, save to meta data
    total_wear = Bout.total_time(wear_bouts)
    total_seconds_wear = total_wear.total_seconds()
    total_hours_wear = round(total_seconds_wear/3600)
    header["QC_total_hours_wear"] = total_hours_wear

    # Split the enmo channel into lists of bouts for each quadrant:
    ''' quadrant_0 = 00:00 -> 06: 00
        quadrant_1 = 06:00 -> 12: 00
        quadrant_2 = 12:00 -> 18: 00
        quadrant_3 = 18:00 -> 00: 00 '''
    q_0, q_1, q_2, q_3 = channel_inference.create_quadrant_bouts(enmo)

    # calculate the intersection of each set of bouts with wear_bouts, then calculate the wear time in each quadrant.
    sum_quadrant_wear = 0
    for quadrant, name1, name2 in ([q_0, "QC_hours_wear_quadrant_0", "QC_pct_wear_quadrant_0"],
                                   [q_1, "QC_hours_wear_quadrant_1", "QC_pct_wear_quadrant_1"],
                                   [q_2, "QC_hours_wear_quadrant_2", "QC_pct_wear_quadrant_2"],
                                   [q_3, "QC_hours_wear_quadrant_3", "QC_pct_wear_quadrant_3"]):
        quadrant_wear = Bout.bout_list_intersection(quadrant, wear_bouts)
        seconds_wear = Bout.total_time(quadrant_wear).total_seconds()
        hours_wear = round(seconds_wear / 3600)
        header[name1] = hours_wear
        header[name2] = round(((hours_wear / total_hours_wear) * 100), 2)

    for bout in nonwear_bouts:
        # Show non-wear bouts in purple
        bout.draw_properties = {'lw': 0, 'alpha': 0.75, 'facecolor': '#764af9'}

    for channel, channel_name in zip([enmo, battery_pct],["ENMO", "Battery_percentage"]):
        channel.name = channel_name
        results_ts.add_channel(channel)

    if PLOT == "YES":    
        # Plot statistics as subplots in one plot file per data file
        results_ts["ENMO"].add_annotations(nonwear_bouts)
        results_ts.draw_qc(plotting_df, file_target=os.path.join(charts_folder,"{}_plots.png".format(filename_short)))

    header["QC_script"] = version
    
    # file of metadata from qc process
    qc_output = os.path.join(results_folder, "qc_meta_{}.csv".format(filename_short))
    # check if qc_output already exists...
    if os.path.isfile(qc_output):
        os.remove(qc_output)
    
    metadata = {**header, **anomalies_dict}
    
    # write metadata to file
    pampro_utilities.dict_write(qc_output, id_num, metadata)

    for c in ts:
        del c.data
        del c.timestamps
        del c.indices
        del c.cached_indices

batch_processing.batch_process(qc_analysis, job_file_path, job_num, num_jobs, task="qc_diagnostics")