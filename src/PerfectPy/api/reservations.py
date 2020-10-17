#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function
from .__init__ import APIBase, log, properParams
from urllib import urlencode


class Reservations(APIBase):
    """
    Devices may be reserved to ensure availability. If you open a device but do not lock or reserve it, another user may lock or reserve the device and your session will be terminated. You will be blocked from using the device for the reserved time period of the other user.

    Users should reserve a device to guarantee its availability.

    Reserving a device according to device attributes
    Use the Get Devices List operation to select one or more devices with a specific filter, and reserve.

    Public Cloud - Reservations for public cloud devices are charged at time of reservation. In case a reservation is cancelled the balance of hours will be restored.

    Time Format - The input parameters, startTime and endTime, indicate the time as a long value representing the number of ms after January 1st, 1970 (System time). These parameters are found in the Create, Update, and List reservation operations.

    """

    def __init__(self, securityToken, baseURL='https://mobilecloud.perfectomobile.com/services/'):
        self.initClient(securityToken, baseURL)

    def reservationList(self, resourceIds=None, startTime=None, endTime=None, reservedTo=None, admin=False, responseFormat="json"):
        """
        Return a list of reserved devices.
        resourceIds *   optional A comma separated list of deviceId.
        startTime     long  The start time, in milliseconds from midnight January 1, 1970 ( Epoch/Unix Time)
        endTime        long  The end time, in milliseconds from midnight January 1, 1970 ( Epoch/Unix Time)
        reservedTo  string      The user the device is reserved to.
        responseFormat  string  json    The format to use for the response. json, xml
        """
        uriStr = "reservations?operation=list"

        params = {}
        if admin:
            params["admin"] = "true" if admin else "false"
        if responseFormat is not "json":
            params["responseFormat"] = str(responseFormat)
        if reservedTo:
            params["reservedTo"] = str(reservedTo)
        if resourceIds:
            params["resourceIds"] = ",".join([str(x) for x in resourceIds])
        if startTime:
            params["startTime"] = str(startTime)
        if endTime:
            params["endTime"] = str(endTime)
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("parameters are '%s'" % uriStr)
        rslt = None
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("reservatiionList API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("reservation list API call failed because '%s'" % e.message)
        return rslt

    def reservationInfo(self, reservationID, admin=False, responseFormat="json"):
        """
        Get reservation info for a specific reservation
        admin   boolean false   true to allow users with administrative credentials to get reservation info for users in their group.
                note: not available on shared MCM.
        responseFormat  string  json    The format to use for the response. JSON, XML
        """
        rslt = None
        uriStr = "reservations/%s?operation=info" % reservationID
        params = {}
        if admin:
            params["admin"] = "true" if admin else "false"
        params["responseFormat"] = str(responseFormat)
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("response is '%s'" % rslt)
        except Exception as e:
            log.error("reservationInfo API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("reservation info API call failed because '%s'" % e.message)
        return rslt

    def createReservation(self, resourceIDs, startTime, endTime, reserveTo=None, description=None, responseFormat="json", admin=False):
        """
        Creates a new device reservation.

        Public Cloud hourly users - your account will be charged upon confirmation of the reservation.

        admin   boolean false   true to allow users with administrative credentials to create reservations for users in their group.
            note: users with administrative credentials can create reservations longer than the max time-frame.
            note: not available on shared MCM.
        resourceIds *   List      A comma separated list of deviceId.
        startTime * long        The reservation start time, measured in milliseconds, from midnight, January 1, 1970 UTC (standard UNIX time). **
                                * Use -1 to indicate current time.
        endTime *   long        The reservation end time, measured in milliseconds, from midnight, January 1, 1970 UTC (standard UNIX time). **
        reservedTo  string      The user the device is reserved to.
        description     string      The reservation description (free text).
        responseFormat  string  json    The format to use for the response: json, xml

        Response:
            {
                "reservationIds":["87640"],
                "info":{
                    "creationTime":{
                        "formatted":"2016-12-04T11:51:25Z",
                        "millis":"1480852285681"
                    },
                    "items":"1",
                    "modelVersion":"2.6.0.0",
                    "productVersion":"master",
                    "time":"2016-12-04T11:51:25Z"
                }
            }
        """
        if not resourceIDs or not startTime or not endTime:
            raise Exception("Missing one or more required parameters.")
        rslt = None
        uriStr = "reservations?operation=create"
        params = {}
        params["resourceIds"] = ",".join([str(x) for x in resourceIDs])
        params["startTime"] = str(startTime)
        params["endTime"] = str(endTime)
        if reserveTo:
            params["reserveTo"] = str(reserveTo)
        if description:
            params["description"] = str(description)
        params["responseFormat"] = str(responseFormat)
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("createReservation response is '%s'" % rslt)
        except Exception as e:
            log.error("createReservation API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("create reservation API call failed because '%s'" % e.message)
        return rslt

    def deleteReservation(self, reservationID, scope="remaining", responseFormat="json", admin=False):
        """
        Deletes a specific device reservation. The reservation is indicated by the <reservationID> provided when the reservation was created.

        admin   boolean false   true to allow users with administrative credentials to delete reservations for users in their group.
            note: not available on shared MCM.
        scope   string  remaining   Available for active reservations only.
                        remaining to delete the rest of a reservation with tokens refund.
                        entire to delete the entire reservation (only available to admin users).
                        No tokens refund, tokens should be adjusted separately if required.
        responseFormat  string  json    The format to use for the response: json, xml
        """
        if not reservationID:
            raise Exception("reservationID is a required parameter.")
        rslt = None
        uriStr = "reservations/%s?operation=delete" % str(reservationID)
        params = {}
        params["scope"] = str(scope)
        params["responseFormat"] = str(responseFormat)
        if admin:
            params["admin"] = "true" if admin else "false"
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("result is '%s'" % rslt)
        except Exception as e:
            log.error("deleteReservation API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("delete reservation API call failed because '%s'" % e.message)
        return rslt

    def updateReservation(self, reservationID, startTime=None, endTime=None, reserveTo=None, description=None, responseFormat="json", admin=False):
        """
        Updates a specific device reservation. The reservation is indicated by the <reservationID> provided when the reservation was created.

        admin   boolean false   true to allow users with administrative credentials to update reservations for users in their group.
                                note: not available on shared MCM.
        startTime    long       The reservation start time, measured in milliseconds, from midnight, January 1, 1970 UTC.
        endTime      long       The reservation end time, measured in milliseconds, from midnight, January 1, 1970 UTC.
        reserveTo    string     The user the device is reserved to.
        description      string     The reservation description (free text).
        responseFormat  string  json    The format to use for the response. json, xml
        """
        if not reservationID:
            raise Exception("ReservationID is a required parameter and is not valid.")
        if not startTime and not endTime and not reserveTo and not description:
            raise Exception("One or more optional parameters are required.")
        rslt = None
        uriStr = "reservations/%s?operation=update" % reservationID
        params = {}
        if startTime:
            params["startTime"] = str(startTime)
        if endTime:
            params["endTime"] = str(endTime)
        if reserveTo:
            params["reserveTo"] = str(reserveTo)
        if description:
            params["description"] = str(description)
        if admin:
            params["admin"] = "true" if admin else "false"
        params["responseFormat"] = str(responseFormat)
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("updateReservation API call failed because '%s'" % e.message)
            raise Exception("update reservation API call failed because '%s'." % e.message)
        return rslt
