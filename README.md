# Calculating UV Surface Brightness of 1kpc Radius Region around Supernova

####Project Summary:

This repository contains two versions of a python3 script for calculating the UV surface brightness of a 1kpc radius region. Each version is contained in its own folder with its own, more detailed readme file. The csv folder contains an earlier version of the script that calculates results based on values from a .csv file, while the script in the Photometry folder uses a .reg file to perform photometry on a directory of .fits files. 
  
**To calculate surface brightness from spreadsheet values**, use the script located in 'Surface-Brightness/csv'. This script is an earlier version of the project. It requires an input .csv file containing the redshift, counts per second values, and exposure times for each supernova of interest. It is designed to use the counts per second value of a single pixel from a .fits file. With some work, however, it can be modified to use photometric values instead. For more information, see 'Surface-Brightness/csv/README_csv.md'
  
**To calculate surface brightness from a .fits file**, use the script located in 'Surface-Brightness/Photometry'. This is a newer version of the script that uses values from a .reg file to locate supernova within a collection of .fits files. If it locates a supernova in any .fits files contained in a specified directory, it will perform photometry using the photutils package and calculate surface brightness

