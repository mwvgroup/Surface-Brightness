# Calculating Near and Far UV Surface Brightness for Local Environments of Supernovae


### Project Description:

Using observations from [Galex] (http://galex.stsci.edu/) in the near and far UV, we calculate the surface brightness of regions surrounding individual supernovae. The surface brightness of a 5kpc radius region is also calculated for comparison with [Kelly et al. 2015] (http://arxiv.org/abs/1410.0961). Results are found by using the [photutils package] (http://photutils.readthedocs.io/en/latest/) to perform photometry on [int type] (http://galex.stsci.edu/gr6/?page=ddfaq) .fits files published by Galex. 

### Code Overview:

##### The surface brightness class

Surface brightness values are calculated using the `surface_brightness` class from [surface_brightness.py] (https://github.com/mwvgroup/Surface-Brightness/blob/master/surface_brightness.py). The `surface_brightness` class can be initiated without any arguments, but it is recomended create an instance as

    brightness = surface_brightness(cord_dict, red_dict)


##### How to use it

To use the code, first set the value of parameters located after the comment `#User set parameters`. These parameters include:

* `region_file` : The file path of a .reg file containing the names, locations, and redshifts for each supernova of interest.

* `fits_directory` : A directory containing the .fits files used to calculate surface brightness. The script will automatically search through all sub directories. To change this behavior, alter the code following the comment `#We create a list of .fits files to perform photometry on`

* `output_file` : A keyword to be contained in the output file names.

##### How it works

The code begins by walking through the directory `fits_directory` and building a list of .fits files to be analyzed. Files are only added to this list if the filename contains either 'nd-int' or 'fd-int', distinguishing int type files with observations in the near and far UV respectively. After compiling the list, the script uses a .reg file to build a dictionary of redshifts and coordinates for each supernova of interest. The function `photometry` uses these coordinates to check each of the .fits files for an observed supernova and performs photometry using the [photutils package] (http://photutils.readthedocs.io/en/latest/).

The int type .fits files used in this project contain a circular collection of pixels corresponding to the observing telescope's field of view ([here is an example image] (https://github.com/mwvgroup/Surface-Brightness/blob/master/example.jpg)). All pixels outside this field of view are assigned a value of 0. If the photometry process returns 0, there is no immediate way of knowing if the corresponding supernova (and by extension the photometry aperture) is within the field of view. For such cases the script will use the function `zero_check` to perform photometry on a secondary check file. By default, the check file used is a wt type .fits file where zero valued pixels only occur outside the field of view. If performing photometry on the check file yields a non-zero value, then the aperture is deemed to be within the telescope's field of view.

Using the photometry results, the corresponding flux, luminosity, and surface brightness values are calculated and added to a table using the function `create_tables`. If more than one .fits file contains a given supernova, `create_tables` will only include the surface brightness value with the smallest error. `create_tables` is run four times to create tables for observations in the near and far UV using a 1kpc and 5kpc radius aperture. These tables are then combined and written to a single .csv file. The `create_tables` function will also create a table listing int type files that are either missing wt type check files, or do not have a supernova in their field of view. These tables are also combined and written to a .csv file. Using the 1kpc radius surface brightness values, the `create_plots` function is used to save logarithmic plots of surface brightness vs redshift to .pdf files. In total, four plots are saved corresponding to near or far UV surface brightness in units of (erg s-1 A-1 arcsec^-2) and (erg s-1 A-1 kpc^-2).

Comments are contained within the .ipynd file to provide a step by step outline on how the code works.

##### Calculating Surface brightness from Photometry values

Using the photometry value from a .fits file, the corresponding flux is given in (erg sec-1 cm-2 Å-1) by a conversion factor

    flux = flux_conv * photom 

This conversion factor is given by the [Galex website] (http://asd.gsfc.nasa.gov/archive/galex/FAQ/counts_background.html) as  2.06 x 10-16 for near UV observations and 1.40 x 10-15 for the far UV. The Luminosity is given by the flux times the surface area. Using the WMAP9 cosmology,

    from astropy.cosmology import WMAP9 as cosmo
    
    ldist = cosmo.luminosity_distance(redshift).cgs.value
    lum = flux * 4 * np.pi * (ldist**2) 
    
To find surface brightness in the desired units, we then convert from units of kpc^-2 to armin^-2 and then from arcmin^-2 to arcsec^-2

    arcmin = cosmo.kpc_comoving_per_arcmin(redshift).value**2 
    sbrightness = lum * arcmin / 3600

### Repository File List:

* Friedman data table.csv: A table listing supernova considered in [Friedman 2015] (http://arxiv.org/abs/1408.0465).

* observed_target_info.reg: A region file containing a collection of supernova not considered in Friedman 2015, along with their redshift and location.

* output.csv: A .csv file containing numerical results generated by the Surface Brightness.ipynb. The .fits files used to generate this file are not included in the repository.

* NUV/FUV plot (arcsec).pdf: A logarithmic plot of the values from Output NUV/FUV.csv showing surface brightness in units of (erg s-1 A-1 arcsec^-2) verses the redshift. Surface brightness in these plots is calculated using a 1kpc radius aperture.

* NUV/FUV plot (arcsec).pdf: A logarithmic plot of the values from Output NUV/FUV.csv showing surface brightness in units of (erg s-1 A-1 arcsec^-2) verses the redshift. Surface brightness in these plots is calculated using a 1kpc radius aperture.

* output log.csv: A list of int type files and whether or not they missing wt type check files or do not have a supernova in their field of view.


### ToDo:

* doublecheck error propogation
* rewrite function descriptions
* check functionality