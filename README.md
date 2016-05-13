# Calculating UV Surface Brightness of 1kpc Radius Region around Supernova

####Project Summary:

This repository contains two versions of a script for calculating the UV surface brightness of a 1kpc radius region. Each version is contained in its own folder and has its own, more detailed, readme file. The csv folder contains an earlier version of the script that calculates results based on values from a .csv file, while the script in the Photometry folder uses a .reg file to calculate values from multiple .fits files. 
  
####Script Usage:
  
To calculate surface brightness from spreadsheet values, use the script located in 'Surface-Brightness/csv'. This script is an earlier version that requires an input .csv file containing the redshift, counts per second values, and exposure times for each supernova of interest. It is designed to use counts per second values for a single pixel, but can be modified to use photometric values instead. For more information, see 'Surface-Brightness/csv/README_csv.md'
  
To calculate surface brightness from a .fits file, use the script located in 'Surface-Brightness/Photometry'. This is a newer version of the script that uses values from a .reg file to locate supernova within a .fits file. 
  
  
####Words of Caution /  Todo:

1. The error propagation in the photometry script is not correct. I believe all other calculations to be fine.

2. A readme file for the photometry script is on its way
