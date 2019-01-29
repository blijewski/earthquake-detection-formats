#!/usr/bin/env python

#package imports
import detectionformats.source
import detectionformats.pick
import detectionformats.correlation

#stdlib imports
import json
import datetime

# a conversion class used to create, parse, and validate a Detection
# as part of detection data.
class Detection:
    TYPE_KEY = "Type"
    ID_KEY = "ID"
    SOURCE_KEY = "Source"
    HYPOCENTER_KEY = "Hypocenter"
    DETECTIONTYPE_KEY = "DetectionType"
    EVENTTYPE_KEY = "EventType"
    DETECTIONTIME_KEY = "DetectionTime"
    BAYES_KEY = "Bayes"
    MINIMUMDISTANCE_KEY = "MinimumDistance"
    RMS_KEY = "RMS"
    GAP_KEY = "Gap"
    DATA_KEY = "Data"

    # init
    def __init__(self, newID=None, newSource=None, newHypocenter=None,
        newDetectionType=None, newEventType=None, newDetectionTime=None,
        newBayes=None, newMinimumDistance=None, newRMS=None, newGap=None,
        newPickData=None, newCorrelationData=None) :
        """Initialize the detection object. Constructs an empty object
           if all arguments are None

        Args:
            newID: a required String containing the desired ID
            newSource: a required detectionformats.source.Source containing the
                desired source
            newHypocenter: a required detectionformats.hypocenter.Hypocenter
                containing the desired hypocenter
            newDetectionType: an optional String containing the desired detection
                type
            newEventType: an optional detectionformats.eventtype.EventType 
                containing the desired event type
            newDetectionTime: an optional datetime containing the time this
                detection was made
            newBayes: an optional Number containing the desired bayes estimate
                as a float
            newMinimumDistance: an optional Number containing the desired
                minimum Distance measurement as a float
            newRMS: an optional Number containing the desired RMS estimate as a
                float
            newGap: an optional Number containing the gap estimate as a float
            newPickData: an optional array of detectionformats.pick.Pick objects
                that support this detection
            newCorrelationData: an optional array of
                detectionformats.correlation.Correlation objects that support
                this detection
        Returns:
            Nothing
        Raises:
            Nothing
        """
        # first required keys
        self.type = 'Detection'
        if newID is not None:
            self.id = newID

        if newSource is not None:
            self.source = newSource
        else:
            self.source = detectionformats.source.Source()

        if newHypocenter is not None:
            self.hypocenter = newHypocenter
        else:
            self.hypocenter = detectionformats.hypocenter.Hypocenter()

        # second optional keys
        if newDetectionType is not None:
            self.detectionType = newDetectionType

        if newEventType is not None:
            self.eventType = newEventType
        else:
            self.eventType = detectionformats.eventtype.EventType()

        if newDetectionTime is not None:
            self.detectionTime = newDetectionTime

        if newBayes is not None:
            self.bayes = newBayes

        if newMinimumDistance is not None:
            self.minimumDistance = newMinimumDistance

        if newRMS is not None:
            self.rms = newRMS

        if newGap is not None:
            self.gap = newGap

        if newPickData is not None:
            if newPickData and len(newPickData) > 0:
                self.pickData = newPickData

        if newCorrelationData is not None:
            if newCorrelationData and len(newCorrelationData) > 0:
                self.correlationData = newCorrelationData

    # populate class from a json string
    def fromJSONString(self, jsonString) :
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

    # populate class from a dictonary
    def fromDict(self, aDict) :
        """Populates the object from a dictonary

        Args:
            aDict: a required Dictonary
        Returns:
            Nothing
        Raises:
            Nothing
        """
        # first required keys
        try:
            self.type = aDict[self.TYPE_KEY]
            self.id = aDict[self.ID_KEY]
            self.source.fromDict(aDict[self.SOURCE_KEY])
            self.hypocenter.fromDict(aDict[self.HYPOCENTER_KEY])
        except (ValueError, KeyError, TypeError):
            print ("Dict format error")

        # second optional keys
        if self.DETECTIONTYPE_KEY in aDict:
            self.detectionType = aDict[self.DETECTIONTYPE_KEY]

        if self.EVENTTYPE_KEY in aDict:
            self.eventType = detectionformats.eventtype.EventType()
            self.eventType.fromDict(aDict[self.EVENTTYPE_KEY])

        if self.DETECTIONTIME_KEY in aDict:
            timeString = aDict[self.DETECTIONTIME_KEY][:-1] + "000Z"
            self.detectionTime = datetime.datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S.%fZ")

        if self.BAYES_KEY in aDict:
            self.bayes = aDict[self.BAYES_KEY]

        if self.MINIMUMDISTANCE_KEY in aDict:
            self.minimumDistance = aDict[self.MINIMUMDISTANCE_KEY]

        if self.RMS_KEY in aDict:
            self.rms = aDict[self.RMS_KEY]

        if self.GAP_KEY in aDict:
            self.gap = aDict[self.GAP_KEY]

        if self.DATA_KEY in aDict:
            aDataList = aDict[self.DATA_KEY]
            if aDataList:
                self.pickData = []
                self.correlationData = []
                for aData in aDataList:
                    if self.TYPE_KEY in aData:
                        if aData[self.TYPE_KEY] == 'Pick':
                            newPick = detectionformats.pick.Pick()
                            newPick.fromDict(aData)
                            self.pickData.append(newPick)
                        elif aData[self.TYPE_KEY] == 'Correlation':
                            newCorrelation = detectionformats.correlation.Correlation()
                            newCorrelation.fromDict(aData)
                            self.correlationData.append(newCorrelation)

    # convert class to a json string
    def toJSONString(self) :
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

    # convert class to a dictonary
    def toDict(self) :
        """Converts the object to a dictonary

        Args:
            None
        Returns:
            The Dictonary
        Raises:
            Nothing
        """
        aDict = {}

        # first required keys
        try:
            aDict[self.TYPE_KEY] = self.type
            aDict[self.ID_KEY] = self.id
            aDict[self.SOURCE_KEY] = self.source.toDict()
            aDict[self.HYPOCENTER_KEY] = self.hypocenter.toDict()
        except NameError:
            print ("Missing data error")

        # second optional keys
        try:
            aDict[self.DETECTIONTYPE_KEY] = self.detectionType
        except:
            pass

        try:
            if self.eventType.isEmpty() == False:
                aDict[self.EVENTTYPE_KEY] = self.eventType.toDict()
        except:
            pass

        try:
            timeString = self.detectionTime.isoformat(timespec='milliseconds') + "Z"
            aDict[self.DETECTIONTIME_KEY] = timeString
        except:
            pass

        try:
            aDict[self.BAYES_KEY] = self.bayes
        except:
            pass

        try:
            aDict[self.MINIMUMDISTANCE_KEY] = self.minimumDistance
        except:
            pass

        try:
            aDict[self.RMS_KEY] = self.rms
        except:
            pass

        try:
            aDict[self.GAP_KEY] = self.gap
        except:
            pass

        try:
            aDataList = []
            if self.pickData and len(self.pickData) > 0:
                for aPick in self.pickData:
                    aDataList.append(aPick.toDict())

            if self.correlationData and len(self.correlationData) > 0:
                for aCorrelation in self.correlationData:
                    aDataList.append(aCorrelation.toDict())

            aDict[self.DATA_KEY] = aDataList
        except:
            pass


        return aDict

    # test to see if class is valid
    def isValid(self) :
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

    # get list of validation errors
    def getErrors(self) :
        """Gets a list of object validation errors

        Args:
            None
        Returns:
            A List of Strings containing the validation error messages
        Raises:
            Nothing
        """
        errorList = []

        # required values
        try:
            if self.type == '':
                errorList.append('Empty Type in Detection Class.')
            elif self.type != 'Detection':
                errorList.append('Non-Detection Type in Detection Class.')
        except (NameError, AttributeError):
            errorList.append('No Type in Detection Class.')

        try:
            if self.id == '':
                errorList.append('Empty ID in Detection Class.')
        except (NameError, AttributeError):
            errorList.append('No ID in Detection Class.')

        try:
            if self.source.isValid() == False:
                errorList.append('Invalid Source in Detection Class.')
        except (NameError, AttributeError):
            errorList.append('No Source in Detection Class.')

        try:
            if self.hypocenter.isValid() == False:
                errorList.append('Invalid Hypocenter in Detection Class.')
        except (NameError, AttributeError):
            errorList.append('No Hypocenter in Detection Class.')

        # optional values
        try:
            self.detectionType
            if self.detectionType != 'New' and self.detectionType != 'Update' and self.detectionType != 'Final' and self.detectionType != 'Retract':
                errorList.append('Invalid DetectionType in Detection Class.')
        except (NameError, AttributeError):
            pass

        try:
            if self.eventType.isEmpty() == False:
                if self.eventType.isValid() == False:
                    errorList.append('Invalid EventType in Detection Class.')
        except (NameError, AttributeError):
            pass

        try:
            self.detectionTime
        except (NameError, AttributeError):
            pass

        try:
            if self.bayes < 0:
                errorList.append('Bayes in Detection Class not in greater than 0.')
        except (NameError, AttributeError):
            pass

        try:
            if self.minimumDistance < 0:
                errorList.append('MinimumDistance in Detection Class not in greater than 0.')
        except (NameError, AttributeError):
            pass

        try:
            if self.gap < 0 or self.gap > 360:
                errorList.append('Gap in Detection Class not in the range of 0 to 360.')
        except (NameError, AttributeError):
            pass

        try:
            if self.pickData and len(self.pickData) > 0:
                for aPick in self.pickData:
                    if aPick.isValid() == False:
                        errorList.append('Invalid Pick in Detection Class.')
        except (NameError, AttributeError):
            pass

        try:
            if self.correlationData and len(self.correlationData) > 0:
                for aCorrelation in self.correlationData:
                    if aCorrelation.isValid() == False:
                        errorList.append('Invalid Correlation in Detection Class.')
        except (NameError, AttributeError):
            pass

        return errorList
