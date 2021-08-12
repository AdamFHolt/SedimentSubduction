#!/usr/bin/env python 
import sys
import numpy
import numpy, scipy, scipy.special

# box dimensions (i.e. "extent" in ASPECT input)
xmin=0;xmax=11600.e3;
ymin=0;ymax=2900.e3;
# number of cells, (i.e. "number of repetitions" in ASPECT input)
xnum=5800
ynum=1450

x_gap = 1550.e3; 
x_SP  = 6000.e3; 
y_crust = 7.5e3; 
radius_notch = 200e3;  # radius of curvature of lithosphere center-line
depth_notch  = 200e3;
depth_notch_core  = 170e3;
radius_outer = 245e3;
slab_dip = 70.;
OPthick = 150.e3;

age_ma=80;    # subucting plate age [Ma]
age=age_ma*1e6*365*24*60*60;
ridge_extent = 1000.e3; # length of subducting plate that is a "ridge"
k = 1e-6      # thermal diffusivity (for half-space cooling)
Tmax = 1573.; Tmin = 273.; # min/max temperatures


No_nodes= (xnum + 1) * (ynum + 1)
C=numpy.zeros([No_nodes,5],float)
 
ind=0

for j in range(ynum + 1): 
	for i in range(xnum + 1):

		x = xmin + i * ((xmax - xmin)/xnum)
		y = ymin + j * ((ymax - ymin)/ynum) 

		C[ind,0] = x
		C[ind,1] = y

		# Crust
		if x > (x_gap) and x <= (x_gap + x_SP - radius_outer) and y > (ymax - y_crust):
			C[ind,2]=1
		elif x > (x_gap + x_SP - radius_outer) and x < (x_gap + x_SP):
			x1 = x_gap + x_SP - radius_outer; 
			y1 = ymax - radius_outer;
			if ((x-x1)**2 + (y-y1)**2) < radius_outer**2 and ((x-x1)**2 + (y-y1)**2) >= (radius_outer-y_crust)**2 and y > (ymax - depth_notch): 
				angle=numpy.arctan((y-y1)/(x-x1));
				if angle > numpy.radians(90. - slab_dip):
				   C[ind,2]=1

		# OP
		if x > (x_gap + x_SP - radius_outer) and x < (x_gap + x_SP):
			x1 = x_gap + x_SP - radius_outer; 
			y1 = ymax - radius_outer;
			if ((x-x1)**2 + (y-y1)**2) >= radius_outer**2 and y > (ymax - OPthick): 
				C[ind,3]= 1
		if  x >= (x_gap + x_SP) and x < (xmax - x_gap) and y > (ymax - OPthick): 
				C[ind,3]= 1

		# slab tracers
		if C[ind,2] != 1 and C[ind,3] != 1:

			if x > (x_gap + ridge_extent) and x <= (x_gap + x_SP - radius_outer):
				if y > (ymax - 47.5e3) and y <= (ymax - 35.e3):
					C[ind,4] = 1
			if x > (x_gap + x_SP - radius_outer) and x < (x_gap + x_SP):
				x1 = x_gap + x_SP - radius_outer;
				y1 = ymax - radius_outer;
				if ((x-x1)**2 + (y-y1)**2) > (radius_outer - 47.5e3)**2 and ((x-x1)**2 + (y-y1)**2) <= (radius_outer - 35.e3)**2 and y > (ymax - depth_notch_core):
					angle=numpy.arctan((y-y1)/(x-x1));
					if angle > numpy.radians(90. - slab_dip):
						C[ind,4] = 1

		ind=ind+1;

# write to file
f= open("text_files/compnotch_thick7.5km_SedSubdTest_OneCrustType_ThickContOPSPThinCore.txt","w+")
f.write("# POINTS: %s %s\n" % (str(xnum+1),str(ynum+1)))
f.write("# Columns: x y comoosition1 composition2 composition3 composition4\n")
for k in range(0,ind):
	f.write("%.6f %.6f %.6f %.6f %.6f\n" % (C[k,0],C[k,1],C[k,2],C[k,3],C[k,4]))
f.close() 

