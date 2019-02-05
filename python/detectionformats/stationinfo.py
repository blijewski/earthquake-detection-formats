#!/usr/bin/env python

#package imports
import detectionformats.site
import detectionformats.source

#stdlib imports
import json


class StationInfo:
    """ StationInfo - a conversion class used to create, parse, and validate 
        station info data as part of detection data.
    """
    # json keys
    TYPE_KEY = "Type"
    SITE_KEY = "Site"
    LATITUDE_KEY = "Latitude"
    LONGITUDE_KEY = "Longitude"
    ELEVATION_KEY = "Elevation"
    QUALITY_KEY = "Quality"
    ENABLE_KEY = "Enable"
    USEFORTELESEISMIC_KEY = "UseForTeleseismic"
    INFORMATIONREQUESTOR_KEY = "InformationRequestor"

    def __init__(self, newSite=None, newLatitude=None, newLongitude=None,
        newElevation=None, newQuality=None, newEnable=None,
        newUseForTeleseismic=None, newInformationRequestor=None):
        """Initialize the station info object. Constructs an empty object
           if all arguments are None

        Args:
            newSite: a required detectionformats.site.Site containing the desired
                site
            newLatitude: a required Number containing the latitude as a float in
                degrees
            newLongitude: a required Number containing the longitude as a float
                in degrees
            newElevation: a required Number containing the elevation as a float
            newQuality: an optional Number containing the station quality
            newEnable: an optional Boolean indicating whether the station should
                be used or not
            newUseForTeleseismic: an optional Boolean indicating whether the
                station should for teleseismic calculations or not
            newInformationRequestor: an optional detectionformats.source.Source
                containing the source of the information
        Returns:
            Nothing
        Raises:
            Nothing
        """
        # first required keys
        self.type = 'StationInfo'
        if newSite is not None:
            self.site = newSite
        else:
            self.site = detectionformats.site.Site()
        if newLatitude is not None:
            self.latitude = newLatitude
        if newLongitude is not None:
            self.longitude = newLongitude
        if newElevation is not None:
            self.elevation = newElevation

        # second optional keys
        if newQuality is not None:
            self.quality = newQuality

        if newEnable is not None:
            self.enable = newEnable

        if newUseForTeleseismic is not None:
            self.useForTeleseismic = newUseForTeleseismic

        if newInformationRequestor is not None:
            self.informationRequestor = newInformationRequestor
        else:
            self.informationRequestor = detectionformats.source.Source()

    def fromJSONString(self, jsonString):
        """Populates the object from a json formatted string

        Args:
            jsonString: a required String containing the json formatted text
        Returns:
            Nothing
        Raises:
            Nothing
        """
        jsonObject = json.loads(jsonString)
        self.fromDict(jsonObject)

    def fromDict(self, aDict):
        """Populates the object from a dictionary

        Args:
            aDict: a required dictionary
        Returns:
            Nothing
        Raises:
            Nothing
        """
        # first required keys
        try:
            self.type = aDict[self.TYPE_KEY]
            self.site.fromDict(aDict[self.SITE_KEY])
            self.latitude = aDict[self.LATITUDE_KEY]
            self.longitude = aDict[self.LONGITUDE_KEY]
            self.elevation = aDict[self.ELEVATION_KEY]
        except(ValueError, KeyError, TypeError) as e:
            print("Dict format error, missing required keys: %s" % e)

        # second optional keys
        if self.QUALITY_KEY in aDict:
            self.quality = aDict[self.QUALITY_KEY]

        if self.ENABLE_KEY in aDict:
            self.enable = aDict[self.ENABLE_KEY]

        if self.USEFORTELESEISMIC_KEY in aDict:
            self.useForTeleseismic = aDict[self.USEFORTELESEISMIC_KEY]

        if self.INFORMATIONREQUESTOR_KEY in aDict:
            self.informationRequestor.fromDict(aDict[self.INFORMATIONREQUESTOR_KEY])

    def toJSONString(self):
        """Converts the object to a json formatted string

        Args:
            None
        Returns:
            The JSON formatted message as a String
        Raises:
            Nothing
        """
        jsonObject = self.toDict()

        return json.dumps(jsonObject, ensure_ascii=False)

    def toDict(self):
        """Converts the object to a dictionary

        Args:
            None
        Returns:
            The dictionary
        Raises:
            Nothing
        """
        aDict = {}

        # first required keys
        try:
            aDict[self.TYPE_KEY] = self.type
            aDict[self.SITE_KEY] = self.site.toDict()
            aDict[self.LATITUDE_KEY] = self.latitude
            aDict[self.LONGITUDE_KEY] = self.longitude
            aDict[self.ELEVATION_KEY] = self.elevation
        except(NameError, AttributeError) as e:
            print("Missing required data error: %s" % e)

        # second optional keys
        if hasattr(self, 'quality'):
            aDict[self.QUALITY_KEY] = self.quality

        if hasattr(self, 'enable'):
            aDict[self.ENABLE_KEY] = self.enable

        if hasattr(self, 'useForTeleseismic'):
            aDict[self.USEFORTELESEISMIC_KEY] = self.useForTeleseismic

        if hasattr(self, 'informationRequestor'):
            aDict[self.INFORMATIONREQUESTOR_KEY] = self.informationRequestor.toDict()

        return aDict

    def isValid(self):
        """Checks to see if the object is valid

        Args:
            None
        Returns:
            True if the object is valid, False otherwise
        Raises:
            Nothing
        """
        errorList = self.getErrors()

        return not errorList

    def getErrors(self):
        """Gets a list of object validation errors

        Args:
            None
        Returns:
            A List of Strings containing the validation error messages
        Raises:
            Nothing
        """
        errorList = []

        # first required keys
        try:
            if self.type == '':
                errorList.append('Empty Type in StationInfo Class.')
            elif self.type != 'StationInfo':
                errorList.append('Non-StationInfo Type in StationInfo Class.')
        except(NameError, AttributeError):
            errorList.append('No Type in StationInfo Class.')

        try:
            if not self.site.isValid():
                errorList.append('Invalid Site in StationInfo Class.')
        except(NameError, AttributeError):
            errorList.append('No Site in StationInfo Class.')

        try:
            if self.latitude < -90 or self.latitude > 90:
                errorList.append('Latitude in StationInfo Class not in the range of -90 to 90.')
        except(NameError, AttributeError):
            errorList.append('No Latitude in StationInfo Class.')

        try:
            if self.longitude < -180 or self.longitude > 180:
                errorList.append('Longitude in StationInfo Class not in the range of -180 to 180.')
        except(NameError, AttributeError):
            errorList.append('No Longitude in StationInfo Class.')

        try:
            self.elevation
        except(NameError, AttributeError):
            errorList.append('No Elevation in StationInfo Class.')

        # second optional keys
        if hasattr(self, 'informationRequestor'):
            if not self.informationRequestor.isValid():
                errorList.append('Invalid InformationRequestor in StationInfo Class.')

        return errorList
