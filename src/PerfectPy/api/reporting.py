#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function
from .__init__ import APIBase, log
from urllib import urlencode


class Reporting(APIBase):
    """
    Use these commands to download reports, images, video, vitals & network information, and log files:
    """

    def __init__(self, securityToken, baseURL="https://mobilecloud.perfectomobile.com/services/"):
        """
            Class constructor

            Arguments:
                securityToken {String}: generated token from perfector account. Used instead of username and password
                baseURL {String}: the url to the web services. Public cloud has a different URL compared to a private cloud.
        """
        self.initClient(securityToken, baseURL)

    def getExecutionReport(self, reportKey, owner='', format="xml", responseFormat="json"):
        """
            Download an execution report.

            Arguments:
                reportKey {String}: The key to the report.
                owner {String}: Reports available to this user.
                format {String}: The format of the report. (Default: xml)
                responseFormat {String}: The format of the response. (Default: json)
        """
        if not reportKey:
            raise Exception("reportKey is required and value is invalid.")
        rslt = None
        uriStr = "/reports/%s?operation=download" % reportKey
        params = {}
        if owner:
            params["owner"] = owner
        params["format"] = format
        params["responseFormat"] = responseFormat
        uriStr += urlencode(params)
        log.debug("Params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("Parameters are '%s'" % rslt)
        except Exception as e:
            log.error("getExecutionReport API call failed because '%s'" % e.message)
            raise Exception("get execution report API call failed because '%s'" % e.message)
        return rslt

    def getReportAttachmentList(self, reportKey, type="", owner="", admin=False):
        """
            The <reportKey> is the report identifier returned by the Start New Script Execution, the Get Script Execution Status, or the Get Script Executions List operations.

        Arguments:
            reportKey {string} -- The key for the report

        Keyword Arguments:
            type {str} -- The attachment type.
                            Values: video, image, network, monitor, log.
                            By default all the types are returned. (default: {""})
            owner {str} -- The username of the report owner.
                            This parameter is used in conjunction with the admin
                            parameter to determine the location of reports stored
                            in PRIVATE repositories.
                            For example, if an admin user wants to get the list of
                            attachments of a report for an execution owned by the
                            user execUser, and the reportKey is
                            PRIVATE:myReport.xml,
                            specify the parameters as admin=true and owner=execUser.
                            The attachments of the report named myReport.xml
                            stored under the execUser user's PRIVATE area will be
                            returned.
                            (default: {""})
            admin {bool} -- true - allows admin users to get the list of attachments
                            of a execution report owned by other automation users.
                            (default: {False})
        """
        if not reportKey:
            raise Exception("reportKey is required and the value is invalid.")
        uriStr = "/reports/%s?operation=attachments" % reportKey
        rslt = None
        params = {}
        if type:
            params["type"] = type
        if owner:
            params["owner"] = owner
        if admin:
            params["admin"] = admin
        uriStr += urlencode(params)
        log.debug("Params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("Results are '%s'" % rslt)
        except Exception as e:
            log.error("getReportAttachmentList API call failed because '%s'" % e.message)
            raise Exception("report log attachment list API call failed because '%s'" % e.message)
        return rslt

    def getExecutionReportAttachment(self, reportType, reportKey, attachment, owner="", admin=False):
        """
        The <reportKey> is the report identifier returned by the Start
        New Script Execution, the Get Script Execution Status, or the Get
        Script Executions List operations.

        Arguments:
            reportKey {string} -- report identifier
            attachment {string} -- The image path as it appears in the attachment
                                    tag in the report.
            reportType {str} -- type of the report. ie. image, video, network,
                                monitor, transactions, log, audioText

        Keyword Arguments:

            owner {str} -- The username of the report owner.
                           This parameter is used in conjunction with the admin
                           parameter to correctly identify the location of
                           reports stored in PRIVATE repositories.
                           For example, if an admin user wants to download
                           a report for an execution owned by the user execUser,
                           and the reportKey is PRIVATE:myReport.xml, specify
                           the parameters as admin=true and owner=execUser.
                           The report named myReport.xml stored under the
                           execUser user's PRIVATE area will be downloaded.
                            (default: {""})
            admin {bool} -- true to allow admin users to download image
                            attachments of execution reports owned by other
                            automation users. (default: {False})
        """
        if not reportKey or not attachment or not reportType:
            raise Exception("reportKey, attachment, and reportType are required parameters and their values are invalid.")
        rslt = None
        uriStr = "/reports/%s?operation=%s" % (reportKey, reportType)
        params = {}
        params["attachment"] = attachment
        if owner:
            params["owner"] = owner
        if admin:
            params["admin"] = admin
        uriStr += urlencode(params)
        log.degug("parameters are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("Results are '%s'" % rslt)
        except Exception as e:
            log.error("getExecutionReportImage API call failed because '%s'" % e.message)
            raise Exception("download execution report API call failed because '%s'" % e.message)
        return rslt
