# Calculating UV Surface Brightness of 1 kpc Radius Region from a .fits File

####Code Summary:

The script [Surface Brightness (Photometry).ipynb] (https://github.com/mwvgroup/Surface-Brightness/blob/master/Photometry/Surface%20Brightness%20(Photometry).ipynb) begins by walking through a specified directory and its subdirectories. It collects a list of all the .fits files it encounters provided they contain a keyword specified by the user. An example of such keywords are 'nd' or 'fd' to distinguish between fits files observed in the near or far UV respectively. After compiling this list it uses a user specified .reg file to build a dictionary of redshifts and coordinates for each supernova of interest. The script uses these coordinates to check each .fits file if there is an observed supernova. If a supernova is found the [photutils package] (http://photutils.readthedocs.io/en/latest/) is used to perform photometry at the location of the supernova. The photometry process, however, is only semi-automated and requires some user input.

The .fits files used in this project contain a circular collection of pixels corresponding to the observing telescopes field of view. An example is shown in [this will be an example image] (), where black pixels represent the value 0. All pixels outside the field of view are automatically assigned the value 0. This means if the photometry process returns 0, there is no immediate way of knowing if the corresponding supernova is within the field of view. To avoid calculating photometry outside the field of view, the script will check if the supernova coordinates fall on the .fits image and whether or not a the 400 pixel area surrounding the location has any nonzero pixels. If these tests are inconclusive the script will display the .fits image along with the aperture location and ask the user to decide ([this will be an example image] ()). Entering 'no' (or anything containing an 'n') means the aperture is not in the field of view, while any other entry is taken as a yes.

After performing photometry on all of the files, the corresponding flux, luminosity, and surface brightness are calculated and written to an output file. The error in each value is also calculated, but **the current version of the script does not determine error correctly**.

####Code Use:

####Current goals / issues:

1. The running of photometry and calculation of values uses multiple loops. I would like to simplify the script so that less loops are used and running is hopefully decreased.

2. I can see no better alternative to asdf

2. The error propagation used in the script is incorrect. The first sign of this is that photutils sometimes generates an error that is larger that the reported photometry value

3. For certain table columns in the output file, the header is missing appropriate units
