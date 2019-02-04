#!/usr/bin/env python

#stdlib imports
import json

class Site:
    """ Site - a conversion class used to create, parse, and validate site data 
        as part of detection data.
    """
    # json keys
    STATION_KEY = "Station"
    CHANNEL_KEY = "Channel"
    NETWORK_KEY = "Network"
    LOCATION_KEY = "Location"

    def __init__(self, newStation=None, newNetwork=None, newChannel=None,
        newLocation=None):
        """Initialize the site object. Constructs an empty object
           if all arguments are None

        Args:
            newStation: a required String containing the station identifier
            newNetwork: a required String containing the network identifier
            newChannel: an optional String containing the channel code
            newLocation: an optional String containing the location code
        Returns:
            Nothing
        Raises:
            Nothing
        """
        # first required keys
        if newStation is not None:
            self.station = newStation
        if newNetwork is not None:
            self.network = newNetwork

        # second optional keys
        if newChannel is not None:
            if newChannel != '':
                self.channel = newChannel

        if newLocation is not None:
            if newLocation != '':
                self.location = newLocation

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
            self.station = aDict[self.STATION_KEY]
            self.network = aDict[self.NETWORK_KEY]
        except (ValueError, KeyError, TypeError):
            print ("Dict format error")

        # second optional keys
        if self.CHANNEL_KEY in aDict:
            self.channel = aDict[self.CHANNEL_KEY]
        if self.LOCATION_KEY in aDict:
            self.location = aDict[self.LOCATION_KEY]

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
            aDict[self.STATION_KEY] = self.station
            aDict[self.NETWORK_KEY] = self.network
        except NameError:
            print ("Missing data error")

        # second optional keys
        if hasattr(self, 'channel'):
            if self.channel != '':
                aDict[self.CHANNEL_KEY] = self.channel

        if hasattr(self, 'location'):
            if self.location != '':
                aDict[self.LOCATION_KEY] = self.location

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

        if len(errorList) == 0:
            return True
        else:
            return False

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

        try:
            if self.station == '':
                errorList.append('Empty Station in Site Class.')
        except (NameError, AttributeError):
            errorList.append('No Station in Site Class.')

        try:
            if self.network == '':
                errorList.append('Empty Network in Site Class.')
        except (NameError, AttributeError):
            errorList.append('No Network in Site Class.')

        return errorList
