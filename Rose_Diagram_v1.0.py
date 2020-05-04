# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:21:27 2020

@author: Xiaofan Hu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math
import mplstereonet

points_headers = ['Datetime', 'EventID', 't0', 'X', 'Y', 'Z', 'Magnitude']

# Load data
df_stg7 = pd.read_csv(r'D:\Study\Microseismic\Project\Rose_Diagram_Analysis\Data\2015HOU0098_NNE_MIP_3H_Stg07.csv', skiprows=4, header=None, names=points_headers)

num_event = 20 # Number of events
num_gap = 5 # Number of gaps
strikes = []

for index, row in df_stg7.iterrows():
    if index + num_event <= df_stg7.shape[0]:
        sub_df = df_stg7.loc[index:(index+num_event)]
        slope, intercept, r_value, p_value, std_err = linregress(sub_df['X'], sub_df['Y'])
        degree = math.atan(slope) * 180 / math.pi
        strikes.append(degree)

plt.plot(strikes)
plt.ylabel('some numbers')
plt.show()

dips = [float(90)] * (len(strikes))

bin_edges = np.arange(-5, 366, 10)
number_of_strikes, bin_edges = np.histogram(strikes, bin_edges)

# Sum the last value with the first value.

number_of_strikes[0] += number_of_strikes[-1]

# Sum the first half 0-180° with the second half 180-360° to achieve the "mirrored behavior" of Rose Diagrams.

half = np.sum(np.split(number_of_strikes[:-1], 2), 0)
two_halves = np.concatenate([half, half])

# Create the rose diagram.

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, projection='polar')

ax.bar(np.deg2rad(np.arange(0, 360, 10)), two_halves, 
       width=np.deg2rad(10), bottom=0.0, color='red', edgecolor='k')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_thetagrids(np.arange(0, 360, 10), labels=np.arange(0, 360, 10))
ax.set_rgrids(np.arange(0, two_halves.max() + 1, 10), angle=0, weight= 'black')
ax.set_title('Rose Diagram of the "Microseismic Events"', y=1.10, fontsize=15)

fig.tight_layout()