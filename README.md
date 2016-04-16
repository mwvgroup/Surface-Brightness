# Calculating the Surface Brightness of Supernova

####Description of Code:

This script uses input values from the file 'GALEX flux.csv' to determine the surface brightness of a supernova's local enviornment. The input file contains a list of super nova, the redshift of their enviornment's, their observed average photon counts per second, and the corresponding exposure time. The script referances information from the input file by column number (indexed at zero). Because of this it is necessary to properly specify what column number corresponds to what value. For example, collumn 1 may correspod to redshift values while collumn 2 may contain average photon counts per second. These parameters are pointed out in comments toward the beginning of the script.

In the case where the input file has no value for counts per second, the script will treat it as 'nan' and report it as such in the output file. A detailed outline of how the code works is contained in comments within the .ipynd file itself.

####Notes:

1. For some cases there was no available redshift value for a supernova’s host environment. In these cases redshift values of the supernova itself were used. These cases include:

  ASASSN-15fj, ASASSN-15ho, CSS140425:161024+470440, CSS140501:170414+174839, CSS141123:091002+521856, iPTF13dad, iPTF13dkl, iPTFdkx, iPTF14gdr, iPTF15xi, LSQ12fuk, LSQ12gef, LSQ13crf, LSQ14age, LSQ14ahm, LSQ14fmg, LSQ14gde, LSQ15aae, PS1-13dkh, PS15aez, PS15mt, PS15sv, PTF11moy, PTF11qri, PTF11qzq, PTF13asv, PTF13ddg, SN2011ha, SN2011io, SN2012go, SN2013bo, SN2013bq, SN2013ck, SN2014dk

2. When inheriting this project there were two supernova "iPTFdkj", and "iPTFdkx" in the the input file 'GALEX flux.csv' that were missing associated redshift info and .int files). I took these as typos for iPTF13dkj, and iPTF13dkx.

3. The photon counts per second for each supernova were collected manually using ds9. If the exact pixel value of the source was 0 at the location of the supernova, the pixel with a value closest to the target was used. 

4. 'File list.csv' contains a list of the .tar archives and .int files corresponding to each supernova. It will also be updated to include a list of which .int files in which the intended target was not observed. 

5. The script treats the error in pixel area and flux conversion factor as being zero. To change these alter the values of the variable Pixel_area_err and flux_conv_err respectivley. 


