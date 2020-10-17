#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function

from .__init__ import APIBase, log
from urllib import urlencode


class Scheduler(APIBase):
    """Scheduling operations

    Extends:
        APIBase
    """

    def __init__(self, securityToken, baseURL='https://mobilecloud.perfectomobile.com/services/'):
        """construct class

        Arguments:
            securityToken {string} -- security token generated through the perfecto console

        Keyword Arguments:
            baseURL {str} -- Base url for the web services. (default: {'https://mobilecloud.perfectomobile.com/services/'})
        """
        self.initClient(securityToken, baseURL)

    def createSchedule(self, scheduleKey, recurrence, scriptKey,
                       status=None, owner=None, startTime=None,
                       endTime=None, repeatCount=None, description=None,
                       responseFormat="json", admin=False, *parameters, **securedParams):
        """Creates a new scheduled execution. It is possible to request a status message via email or SMS indicating whether the script ran successfully.

            Users can create up to 20 scheduled executions.
            Every scheduled execution name must be unique. You cannot use the same scheduled execution name more than once


        Arguments:
            scheduleKey {string} -- Format is: visibility:<scheduled execution_name>
                                    visibility values: PUBLIC, PRIVATE, GROUP.
                                    The default visibility is PRIVATE.
                                    PRIVATE – the scheduled execution can be viewed by the owner only.
                                    GROUP – the scheduled execution can be viewed by everyone in the owner's group.
                                    PUBLIC – the scheduled execution can be viewed by every user.
                                    execution_name is supplied by the user.
                                    The scheduled execution can be updated by its owner and by automation
                                    administrators.
            recurrence {string} -- Cron expression.
                                   The Cron expression maker can be used for creating Cron expressions.
                                   Cron expression limitations
                                   It is not possible for run a script every second.
                                   In the second and minute expressions " *" is not allowed.
                                   Note: The Cron expression is reset every round hour/day.
                                   For example, if a schedule is executed every 20 minutes, starting 10
                                   minutes after the top of the hour, in first hour the script
                                   will run at x:30, x:50, and in the next hour it will run
                                   at x:30, x:50 again.
            scriptKey {string} -- Format is: visibility:<scheduled execution_name>
                                  visibility values: PUBLIC, PRIVATE, GROUP.
                                  The default visibility is PRIVATE.
                                   PRIVATE – the scheduled execution can be viewed by the owner only.
                                   GROUP – the scheduled execution can be viewed by everyone in the owner's group.
                                   PUBLIC – the scheduled execution can be viewed by every user.
                                   execution_name is supplied by the user.
                                   The scheduled execution can be updated by its owner and by automation
                                   administrators.
            *params {List[Tuple[string, string]]} -- [description]
            **securedParams {dict[string, string]} -- [description]

        Keyword Arguments:
            status {string} -- Available values: ACTIVE, INACTIVE  (default: {None})
            owner {string} -- The user name of the user who owns the scheduled execution.
                              This parameter is used in conjunction with the admin parameter to allow
                              administrators to perform operations on scheduled executions of other users.
                              If a user with administrative credentials wants to create a scheduled
                              executions of user "User", specify the parameters as
                              admin=true and owner=User. (default: {None})
            startTime {long} -- When the scheduled execution will start. In UTC milliseconds.  (default: {None})
            endTime {long} -- When the scheduled execution will end. In UTC milliseconds.  (default: {None})
            repeatCount {int} -- The number of times the scheduled execution will be executed.  (default: {None})
            description {string} -- The description of the scheduled execution (free text).  (default: {None})
            responseFormat {str} -- Available values: json, xml (default: {"json"})
            admin {bool}         -- true to allow users with administrative credentials to create schedules
                                    for users in their group. (default: {False})
        """
        if not scheduleKey or not recurrence or not scriptKey:
            raise Exception("scheduleKey, recurrence, and scriptKey are required parameters and the values are wrong.")
        uriStr = "/schedules?operation=create"
        params = {}
        rslt = None
        if status:
            params["status"] = status
        if owner:
            params["owner"] = owner
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
        if repeatCount:
            params["repeatCount"] = repeatCount
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        params["scheduleKey"] = scheduleKey
        params["recurrence"] = recurrence
        params["scriptKey"] = scriptKey
        if parameters:
            params.update({("param.%s" % k, v) for (k, v) in parameters})
        if securedParams:
            params.update({("securedParam.%s" % k, v) for (k, v) in securedParams})
        uriStr += urlencode(params)
        log.debug("parameters are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("createSchedule API failed because '%s'" % e.message)
            raise Exception("create schedule API call failed because '%s'" % e.message)
        return rslt

    def getScheduledExcutions(self, owner=None, responseFormat="json", admin=False):
        """Last updated: Dec 06, 2016 11:57
        Returns a list of scheduled executions.
        It is possible to return all scheduled executions,
        scheduled executions according to visibility:
        private, public, group, or single scheduled executions.

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the scheduled execution.
                              This parameter is used in conjunction with the admin
                              parameter to allow administrators to perform operations
                              on scheduled executions of other users. If a user with
                              administrative credentials wants to get a list of scheduled
                              executions of user "User", specify the parameters as
                              admin=true and owner=User. (default: {None})
            responseFormat {str} -- Available values: json, xml (default: {"json"})
            admin {bool} -- true to allow users with administrative
                            credentials to create schedules for
                            users in their group. (default: {False})
        """
        uriStr = "/schedules?operation=list"
        params = {}
        rslt = None
        if owner:
            params["owner"] = owner
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        uriStr += urlencode(params)
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("getScheduledExecutions API call failed because '%s'", e.message)
            raise Exception("list scheduled executions API call failed because '%s'" % e.message)
        return rslt

    def getExecutionInfo(self, scheduleKey, owner=None, responseFormat="json", admin=False):
        """Retrieves information about the scheduled execution.
            It is possible to retrieve information on any scheduled
            execution regardless if it was defined as private,
            public, or group.

        Arguments:
            scheduleKey {string} -- scheduleKey for a scheduled execution

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the scheduled execution.
                              This parameter is used in conjunction with the admin parameter
                              to allow administrators to perform operations on scheduled
                              executions of other users. If a user with administrative
                              credentials wants to get information for a scheduled execution
                              of user "User", specify the parameters as admin=true and
                              owner=User. (default: {None})
            responseFormat {str} -- Available values: json, xml (default: {"json"})
            admin {bool} --     true to allow users with administrative
                                credentials to create schedules for users in their group. (default: {False})
        """
        if not scheduleKey:
            raise Exception("scheduleKey is a required parameter and the data is invalid.")
        uriStr = "/schedules/%s?operation=info" % scheduleKey
        rslt = None
        params = {}
        if owner:
            params["owner"] = owner
        params["responseFormat"] = responseFormat
        if admin:
            params["admin"] = admin
        uriStr += urlencode(params)
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("getExecutionInfo API call failed because '%s'" % e.message)
            raise Exception("Excecution info API call failed because '%s'" % e.message)
        return rslt

    def deleteScheduledExecution(self, scheduleKey, owner=None, responseFormat='json', admin=False):
        """Deletes an existing scheduled execution, specified by the scheduleKey

        Arguments:
            scheduleKey {string} -- schedule ID to update

        Keyword Arguments:
            owner {string} --   The user name of the user who owns the scheduled execution.
                                This parameter is used in conjunction with the admin parameter
                                to allow administrators to perform operations on scheduled
                                executions of other users. If a user with administrative
                                credentials wants to delete a scheduled execution of user
                                "User", specify the parameters as admin=true and owner=User.
                                (default: {None})
            responseFormat {str} -- Available values: JSON, XML (default: {'json'})
            admin {bool} -- true to allow users with administrative credentials to create
                            schedules for users in their group. (default: {False})
        """
        if not scheduleKey:
            raise Exception("scheduleKey is a required parameter and the data is invalid.")
        uriStr = "/schedules/%s?operation=delete" % scheduleKey
        rslt = None
        params = {}
        if owner:
            params["owner"]
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        uriStr += urlencode(params)
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("deleteScheduledExecution API call failed because '%s'" % e.message)
            raise Exception("delete scheduled execution failed because '%s'" % e.message)
        return rslt

    def updateScheduledExecution(self, scheduleKey, owner=None, recurrence=None,
                                 startTime=None, endTime=None, repeateCount=None,
                                 scriptKey=None, description=None, responseFormat='json',
                                 admin=False, *parameters, **securedParams):
        """Updates an existing scheduled execution.
        Changes the value of any provided parameter value. Parameters not included
        remain unchanged.

        Arguments:
            scheduleKey {string} -- the key for the schedule to modify

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the scheduled execution.
                              This parameter is used in conjunction with the admin
                              parameter to allow administrators to perform operations on
                              scheduled executions of other users. If a user with
                              administrative credentials wants to update a scheduled
                              execution of user "User", specify the parameters
                              asadmin=true and owner=User. (default: {None})
            recurrence {string} -- Cron expression.
                                    See notes in Create operation Parameters
                                    list
                                    https://developers.perfectomobile.com/display/PD/Create+Scheduled+Execution
                                    (default: {None})
            startTime {long} -- When the scheduled execution will start. In Unix/Epoch system
                                time format (default: {None})
            endTime {long} -- When the scheduled execution will end. In Unix/Epoch system
                            time format (default: {None})
            repeateCount {int} -- The number of times the scheduled execution will be executed. (default: {None})
            scriptKey {string} -- The repository key of the automation script file. For example,
                                    Private:executeScript.xml (default: {None})
            description {string} -- The description of the scheduled execution (free text).
                                    (default: {None})
            responseFormat {str} -- Available values: json, xml (default: {'json'})
            admin {bool} -- true to allow users with administrative credentials to create
                                schedules for users in their group. (default: {False})
        """
        if not scheduleKey:
            raise Exception("schedule key is required and is invalid.")
        uriStr = "/schedules/%s?operation=update" % scheduleKey
        rslt = None
        params = {}
        if parameters:
            params.update({("param.%s" % k, v) for (k, v) in parameters})
        if securedParams:
            params.update({("securedParam.%s" % k, v) for (k, v) in securedParams})
        if owner:
            params["owner"] = owner
        if recurrence:
            params["recurrence"] = recurrence
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
        if repeateCount:
            params["repeateCount"] = repeateCount
        if scriptKey:
            params["scriptKey"] = scriptKey
        if description:
            params["description"] = description
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        uriStr += urlencode(params)
        log.debug("parameters are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("updateScheduledExecution API call failed because '%s'" % e.message)
            raise Exception("update scheduled execution API call failed because '%s'" % e.message)
        return rslt
