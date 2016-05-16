# Calculating UV Surface Brightness of 1kpc Radius Region around Supernova

###Project Summary:

The goal of this project is to calculate the surface brightness of a supernova's local enviornment in the UV. This repository contains two versions of a python3 script used for calculating the surface brightness of a 1kpc radius region. Each version is contained in its own folder with its own, more detailed readme file. The csv folder contains an earlier version of the script that calculates results based on values from a .csv file, while the script in the Photometry folder uses a .reg file to perform photometry on a directory of .fits files. 
  
#####To calculate surface brightness from spreadsheet values: 

Use the script located in 'Surface-Brightness/csv'. This script is an earlier version of the project. It requires an input .csv file containing the redshift, average photon counts per second, and exposure times for each supernova of interest. The script is designed to use the counts per second value of a single pixel that has been manually pulled from a .fits file. With some work, however, it can be modified to use photometric values instead. For more information see 'Surface-Brightness/csv/README_csv.md'
  
#####To calculate surface brightness from a .fits file: 

Use the script located in 'Surface-Brightness/Photometry'. This is a newer version of the script that is much more automated. When given a directory of .fits files, it uses the coordiantes from a .reg file to see if there are any observed supernova in each .fits file. If it locates a supernova it will perform photometry using the [photutils package] (http://photutils.readthedocs.io/en/latest/) and use the resulting value to calculate surface brightness. For more information see [Surface-Brightness/csv/README_Photometry.md] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Photometry/README_Photometry.md)

