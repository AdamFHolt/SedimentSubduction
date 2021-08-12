## OVERVIEW

Contains the thermo-mechanical subduction models presented in Behr et al. (submitted to Geophys. J. Int.). All models were ran using ASPECT version 2.1.0 with the addition of a rheology plugin (contained here). 
To summarize the folder contents:

**input_files:**  Contains all ASPECT input (.prm) files used in the study:
-- more details to be added

**input_geometries:** Contains Python scripts used to create the initial conditions of the models as .txt files. 
-- more details to be added 

**plugin:** Contains the source code of the rheology plugin: visco_plastic_mod. This is a modified version of the original visco_plastic rheology module. Main modifications: a simplified diffusion/dislocation creep flow law (with options to switch one component off in the lower mantle), an additional plasticity formulation (Byerlee-type yielding), options to cut off the crustal viscosity/density component at a specified depth (or taper out between two depths).

## REFERENCES

**Main study reference:**

Behr, W.M., Holt, A.F., Becker, T.W., and Faccenna, C. The effects of plate interface rheology on subduction kinematics and dynamics. Submitted to Geophysical Journal International.

**ASPECT references:**

Martin Kronbichler, Timo Heister, and Wolfgang Bangerth. 2012. “High Accuracy Mantle Convection Simulation through Modern Numerical Methods.” Geophysical Journal International 191 (1) (August 21): 12–29. doi:10.1111/j.1365-246x.2012.05609.x. http://dx.doi.org/10.1111/j.1365-246X.2012.05609.x.

Timo Heister, Juliane Dannberg, Rene Gassmöller, and Wolfgang Bangerth. 2017. “High Accuracy Mantle Convection Simulation through Modern Numerical Methods – II: Realistic Models and Problems.” Geophysical Journal International 210 (2) (May 9): 833–851. doi:10.1093/gji/ggx195. http://dx.doi.org/10.1093/gji/ggx195.

Wolfgang Bangerth, Juliane Dannberg, Rene Gassmoeller, and Timo Heister. 2020. ASPECT v2.1.0. (version v2.1.0). Zenodo. https://doi.org/10.5281/zenodo.2653531

Wolfgang Bangerth, Juliane Dannberg, Rene Gassmoeller, Timo Heister, and others. 2020. ASPECT: Advanced Solver for Problems in Earth's ConvecTion, User Manual. <i>Figshare</i>. https://doi.org/10.6084/m9.figshare.486533
