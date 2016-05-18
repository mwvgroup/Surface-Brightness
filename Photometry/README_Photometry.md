# Calculating UV Surface Brightness of 1 kpc Radius Region from a .fits File

####Code Summary:

The script [Surface Brightness (Photometry).ipynb] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Photometry/Surface%20Brightness%20(Photometry).ipynb) begins by walking through a specified directory and its subdirectories. It collects a list of all the .fits files it encounters provided they contain a keyword specified by the user. An example of such keywords are 'nd' or 'fd' to distinguish between .fits files observed in the near or far UV respectively. After compiling this list it uses a user specified .reg file to build a dictionary of redshifts and coordinates for each supernova of interest. The script uses these coordinates to check each .fits file if there is an observed supernova. If a supernova is found the [photutils package] (http://photutils.readthedocs.io/en/latest/) is used to perform photometry at the location of the supernova. The photometry process, however, is only semi-automated and requires some user input.

The .fits files used in this project contain a circular collection of pixels corresponding to the observing telescope's field of view ([this will be an example image] (), where black pixels represent the value 0). All pixels outside the field of view are automatically assigned the value 0. If the photometry process returns 0, this means there is no immediate way of knowing if the corresponding supernova (and by extension the photometry aperture) is within the field of view. To avoid calculating photometry outside the field of view, the script will check whether or not the supernova coordinates fall on the .fits image and if the 400 pixel area surrounding the supernova location has any nonzero pixels. If these tests are inconclusive, the script will display the .fits image along with the aperture location and ask the user to decide ([this will be an example image] ()). If the user responds with 'no' (or anything containing an 'n') means the aperture is not in the field of view, while any other entry is taken as a yes. 

After performing photometry on all of the .fits files, the corresponding flux, luminosity, and surface brightness values are calculated and written to an output file. The error in each value is also calculated, but **the current version of the script does not determine error correctly**. A step by step outline of how the code works is commented within the .ipynd file. Instructions on how to get the script running are listed in the next section.

####Code Use:

Before using the code it is necessary to set the value of certain parameters. For convenience these are located at the beginning of the script and notated in the comments. After this initial change the rest of the script can be run and will perform as described above. These parameters include the following:

* region_file: The file path of the .reg file containing a name, location, and redshift for each supernova of interest.

* output_file: The file path were the generated table should be written to. This path should end with 'filename.csv'.

* fits_directory: The directory contain the .fits files you want to calculate surface brightness from. The script will automatically search through all sub directories as well. To change this behavior alter the code following the comment "#We create a list of .fits files to perform photometry on"

* file_key: A string which can be used to identify which files in fits_directory you want to calculate surface brightness on. Files without file_key in their name will not be analyzed. To include all files set this equal to ''.

* flux_conv: A conversion factor from pixel count to flux. This value is given [here] (http://asd.gsfc.nasa.gov/archive/galex/FAQ/counts_background.html).

####Current Goals / Issues:

2. The error propagation used in the script is incorrect. The first sign of this is that photutils sometimes generates an error that is larger that the reported photometry value.

2. I can see no better alternative to determining whether or not apertures yielding the value zero lie within the field of view than having the user give the final say. While this is potentially annoying to the user, it yields the highest accuracy.

2. After resolving the above issues I want to go through the script and simplify some of the functionality, making the script more streamlined and "pythonic".

3. For certain table columns in the output file, the header is missing appropriate units

4. Double check the trim settings
