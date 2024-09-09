# Imports
import sys
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rnd
from scipy import stats as st
import math

def xs_act_avg_screen_time(xs_indiv):
     #replace -1 with NaN 
     aast_na = xs_indiv.actual_average_screen_time.replace(-1, np.nan)

     #initial histogram of data
     hist_data(aast_na,\
     "Actual Average Screen Time where Missing Values Are Excluded", "Excluded", "Excluded_AAST")
    
     #find mean, median, and one random value between 0-12
     aast_meanval = np.nanmean(aast_na)
     aast_medval = np.nanmedian(aast_na)
     aast_rval = 12*rnd.random()

     #create filled-in arrays and histograms
     aast_mean =  aast_na.replace(np.nan, aast_meanval)
     hist_data(aast_mean,\
     "Actual Average Screen Time where Missing Values Are Replaced by the Mean Value", "Mean", "Mean_AAST")
      
     aast_median = aast_na.replace(np.nan, aast_medval)
     hist_data(aast_median,\
     "Actual Average Screen Time where Missing Values Are Replaced by the Median Value", "Median", "Median_AAST")
     
     aast_rand = aast_na.replace(np.nan, aast_rval)
     hist_data(aast_rand,\
     "Actual Average Screen Time where Missing Values Are Replaced by a Random Value", "Random", "Random_AAST")

     aast_overlaid = [aast_na, aast_mean, aast_median, aast_rand]
     hist_data(aast_overlaid,\
     "Actual Average Screen Time with Multiple Missing Value Replacements",\
     ["Excluded", "Mean", "Median", "Random"], "Combined_AAST")
    
     #Perform t-test and retrieve t & p values
     t_mean, p_mean = t_test_aast(aast_mean)
     t_median, p_median = t_test_aast(aast_median)  
     t_rand, p_rand = t_test_aast(aast_rand)

def t_test_aast(aast_data):
     sample_data = np.random.normal(3.75, 1.25, 60)
     t,p = st.ttest_ind(aast_data, sample_data)
     #print(t,p)
     return(t,p)

def xs_prc_avg_screen_time(xs_indiv):
     #replace -1 with NaN 
     past_na = xs_indiv.perceived_average_screen_time.replace(-1, np.nan)
     aast_na = xs_indiv.actual_average_screen_time.replace(-1, np.nan)

     #initial histogram of data
     hist_data(past_na,\
     "Perceived Average Screen Time where Missing Values Are Excluded", "Excluded", "Excluded_PAST")
  
     #calculate intense users 
     intense_users, intense_cutoff = calc_intense_users(aast_na) 
       
     #Boolean arrays of data
     intense_users_bool = (aast_na > intense_cutoff)
     print(sum(intense_users_bool))
     missing_past = (xs_indiv.perceived_average_screen_time == -1)
     cont_table = pd.crosstab(missing_past, intense_users_bool)
     chi2, p, dof, exp = st.chi2_contingency(cont_table)
     #print(p)

def calc_intense_users(data):
     #calculate intense phone users
     intense_cutoff = np.std(data) + np.mean(data)
     intense_users = data[(data > intense_cutoff)]
     return intense_users, intense_cutoff
      
def hist_data(data, label, legend_label, file_name):
     #plot histogram 
     plt.hist(data)
     plt.title(label)
     plt.xlabel("# of Hours")
     plt.ylabel("# of Users")
     plt.legend(legend_label)
     plt.savefig(file_name + ".png")
     plt.close()

def location_v_battery(xs_sensor):
     for uuid in xs_sensor.keys():
          #get battery level and location columns, turn into bool arrays
          df = pd.DataFrame(xs_sensor.get(uuid))
          low_battery = df['lf_measurements:battery_level']
          low_battery_bool = (low_battery < 0.20)
          lat = df['location:raw_latitude']
          missing_lat = pd.isnull(lat)

          #calculate chi squared
          cont_table = pd.crosstab(missing_lat, low_battery_bool)
          chi2, p, dof, exp = st.chi2_contingency(cont_table, correction=True)
          if p < 0.05:
              print(uuid)
              #print(p)
              #print(cont_table[1][1])

def location_filling(xs_sensor):
     selected_uuid = 'F50235E0-DD67-4F2A-B00B-1F31ADA998B9'
     df = pd.DataFrame(xs_sensor.get(selected_uuid))
     lat = df['location:raw_latitude']
     ffill_lat = lat.fillna(method='ffill')
     bfill_lat = lat.fillna(method='bfill')
     interp_lat = lat.interpolate()
     plt.figure()
     plt.plot(lat, 'r')
     plt.plot(ffill_lat, 'c', alpha =0.8)
     plt.plot(bfill_lat, 'g', alpha = 0.6)
     plt.plot(interp_lat, 'y', alpha = 0.8)
     plt.title("Latitude, using various fill methods")
     plt.xlabel("Time (Minutes)")
     plt.ylabel("Latitude")
     plt.legend(["No Fill", "Forward Fill", "Back Fill", "Linear Interpolation"])
     plt.savefig("latitude.png")
     plt.close()

def main():
     """
     Main function
     
     :param:

     :return: None
     """
     
     #Unpickle files, create dicts
     xs_indiv_infile = open(xs_indiv_arg, 'rb')
     xs_sensor_infile = open(xs_sensor_arg, 'rb')
     xs_indiv = pickle.load(xs_indiv_infile)
     xs_sensor = pickle.load(xs_sensor_infile)

     #Graphing data (Actual v. Percieved Screen Time)
     xs_act_avg_screen_time(xs_indiv)
     xs_prc_avg_screen_time(xs_indiv)     
     
     #Location & Battery Tracking
     location_v_battery(xs_sensor)
     location_filling(xs_sensor)

if __name__ == '__main__':
     xs_indiv_arg = sys.argv[1]
     xs_sensor_arg = sys.argv[2]
     main()
