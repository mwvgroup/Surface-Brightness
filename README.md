# Calculating UV Surface Brightness of 1kpc Radius Region around Supernova

####Code Overview / use:

[Surface Brightness (Photometry).ipynb] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Surface%20Brightness.ipynb) calculates the UV surface brightness of supernova environments using data from GALEX. The code begins by walking through a directory and building a list of .fits files containing a user specified keyword. After compiling this list, the script uses a .reg file to build a dictionary of redshifts and coordinates for each supernova of interest. It uses these coordinates to check each of the .fits files for an observed supernova and performs photometry using the [photutils package] (http://photutils.readthedocs.io/en/latest/) with a 1 kpc radius aperture. The code uses the keywords 'nd-int' or 'fd-int' by default, corresponding to int type files observed in the near and far UV respectively. For an outline of different file types, GALEX maintains a list of file naming conventions [here](http://galex.stsci.edu/gr6/?page=ddfaq).Before running the code, set the value of the following parameters located after the comment `#User set parameters`:

* region_file: The file path of a .reg file containing the names, locations, and redshifts for each supernova of interest.

* output_file: The file path where the generated table should be written to. This path should not end with any extension.

* fits_directory: The directory containing the .fits files you want to calculate surface brightness from. The script will automatically search through all sub directories as well. To change this behavior, alter the code following the comment "#We create a list of .fits files to perform photometry on"

* uv_type: Set this object equal to 'nuv' or 'fuv' so that the code can set the remainder of the necessary parameters automatically.
	
The following parameters are automatically set depending on the value of uv_type:

* file_key: A string which can be used to identify which files in fits_directory you want to perform photometry on. Files without file key in their name will not be analyzed.

* check_file_key: When the script needs to perform photometry on a check file, it will use the file path of the primary .fits file, but replace file_key with the string check_file_key

* flux_conv: A conversion factor from pixel count to flux. This value is given [by Galex] (http://asd.gsfc.nasa.gov/archive/galex/FAQ/counts_background.html) and is different for far and near UV observations. 

The int type .fits files used in this project contain a circular collection of pixels corresponding to the observing telescope's field of view. All pixels outside this field of view are assigned a value of 0 ([here is an example image] (https://github.com/mwvgroup/Surface-Brightness/blob/master/ds9.jpg)). If the photometry process returns 0, there is no immediate way of knowing if the corresponding supernova (and by extension the photometry aperture) is within the field of view. For such cases the script will perform photometry on a secondary check file. By default, the check file used is a wt type .fits where zero valued pixels only occur outside the field of view. If the performing photometry on the check file yields a non-zero value, then the aperture is within the telescopes field of view.

Using the photometry results, the corresponding flux, luminosity, and surface brightness values are calculated and written to a .csv file. For each supernova region, only the value with the smallest error is written to this file. The script will also create a .csv file listing int type files that are either missing wt type check files, or do not have a supernova in their field of view. The third file generated by the code is a logarithmic plot of the surface brightness values versus redshift. A step by step outline of how the code works is commented within the .ipynd file. Instructions on how to get the script running are listed below.

####Code Use:



####Repository File List:

* Friedman data table.csv: A table listing supernova considered in [Friedman 2015] (http://arxiv.org/abs/1408.0465).

* observed_target_info.reg: A region file containing a collection of supernova not considered in Friedman 2015, along with their redshift and location.

* output NUV/FUV.csv: A .csv file containing numerical results generated by the Surface Brightness.ipynb. The .fits files used to generate this file are not included in the repository.

* output NUV/FUV plot.pdf: A plot of the values from Output NUV/FUV.csv showing surface brightness verses the redshift on a logarithmic scale.

* Friedman NUV/FUV plot.pdf: A plot of the values from Output NUV/FUV.csv showing surface brightness verses the redshift on a logarithmic scale. This plot only shows supernova from Friedman 2015.

* output NUV/FUV log.csv: A list of int type files that are either missing wt type check files, or do not have a supernova in their field of view.
