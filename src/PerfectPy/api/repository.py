#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, generators, division, absolute_import, with_statement, print_function
from .__init__ import APIBase, log, properParams
from urllib import urlencode
#URL: https://mycloud.perfectomobile.com/services/handsets
#Request: operation=list&user=myUsername&password=myPassword&status=connected


class Repository(APIBase):
    """
    Repository operations.
    """

    def __init__(self, securityToken, baseURL='https://mobilecloud.perfectomobile.com/services/'):
        """
        Construct the class

        Arguments:
            securityToken {string} -- Perfecto security token

        Keyword Arguments:
            baseURL {str} -- baseURL for the web services (default: {'https://mobilecloud.perfectomobile.com/services/'})
        """
        self.initClient(securityToken, baseURL)
        return

    def uploadItem(self, repository, itemKey, data, admin=False, owner=None, group=None, overwrite=False, format=None, reponseFormat="json", **properties):
        """Upload an item to a repository

        Arguments:
            repository {string} -- Name of the repo to upload to
            itemKey {string} -- item key for this uploaded item
            data    {bytes}    The file to upload
            admin   boolean     false   true to allow users with administrative credentials
                                        to upload items to private repository of other automation users.
            owner   string      The user name of the user who owns the item. This parameter is used
                                in conjunction with the admin parameter to correctly identify items
                                to be stored in PRIVATE or GROUP repositories of the owner.
                                For example, if a user with administrative credentials wants to
                                upload an item where the repositoryItemKey is PRIVATE:myItem.jpg
                                orGROUP:myItem.jpg, specify the parameters as admin=true and
                                owner=itemUser.
            group   string      The group name. This parameter is used in conjunction with the admin
                                parameter to correctly identify items to be stored in GROUP repositories.
                                For example, if a user with administrative credentials wants to upload
                                an item where the repositoryItemKey isGROUP:myItem.jpg , specify the
                                parameters as admin=true and group= groupName.
            property.<name> boolean         The name and value of one or more a repository properties,
                                each prefixed with property. For example, to specify an integer property
                                called readonly with the value true, add property.readonly=true to the URL.
            overwrite   boolean     false   true to overwrite existing files.
            format  string      The format of the file. This option only applies when uploading data tables.
                                possible values: xml, csv
            responseFormat  string  json    Format of response: json, xml
        """
        if not repository or not itemKey:
            raise Exception("repository key or itemKey are invalid values.")
        uriStr = u"repositories/%s/%s?operation=upload" % (repository, itemKey)
        rslt = None
        params = {}
        if admin:
            params[u"admin"] = admin
        if owner:
            params[u"owner"] = owner
        if group:
            params[u"group"] = group
        if overwrite:
            params[u"overwrite"] = "true" if overwrite is True else "false"
        if format:
            params[u"format"] = format
        params[u"responseFormat"] = reponseFormat
        if properties:
            params.update({(u"property.%s" % k, v) for (k, v) in properties})
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_post(uriStr, data)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("uploadItem API call failed because '%s'" % e.message)
            log.error(e)
            raise Exception("upload item API call failed because '%s'" % e.message)
        return rslt

    def repositoryList(self, repository, itemKey, owner=None, group=None, responseFormat='json', admin=False):
        """Gets the status of one or more items from the repository area specified by and optionally
        from the subarea within the repository specified. If the is not specified, the response returns
        items from all the subareas.

            is specified as follows:

                media - the repository area for general media files
                datatables - the repository area for data table files
                scripts - the repository area for automation script files



        Arguments:
            repository {string} -- The repository name
            itemKey {string} -- is the location of the items within the repository,
                                specified as a repository key that contains subarea and folder information

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the item.
                              This parameter is used in conjunction with the
                              admin parameter to correctly identify items stored
                              in PRIVATE or GROUP repositories of the owner.
                              For example, if a user with administrative credentials
                              wants to download an items list where the repositoryItemKey
                              is PRIVATE:myItem.jpg or GROUP:myItem.jpg, specify the
                              parameters asadmin=true and owner=itemUser. (default: {None})
            group {string} -- The group name. This parameter is used in conjunction
                               with the admin parameter to correctly identify items
                               stored in GROUP repositories. For example, if a user with
                               administrative credentials wants to download an items list
                               where the repositoryItemKey is GROUP:myItem.jpg, specify
                               the parameters as admin=true and group= groupName. (default: {None})
            responseFormat {str} -- Format of response: json, xml (default: {'json'})
            admin {bool} -- true to allow users with administrative credentials to get
                            the status of one or more items from the repository of other
                            automation users.  (default: {False})
        """
        if not repository and not itemKey:
            raise Exception("repository and itemKey are required fields and the values are invalid.")
        uriStr = "repositories/%s/%s?operation=list" % (repository, itemKey)
        rslt = None
        params = {}
        if owner:
            params["owner"] = owner
        if group:
            params["group"] = group
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("listRepository API call failed because '%s'" % e.message)
            raise Exception("list repository API call failed because '%s'" % e.message)
        return rslt

    def deleteItem(self, repository, itemKey, owner=None, group=None, responseFormat="json", admin=False):
        """Deletes the item specified by <repositoryItemKey> from the repository area specified by <repository>

        Arguments:
            repository {string} -- The name of the repository
            itemKey {string} -- The key for the item

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the item.
                              This parameter is used in conjunction with the
                              admin parameter to correctly identify items stored
                              in PRIVATE or GROUP repositories of the owner.
                              For example, if an user with administrative
                              credentials wants to delete an item where the
                              repositoryItemKey is PRIVATE:myItem.jpg or
                              GROUP:myItem.jpg, specify the parameters as
                              admin=true and owner=itemUser. (default: {None})
            group {string} -- The group name. This parameter is used in
                              conjunction with the admin parameter to correctly
                              identify items stored in GROUP repositories.
                              For example, if a user with administrative
                              credentials wants to delete an item where the
                              repositoryItemKey is GROUP:myItem.jpg , specify
                              the parameters as admin=true and group= groupName
                              (default: {None})
            responseFormat {str} -- Format of response: json, xml (default: {"json"})
            admin {bool} -- true to allow users with administrative credentials to
                            delete other users items in the public repository, items
                            in the private repository of other automation users, and
                            folder that are not empty.  (default: {False})
        """
        if not repository or not itemKey:
            raise Exception("repository and itemKey are required parameters and the values are invalid.")
        uriStr = "repositories/%s/%s?operation=delete" % (repository, itemKey)
        rslt = None
        params = {}
        if owner:
            params["owner"] = owner
        if group:
            params["group"] = group
        if admin:
            params["admin"] = admin
        params["responseFormat"] = responseFormat
        uriStr = properParams(uriStr, urlencode(params))
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("deleteItem API call failed because '%s'" % e.message)
            raise Exception("delete item API call failed because '%s'" % e.message)
        return rslt

    def cleanupRepository(self, itemKey, daysToKeep, owner=None, group=None, dryRun=False, userStatus=None, responseFormat="json", admin=False):
        """Delete all the execution reports older than the specified number of days using the lastModified.daysToKeep parameter.

        Arguments:
            itemKey {string} -- What to delete

        Keyword Arguments:
            owner {string} -- The user name of the user who owns the repository items.
                               Use * to specify this operation for all users within the
                               PRIVATE visibility (with corresponding repositoryItemKey).
                               (default: {None})
            group {string} -- Note: the parameter must be used when specifying PRIVATE visibility.
                              When specifying owner with GROUP visibility, the operation will be applied to the owner's group.
                              This parameter cannot be specified with PUBLIC or SYSTEM visibility. group ½
                              string
                              The group ID. This parameter is used in conjunction with the
                              admin parameter to correctly identify items stored in GROUP
                              repositories.
                              Use * to specify the operation for all groups under GROUP
                              visibility (with corresponding repositoryItemKey)
                              (default: {None})
            dryRun {bool} -- Use this mode to test the clean operation without deleting any
                             items. Statistics of what would be deleted once this operation
                             is performed will be returned.  (default: {False})
            daysToKeep {int} -- The number of days to keep reports since last modification.
                                Reports older than this number of days will be deleted.
                                (default: {None})
            userStatus {string} -- Filter the users according to their status.
                                    Used only when specifying owner =*.
                                    Supported values:ACTIVE,INACTIVE,PENDING,DELETE
                                    (default: {None})
            responseFormat {str} -- Format of the response: json, xml (default: {"json"})
            admin {bool} -- true to allow users with administrative credentials to delete
                            other user items in the executions repository. (default: {False})
        """
        if not itemKey:
            raise Exception("itemKey value is invalid.")
        uriStr = "repositories/executions/%s?operation=clean" % itemKey
        rslt = None
        params = {}
        if owner:
            params["owner"] = owner
        if group:
            params["group"] = group
        if dryRun:
            params["dryRun"] = dryRun
        params["lastModified.daysToKeep"] = daysToKeep
        if userStatus:
            params["userStatus"] = userStatus
        if admin:
            params["admin"] = admin
        uriStr = properParams(uriStr, urlencode(params))
        log.debug("params are '%s'" % uriStr)
        try:
            rslt = self.client.send_get(uriStr)
            log.debug("results are '%s'" % rslt)
        except Exception as e:
            log.error("cleanupRepository API call failed because '%s'" % e.message)
            raise Exception("clean up repository API call failed because '%s'" % e.message)
        return rslt
