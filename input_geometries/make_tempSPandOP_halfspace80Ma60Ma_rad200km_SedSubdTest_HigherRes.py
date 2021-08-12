#!/usr/bin/env python 
#cp'd from make_tempSPandOP_halfspace80Ma25Ma_rad200km_BigBox_SmallerOP.py

import sys
import numpy as np
import scipy, scipy.special
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ioff()

output_name="tempSPandOP_halfspace80Ma60Ma_rad200km_SedSubdTest_HigherRes"

# box dimensions (i.e. "extent" in ASPECT input)
xmin=0;xmax=11600.e3;
ymin=0;ymax=2900.e3;
# number of input field points
xnum=5800
ynum=1450

# refinement in y-direction
ybound = 250.e3    # depth of refinement boundary
num_refine = 250  # number of grid points in refined (upper) layer
lower_lowres = np.linspace(0,ymax-ybound,ynum+1-num_refine)
upper_highres = np.linspace(ymax-ybound,ymax,1+num_refine)
yvals = np.concatenate((lower_lowres, upper_highres[1:]), axis=0)
print "lower vertical res = %.2f km" % ((yvals[1]-yvals[0])/1.e3)
print "higher vertical res = %.2f km" % ((yvals[ynum]-yvals[ynum-1])/1.e3)

# geometrical parameters
x_gap = 1550.e3;       # distance between plate edges and domain sides
x_SP  = 6000.e3;       # subducting plate length
depth_notch  = 200e3;  # initial slab depth
radius_outer = 245e3;  # initial slab radius of curvature
Tmax = 1573.; Tmin = 273.; # min/max temperatures
Tcutoff = 1325.;       # if T > Tcutoff, T = Tmax
slab_dip = 70.;

age_ma=80;    # subucting plate age [Ma]
age=age_ma*1e6*365*24*60*60;
age_op_ma=60; # upper plate age [Ma]
age_op=age_op_ma*1e6*365*24*60*60;
ridge_extent = 1000.e3; # length of subducting plate that is a "ridge"
k = 1e-6      # thermal diffusivity (for half-space cooling)

No_nodes= (xnum + 1) * (ynum + 1)
T=np.zeros([No_nodes,3],float)
 
ind=0
print "writting text file..."
for j in range(ynum + 1): 

        y = yvals[j]

	for i in range(xnum + 1):

		x = xmin + i * ((xmax - xmin)/xnum)
		#y = ymin + j * ((ymax - ymin)/ynum) 

		T[ind,0] = x
		T[ind,1] = y
		T[ind,2] = Tmax

		if x > (x_gap) and x <= (x_gap + ridge_extent):
			age_ridge = (x - x_gap) * (age/ridge_extent)
			erf_term=(ymax-y)/(2*np.sqrt(k*age_ridge))
			T[ind,2]='%.5f'  %   (Tmax - (Tmax - Tmin)*scipy.special.erfc(erf_term))
		elif x > (x_gap + ridge_extent) and x <= (x_gap + x_SP - radius_outer):
			erf_term=(ymax-y)/(2*np.sqrt(k*age))
			T[ind,2]='%.5f'  %   (Tmax - (Tmax - Tmin)*scipy.special.erfc(erf_term))
		elif x >= (x_gap + x_SP) and x < (xmax - x_gap):
			erf_term=(ymax-y)/(2*np.sqrt(k*age_op))
			T[ind,2]='%.5f'  %   (Tmax - (Tmax - Tmin)*scipy.special.erfc(erf_term))
				
		if x > (x_gap + x_SP - radius_outer) and x < (x_gap + x_SP):
			x1 = x_gap + x_SP - radius_outer; 
			y1 = ymax - radius_outer;
			if ((x-x1)**2 + (y-y1)**2) < radius_outer**2 and y > (ymax - depth_notch): 
				angle=np.arctan((y-y1)/(x-x1));
				if angle > np.radians(90. - slab_dip):
					ynotch = radius_outer - np.sqrt((x-x1)**2 + (y-y1)**2)
					erf_term=(ynotch)/(2*np.sqrt(k*age))
					T[ind,2]='%.5f'  %   (Tmax - (Tmax - Tmin)*scipy.special.erfc(erf_term))
			elif ((x-x1)**2 + (y-y1)**2) >= radius_outer**2 and y > (ymax - depth_notch): 
				erf_term=(ymax-y)/(2*np.sqrt(k*age_op))
				T[ind,2]='%.5f'  %   (Tmax - (Tmax - Tmin)*scipy.special.erfc(erf_term))

		if T[ind,2] > Tcutoff:
		   T[ind,2] = Tmax

		ind=ind+1;
 
# write to file
text_file_name=''.join(['text_files/',str(output_name),'.txt'])
f= open(text_file_name,"w+")
f.write("# POINTS: %s %s\n" % (str(xnum+1),str(ynum+1)))
f.write("# Columns: x y temperature\n")
for k in range(0,ind):
	f.write("%.6f %.6f %.6f\n" % (T[k,0],T[k,1],T[k,2]))
f.close() 
print "file written..."

