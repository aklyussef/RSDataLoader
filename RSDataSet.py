import os
import os.path
import glob
import re

class HRaster:

    def __init__(self,rootpath):
        """Should load all bands based on sattelite Landsat7/8 Sentinel1,2,3 MODUS
        blue
        green
        red
        swir
        load the corresponding scaling factor for level of data proccessing
        """
        self.rootpath = rootpath
        #band designations in order BLUE,GREEN,RED,NIR,SWIR1,SWIR2
        #Landsat https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites?qt-news_science_products=0#qt-news_science_products
        #Sentinel https://en.wikipedia.org/wiki/Sentinel-2
        self.band_designation = {'L07':[1,2,3,4,5,7],'L08':[2,3,4,5,6,7],'S2':[2,3,4,8,11,12]}
        self.get_satellite_from_path()
        metadata_method_lookup = {'L08':self.extract_LS_filename_metdata,'S02':self.extract_S_metadata,
                                  'L07':self.extract_LS_filename_metdata}
        #Get metadata including list of bands
        metadata_method_lookup[self.type]()

        #save band paths
        self.bluep = self.bands[self.band_designation[self.type][0]-1]
        self.greenp = self.bands[self.band_designation[self.type][1]-1]
        self.redp = self.bands[self.band_designation[self.type][2]-1]
        self.nirp = self.bands[self.band_designation[self.type][3]-1]
        self.swir1p = self.bands[self.band_designation[self.type][4]-1]
        self.swir2p = self.bands[self.band_designation[self.type][5]-1]

        return

    #TODO: Test if this takes too long and simplify if necessary
    def load_bands(self,):
        """
        Loads the bands initialized
        :return:
        """
        pass

    def get_satellite_from_path(self):
        """Should check for sattelite information given root path regex matching
        sentinel data holds info in root path
        landsat data holds info in filename
        Returns: keys to band designation dictionary depending on sat type
        """
        self.landsatdirregex = re.compile('L\w(\d\d)\d\d\d\d\d\d(\d\d\d\d).*')
        self.sentineldirregex = re.compile('S(\d)(\w)_\w\w\w\w\w\w_(\d\d\d\d).*')
        #Type string L for landsat append sat number after metadata extraction
        self.type = ''
        if re.match(self.landsatdirregex,self.rootpath):
            self.type = 'L'
            self.extract_LS_filename_metdata()
            self.type += re.match(self.landsatdirregex,self.rootpath).group(1)
            return self.type
        elif re.match(self.sentineldirregex,self.rootpath):
            self.type = 'S'
            self.extract_S_metadata()
            self.type += re.match(self.sentineldirregex,self.rootpath).group(1)
            return self.type
            #elif file.match(self.modius)...etc
        return self.type

    def extract_LS_filename_metdata(self):
        """
        extracts metadata according to
        https://www.usgs.gov/faqs/how-can-i-tell-difference-between-landsat-collections-data-and-landsat-data-i-have-downloaded?qt-news_science_products=7#qt-news_science_products
        :param None:
        :return: None
        """
        self.imagepath = self.rootpath
        self.landsatfileregex = re.compile('L\w(\d\d)_(\w\w\w\w)_\d\d\d\d\d\d_(\d\d\d\d).*')
        self.corrections = {'L1TP':'Precision Terrain', 'L1GT':'Systematic Terrain', 'L1GS':'Systematic'}
        #TODO figure out better way to get band info
        img1 = os.path.join(self.rootpath,'*.B*.tif')
        img2 = os.path.join(self.rootpath,'*band*.tif')
        self.images = glob.glob(img1) + glob.glob(img2)
        self.images.sort()
        for file in self.images:
            metadata = re.match(self.landsatregex,file)
            self.satnumber = metadata.group(1)
            self.correction_string = metadata.group(2)
            self.sensingyear = metadata.group(3)
        pass

    def extract_S_metadata(self):
        """crawls subdirectories of rootpath to find path of remote sensing data
        saves it as saves it as image rootpath
        extracts metadata from filenames"""
        for (dirpath, dirnames, filenames) in os.walk(self.rootpath):
            for file in filenames:
                if file.endswith('.jp2'):
                    self.imagepath = dirpath
                    self.bands = filenames.sort()
        return