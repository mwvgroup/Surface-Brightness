# Calculating UV Surface Brightness of 1 kpc Radius Region from a .fits File

####Code Summary:

The script [Surface Brightness (Photometry).ipynb] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Photometry/Surface%20Brightness%20(Photometry).ipynb) begins by walking through a specified directory and building a list of .fits files containing a user specified keyword. An example of such keywords are 'nd-int' or 'fd-int', which distinguish between observations in the near or far UV respectively. For an outline of possible keywords, GALEX mantains a list of file naming conventions [here](http://galex.stsci.edu/gr6/?page=ddfaq). After compiling this list, the script uses a .reg file to build a dictionary of redshifts and coordinates for each supernova of interest. It uses these coordinates to check each of the .fits files for an observed supernova and performs photometry using the [photutils package] (http://photutils.readthedocs.io/en/latest/) with a 1 kpc radius aperture. 

The primary .fits files used in this project are int type files, outlined in the GALEX naming conventions. These files contain a circular collection of pixels corresponding to the observing telescope's field of view. All pixels outside the field of view are automatically assigned the value 0 ([here is an example image] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Photometry/ds9.jpg), where black pixels represent the value 0). If the photometry process returns 0, this means there is no immediate way of knowing if the corresponding supernova (and by extension the photometry aperture) is within the field of view. In such a case the script will perform photometry on a secondary check file. This check file is a wt type .fits file that contains the same field of view, but is masked so that zero valued pixels only occure outside the field of view.

After performing photometry on all of the .fits files, the corresponding flux, luminosity, and surface brightness values are calculated and written to an output file.  A step by step outline of how the code works is commented within the .ipynd file. Instructions on how to get the script running are listed in the next section.

####Code Use:

Before using the code it is necessary to set the value of certain parameters. For convenience these are located at the beginning of the script and notated in the comments. These parameters include the following:

* region_file: The file path of the .reg file containing a name, location, and redshift for each supernova of interest.

* output_file: The file path were the generated table should be written to. This path should end with 'filename.csv'.

* fits_directory: The directory contain the .fits files you want to calculate surface brightness from. The script will automatically search through all sub directories as well. To change this behavior alter the code following the comment "#We create a list of .fits files to perform photometry on"

* file_key: A string which can be used to identify which files in fits_directory you want to calculate surface brightness on. Files without file_key in their name will not be analyzed. To include all files set this equal to ''.

* check_file_key: When the script needs to perform photometry on a check file, it will use the file path of the primary .fits file, but replace file_key with the string file_key

* flux_conv: A conversion factor from pixel count to flux. This value is given [here] (http://asd.gsfc.nasa.gov/archive/galex/FAQ/counts_background.html).

####Current Goals / Issues:

3. For certain table columns in the output file, the header is missing appropriate units

4. I need to finish downloading all of the check files so photometry can be run. 
