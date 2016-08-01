#General use
import os
import numpy as np
from astropy.io import fits
from astropy.cosmology import WMAP9 as cosmo

#For reading and creating tables
from astropy.table import Table, unique

#For performing photometry
from astropy import units as u
from photutils import aperture_photometry, SkyCircularAperture
from astropy.wcs import WCS

#For generating a plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class surface_brightness():
    
    def __init__(self, cord_dict = {}, red_dict = {}):
        #Make sure we have redshift and coordinates of each supernova
        if cord_dict.keys() == red_dict.keys():
            self.cord_dict = cord_dict #Dict of supernova coordinates
            self.red_dict = red_dict #Dict of supernova redshifts
        
        else:
            raise ValueError('''Keys in coordinate and redshift dictionaries
                                (self.cord_dict, self.red_dict) do not match''')

    def conv_error(self, val, err):
    
        '''
        Find the error in a conversion factor from kpc^2 to arcmin^2 using a
        black box error method.
    
        Args:
            val (float): A redshift value.
            err (float): Error in the redshift.
        
        Returns:
            error (float): Error in the conversion factor.
        '''
        
        diff = (cosmo.kpc_comoving_per_arcmin(val + err)**2
                - cosmo.kpc_comoving_per_arcmin(val - err)**2)
        
        error = abs(.5 * diff.value)
        return(error)
    
    def lum_dist_error(self, val, err):
        
        '''
        Find the error in luminosity distance by using a black box error
        method.
        
        Args:
            val (float): A redshift value
            err (float): Error in the redshift
        
        Returns:
            error (float): Error in the luminosity distance
        '''
        
        diff = (cosmo.luminosity_distance(val + err).cgs
                - cosmo.luminosity_distance(val - err).cgs)
        
        error = abs(.5 * diff.value)
        return(error)
    
    def flux_error(self, pho_val, pho_err, conv_val):
        
        '''
        Find error in the calculated flux due to error in the measured
        photon counts per second and flux conversion factor.
        
        Args:
            pho_val  (float): Average photon counts per second
            pho_err  (float): Error in pho_val
            conv_val (float): Conversion factor from average photon counts 
                                  per second to flux
        
        Returns:
            error (float): Error in the associated flux value
        '''
        
        error = (conv_val * pho_err)**2
        return(error)
    
    def luminosity_error(self, flux_val, flux_err, dist_val, dist_err):
        
        '''
        Find error in the calculated Luminosity due error in the flux and
        luminosity distance
        
        Args:
            flux_val (float): Average photon counts per second
            flux_err (float): Error in val
            dist_val (float): Comoving distance
            dist_err (float): Error in comoving distance
        
        Returns:
            error (float): Error in the luminosity
        '''
        
        error = np.sqrt((4 * np.pi * (dist_val**2) * flux_err)**2
                        + (8 * np.pi * dist_val * flux_val * dist_err)**2)
        
        return(error)
    
    def surf_brightness_error(self, lum_val, lum_err, conv_val, conv_err):
        
        '''
        Find the error in surface brightness
        
        Args:
            lum_val  (float): Luminosity of a supernova environment
            lum_err  (float): Error in the luminosity
            conv_val (float): Conversion factor from arcmin^2 to Kpc^2
            conv_err (float): Error in the conversion factor
        
        Returns:
            error (float): Error in the Surface brightness
        '''
        
        error = np.sqrt((conv_val * lum_err / 3600)**2
                        + (lum_val * conv_err / 3600)**2)
        
        return(error)
    
    def zero_check(self, fits_file, cordinate, r):
        
        '''
        Perform photometry on a wt type .fits file and checks if there are
        data pixels in an aperture.
        
        Args:
            fits_file (str)     : File path of a .fits file
            cordinate (SkyCoord): Coordinate of a supernova in degrees
            r         (Quantity): Radius of a photometry aperture in arcmin
        
        Returns:
            'no check file' (str) : Returned if there is no check file
            in_file         (bool): [supernova name(string),
                                     photometry value (float),
                                     exposure time (float)]
        '''
        
        if os.path.isfile(fits_file.replace('d-int', 'd-exp')):
            with fits.open(fits_file.replace('d-int', 'd-exp')) as hdulist:
                aperture = SkyCircularAperture(cordinate, r)
                phot_table = aperture_photometry(hdulist[0], aperture)
            
                if (phot_table[0][0] != 0) is True:
                    return(True)
            
                else:
                    return('no supernova found')
        
        else:
            return('no check file')
    
    def photometry(self, fits_file, radius):
        
        '''
        Perform photometry on an int type .fits file.
        
        Args:
            fits_file (str)  : File path of an int type .fits file
            radius    (float): Radius of the desired aperture in kpc
        
        Returns:
            results (list): [supernova name (str),
                             photometry value (float),
                             exposure time (float)]
            
            results (list): ['error' (str),
                             fits file path (str),
                             error description (str)]
        '''
        
        results = []
        
        if os.path.isfile(fits_file.replace('d-int', 'd-skybg')):
            with fits.open(fits_file) as (int_file
                    ), fits.open(fits_file.replace('d-int', 'd-skybg')) as (skybg_file
                    ):
    
                wcs = WCS(fits_file)
                for sn in self.cord_dict:
                
                    #Define the SN location in pixels
                    w = wcs.all_world2pix(self.cord_dict[sn].ra, self.cord_dict[sn].dec, 1)
                    
                    #Make sure the sn is located in the image
                    if 0 < w[0] < 3600 and 0 < w[1] < 3600:
                        #Find arcmin of a 1kpc radius region
                        r = radius * u.kpc / cosmo.kpc_comoving_per_arcmin(float(self.red_dict[sn]))
                        
                        #Create an aperture
                        aperture = SkyCircularAperture(self.cord_dict[sn], r)
                        
                        #create an array of the error in each pixel
                        exp_time = int_file[0].header['EXPTIME']
                        int_error = np.sqrt(int_file[0].data / exp_time)
                        skybg_error = np.sqrt(skybg_file[0].data / exp_time)
                        
                        #Perform photometry
                        int_phot_table = aperture_photometry(int_file[0], aperture, error = int_error)
                        
                        if int_phot_table[0][0] != 0:
                            skybg_phot_table = aperture_photometry(skybg_file[0], aperture, error = skybg_error)
                            
                            photometry_sum = int_phot_table[0][0] - skybg_phot_table[0][0]
                            photometry_error = np.sqrt(int_phot_table[0][1]**2 + skybg_phot_table[0][1]**2)
                            
                            results.append([sn, exp_time, photometry_sum, photometry_error])
                        
                        else:
                            check = self.zero_check(fits_file, self.cord_dict[sn], r)
                            if check == True:
                                skybg_phot_table = aperture_photometry(skybg_file[0], aperture, error = skybg_error)
                                
                                photometry_sum = int_phot_table[0][0] - skybg_phot_table[0][0]
                                photometry_error = np.sqrt(int_phot_table[0][1]**2 + skybg_phot_table[0][1]**2)
                                
                                results.append([sn, exp_time, photometry_sum, photometry_error])
                            
                            else:
                                results.append(['error', fits_file, check])
            
            if results == []:
                results.append(['error', fits_file, 'no supernova found'])
                return(results)
            
            else:
                return(results)
            
        else:
            results.append(['error', fits_file, 'no skybg file'])
            return(results)
    
    def create_tables(self, uv_type, directory, radius, show_list = False):
        
        '''
        Perform photometry on a directory of .fits files and create two
        tables. The first table contains the redshift, exposure time,
        luminosity, and surface brightness for various supernova, along with
        the associated error values. The second table is a log outlining any
        files that do not contain a supernova or are missing checkfiles. If
        show_list is set equal to true, the path each fits file will be
        printed before performing photometry on it.
        
        Args:
            uv_type   (str)  : Specifies which type of uv to create a table
                                   for. Use either 'NUV' or 'FUV'.
            directory (str)  : A directory containing .fits files
            radius    (float): Radius of desired photometry aperture in kpc
            show_list (bool) : Whether or not to print the file path of each
                                   fits file

        Returns:
            results (list): [Data table (Table), Log table (Table)]
        '''
        
        #Make sure we have redshift and coordinates of each supernova
        if self.cord_dict.keys() != self.red_dict.keys():
            raise ValueError('''Keys in coordinate and redshift dictionaries
                                (self.cord_dict, self.red_dict) do not match''')
        
        label = uv_type + ' ' + str(radius) + 'kpc '

        #Define the tables that will be returned by the function
        log = Table(names = ['File Path', 'Issue'], dtype = [object, object])
        out = Table(names = ['sn',
                             'Redshift',
                             'Redshift Error',
                             label + 'Exposure Time',
                             'Flux',
                             'Flux Error',
                             label + 'Luminosity',
                             label + 'Luminosity Error',
                             label + 'Surface Brightness',
                             label + 'Surface Brightness Error'],

                    dtype = ('S70', 'float64', 'float64', 'float64', 'float64',
                             'float64', 'float64', 'float64', 'float64', 'float64'))

        out['Redshift'].unit = u.dimensionless_unscaled
        out['Redshift Error'].unit = u.dimensionless_unscaled
        out[label + 'Exposure Time'].unit = u.s
        out['Flux'].unit =  u.erg / u.s / u.Angstrom / u.kpc / u.kpc / u.cm / u.cm / np.pi
        out['Flux Error'].unit = u.erg / u.s / u.Angstrom / u.kpc / u.kpc / u.cm / u.cm / np.pi
        out[label + 'Luminosity'].unit = u.erg / u.s / u.Angstrom / u.kpc / u.kpc
        out[label + 'Luminosity Error'].unit = u.erg / u.s / u.Angstrom / u.kpc / u.kpc
        out[label + 'Surface Brightness'].unit = u.erg / u.s / u.Angstrom / u.arcsec / u.arcsec
        out[label + 'Surface Brightness Error'].unit = u.erg / u.s / u.Angstrom / u.arcsec / u.arcsec

        #Set parameters that are specific to NUV or FUV observations
        if 'N' in uv_type.upper():
            file_key = "nd-int" #A string distinguing galex file types
            flux_conv = 2.06 * 1e-16 #A conversion factor from counts per second to flux

        elif 'F' in uv_type.upper():
            file_key = "fd-int"
            flux_conv = 1.40 * 1e-15

        #Create a list of files to perform photometry on
        file_list = []
        for path, subdirs, files in os.walk(directory):
            for name in files:
                if file_key in name and len(name.split('.')) < 3:
                    file_list.append(os.path.join(path, name))

        #Perform photometry on each .fits file
        for fits_file in file_list:
            if show_list == True:
                print(len(file_list), ':', fits_file, flush = True)

            p = self.photometry(fits_file, radius)
            for elt in p:
                if elt[0] == 'error':
                    log.add_row([elt[1], elt[2]])

                else:
                    #We calculate the values to be entered in the table
                    redshift = float(self.red_dict[elt[0]])
                    peculiar_redshift = np.sqrt((1 + (300 / 299792.458)) / (1 - (300 / 299792.458))) - 1
                    redshift_err = np.sqrt((redshift / 1000)**2 + (peculiar_redshift)**2)

                    arcmin = cosmo.kpc_comoving_per_arcmin(redshift).value**2 #kpc^2 per arcmin^2
                    arcmin_err = self.conv_error(redshift, redshift_err)

                    photom = elt[2] #The photometry value
                    photom_err = elt[3]

                    flux = flux_conv * photom #convert cps to flux using the conversion factor
                    flux_err = self.flux_error(photom, photom_err, flux_conv)

                    ldist = cosmo.luminosity_distance(redshift).cgs.value #Luminosity Distance (cm)
                    ldist_err = self.lum_dist_error(redshift, redshift_err)

                    lum = flux * 4 * np.pi * (ldist**2) #luminosity = flux*4*pi*r^2
                    lum_err = self.luminosity_error(flux, flux_err, ldist, ldist_err)

                    sbrightness = lum * arcmin / 3600
                    sbrightness_err = self.surf_brightness_error(lum, lum_err, arcmin, arcmin_err)

                    out.add_row([elt[0], redshift, redshift_err, elt[1], flux, flux_err,
                                 lum, lum_err, sbrightness, sbrightness_err])

            file_list.remove(fits_file)

        out.sort(label + 'Surface Brightness Error')
        out_unique = unique(out, keys = 'sn')
        out_unique.sort('sn')

        return([out_unique, log])

    def create_plots(self, data_table, uv_type, radius):

        '''
        Create .pdf plots of UV surface brightness vs redshift in units of
        erg s-1 A-1 arcsec-2 and erg s-1 A-1 kpc-2. Plots are created using
        results from the create_table() function. Both plots are saved to the
        working directory.

        Args:
            data_table (Table): Data table returned by create_table()
            uv_type    (str)  : Specifies if the data is for 'NUV' or 'FUV'.

        Returns:
            None
        '''

        label = uv_type + ' ' + str(radius) + 'kpc '

        if 'N' in uv_type.upper(): plot_name = 'NUV Surface Brightness of SN Local Enviornments'
        elif 'F' in uv_type.upper(): plot_name = 'FUV Surface Brightness of SN Local Enviornments'

        plt.figure(1)
        plt.xlabel('Redshift')
        plt.ylabel(str(data_table[label + 'Surface Brightness'].unit))
        plt.title(plot_name)

        plt.figure(2)
        plt.xlabel('Redshift')
        plt.ylabel(str(data_table[label + 'Luminosity'].unit))
        plt.title(plot_name)

        for row in data_table:
            if row[label + 'Surface Brightness'] > 0:
                sigma = row['Flux'] / row['Flux Error']
                if sigma <= 3:

                    plt.figure(1)
                    plt.semilogy(row['Redshift'],
                                 row[label + 'Surface Brightness'],
                                 marker = u'$\u21a7$',
                                 markeredgecolor='lightgrey',
                                 color = 'lightgrey')

                    plt.figure(2)
                    plt.semilogy(row['Redshift'],
                                 row[label + 'Luminosity'],
                                 marker = u'$\u21a7$',
                                 markeredgecolor='lightgrey',
                                 color = 'lightgrey')

        for row in data_table:
            if row[label + 'Surface Brightness'] > 0:
                sigma = row['Flux'] / row['Flux Error']
                if sigma > 3:
                    error = (row[label + 'Surface Brightness Error'],
                             row[label + 'Luminosity Error'])

                    plt.figure(1)
                    plt.semilogy(row['Redshift'],
                                 row[label + 'Surface Brightness'],
                                 marker = '.',
                                 color = 'black')

                    plt.errorbar(row['Redshift'],
                                 row[label + 'Surface Brightness'],
                                 yerr = error[0],
                                 color = 'black',
                                 linestyle = '')

                    plt.figure(2)
                    plt.semilogy(row['Redshift'],
                                 row[label + 'Luminosity'],
                                 marker = '.',
                                 color = 'black')

                    plt.errorbar(row['Redshift'],
                                 row[label + 'Luminosity'],
                                 yerr = error[1],
                                 color = 'black',
                                 linestyle = '')

        plt.figure(1)
        plt.savefig(uv_type + ' plot (arcsec).pdf')

        plt.figure(2)
        plt.savefig(uv_type + ' plot (kpc).pdf')

        plt.close("all")

