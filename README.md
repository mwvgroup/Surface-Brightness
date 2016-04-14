# Surface-Brightness
Surface Brightness Calculations

This script uses input values from the file 'GALEX flux.csv' to determine the surface brightness of a supernova's local enviornment. The input file contains the redshift of each enviornment along with the exposure time and average counts per second. For some cases there was no available redshift for a supernova’s host environment. In these cases redshift values of the supernova itself were used. These cases include:

ASASSN-15fj,
ASASSN-15ho,
CSS140425:161024+470440,
CSS140501:170414+174839,
CSS141123:091002+521856,
iPTF13dad,
iPTF13dkl,
iPTFdkx,
iPTF14gdr,
iPTF15xi,
LSQ12fuk,
LSQ12gef,
LSQ13crf,
LSQ14age,
LSQ14ahm,
LSQ14fmg,
LSQ14gde,
LSQ15aae,
PS1-13dkh,
PS15aez,
PS15mt,
PS15sv,
PTF11moy,
PTF11qri,
PTF11qzq,
PTF13asv,
PTF13ddg,
SN2011ha,
SN2011io,
SN2012go,
SN2013bo,
SN2013bq,
SN2013ck,
SN2014dk

The script referances information from the input file by column number (indexed at zero). Because of this it is necessary to properly specify what column number corresponds to what information. For example, collumn 1 may correspod to redshift values while collumn 2 may contain average photon counts per second. These parameters are pointed out in comments toward the beginning of the script.

In the case where the input file has no value for counts per second, the script will treat it as 'nan' and report it as such in the output file.

Some additional notes:
  When inheriting this project there were two supernova "iPTFdkj", and "iPTFdkx" in the GALEX file that were missing associated files (redshift info, .int files). I took these as typos for iPTF13dkj, and iPTF13dkx.
