#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function
from .__init__ import APIBase, log, properParams
from urllib import urlencode


class Devices(APIBase):
    """
    Accessing device operations.
    """
    __listFilters = {
        "admin",  #true to filter the list to only show devices that the user is able to administrate and provide administrative information in the response.
        "deviceId",  #The identifier of the device specified as IMEI or ESN.
        "manufacturer",  #The manufacturer of the device. For example: Apple, Samsung, HTC, ...
        "model",  #The model of the device. For example: Galaxy S6, iPhone 6, ...
        "distributor",  #The distributor of the device.
        "firmware",  #The version of the firmware of the device.
        "operator.name",  #The name of the operator network to which the device is connected.
        "operator.country",  #The country in which the operator is located.
        "operator.code",  #The code associated with the operator.
        "description",  #The description of the device.
        "location",  #The geographical location of the device.
        "language",  #The current language of the device.
        "status",  #The current connectivity status of the device. The following is a list of the possible values: disconnected connected unavailable - This status indicates a device that is connected but is not available. For example, the device might be initializing or may have encountered an error.
        "allocatedTo",  #The identifier of the user account that is currently using the device.
        "reservedTo",  #The identifier of the user account that is currently reserving the device.
        "availableTo",  #The identifier of the user account for which the device is currently available.
        "owner",  #The owner user id. Used by an administrator to list all the devices which are accessible to this owner. This accessibility is determined by the user's roles - the user can access only devices that have one of the roles assigned to him.
        "inUse",  #true indicates that the device is currently in use.
        "cradleId",  #The identifier of the cradle to which the device is connected.
        "os",  #The name of the device's operating system.
        "osVersion",  #The version of the device's operating system.
        "resolution",  #The resolution of the device's screen.
        "phoneNumber",  #The phone number of the device.
        "link.type"  #The type of device. The possible values are: all, local or lab.
    }



    __deviceUpdateParams = {
        "description", # string      The new device description
        "roles",   #list of strings     Comma separated list of device roles
    }

    def __init__(self, securityToken, baseURL='https://mobilecloud.perfectomobile.com/services/'):
        self.initClient(securityToken, baseURL)

    def listDevices(self, **filters):
        """
        list available devices according to the given filters
        ie 'filterName'="filterValue"
        periods are not allowed in identifiers so just use the part after the period.
        """
        rslt = None
        if filters:
            if "name" in filters:
                val = filters["name"]
                del filters["name"]
                filters["operator.name"] = val
            if "country" in filters:
                val = filters["country"]
                del filters["country"]
                filters["operator.country"] = val
            if "code" in filters:
                val = filters["code"]
                del filters["code"]
                filters["country.code"] = val
            if "type" in filters:
                val = filters["type"]
                del filters["type"]
                filters["link.type"] = val
        try:
            subset = set([unicode(x) for x in filters.keys()])
            log.debug("subset is '%s'" % str(subset))
            log.debug("filters are '%s'" % str(self.__listFilters))
            if filters and not self.__listFilters.issuperset(subset):
                raise Exception("One or more unknown filter types given.")
            uriStr = "/handsets?operation=list"
            if filters:
                uriStr = properParams(uriStr, urlencode(filters))
            log.debug("URI params = %s" % uriStr)
            rslt = self.client.send_get(uriStr)
            if rslt:
                log.debug("list device response\n%s" % str(rslt))
        except Exception as e:
            log.error("list devices API called failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("listDevices API call failed because '%s'" % e.message)
        return rslt

    def deviceInfo(self, deviceID, admin=False):
        """
            Get the info for a specific device
        """
        rslt = None
        try:
            uriStr = "/handsets/%s?operation=info" % deviceID
            if admin:
                uriStr = properParams(uriStr, urlencode({"admin": admin}))
            log.debug("param string is '%s'" % uriStr)
            rslt = self.client.send_get(uriStr)
            log.debug("device info result is '%s'" % rslt)
        except Exception as e:
            log.error("deviceInfo API called failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("deviceInfo API call failed because '%s'" % e.message)
        return rslt

    def updateDevice(self, deviceID, description=None, roles=[], admin=False):
        """
            Update device info.

            deviceID: required device ID
            description: optional update description
            roles: optional list or tuple of strings representing roles.

            One or more of the optional parameters is required.
        """
        rslt = None
        try:
            if not description and not roles:
                raise Exception("One or more of description or roles required in function call.")
            if not deviceID:
                raise Exception("Device ID is required.")
            uriStr = "/handsets/%s?operation=update" % deviceID
            args = {}
            if description:
                args["description"] = description
            if roles:
                args["roles"] = ",".join(roles)
            if admin:
                args["admin"] = admin
            uriStr = properParams(uriStr, urlencode(args))
            log.debug("updateDevice params are '%s'" % uriStr)
            rslt = self.client.send_get(uriStr)
            log.debug("result of update = '%s'" % rslt)
        except Exception as e:
            log.error("updateDevice API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("updateDevice failed because '%s'" % e.message)
        return rslt

    def releaseDevice(self, deviceID, admin=False):
        """
            Force a release of a device to make sure we are not being charged for time for a given device.

            deviceID: required device if that we are releasing.
            admin: optional admin for this device?
        """
        rslt = None
        uriStr = "/handsets/%s?operation=release" % deviceID
        try:
            if admin:
                uriStr = properParams(uriStr, urlencode({"admin": admin}))
            log.debug("params are '%s'" % uriStr)
            rslt = self.client.send_get(uriStr)
            log.debug("result is '%s'" % rslt)
        except Exception as e:
            log.error("releaseDevice API call failed because '%s'" % e.message)
            log.debug(e.args)
            raise Exception("relase device API call failed because '%s'" % e.message)
        return rslt
