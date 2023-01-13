# coding=utf8
# Autor : Alaways V
# Time  : 2019/1/22 15:31
# File  : harbor.py
# Software PyCharm

import json
import urllib3
import requests
from pprint import pprint

urllib3.disable_warnings()


class HarborApi(object):
    def __init__(self, url, username, passwd, protocol="https"):
        '''
        init the request
        :param url: url address or doma
        :param username:
        :param passwd:
        :param protect:
        '''
        self.url = url
        self.username = username
        self.passwd = passwd
        self.protocol = protocol

    def project_info(self, project_name):
        project_url = "%s://%s/api/v2.0/projects/%s" % (self.protocol, self.url, project_name)
        headers = {
            'accept': 'application/json',
            'X-Is-Resource-Name': 'false'
        }
        resp = requests.get(project_url, headers, auth=(self.username, self.passwd))
        req_handle = json.loads(resp.content.decode(encoding='utf-8'))
        if 200 == resp.status_code:
            return req_handle
        else:
            raise Exception("Failed to get the project info。")

    def repository_info(self, project_name):
        repository_url = '%s://%s/api/v2.0/projects/%s/repositories?page=1&page_size=10' % (
            self.protocol, self.url, project_name)
        headers = {
            'accept': 'application/json'
        }
        resp = requests.get(repository_url, headers, auth=(self.username, self.passwd))
        req_handle = json.loads(resp.content.decode(encoding='utf-8'))
        if 200 == resp.status_code:
            return req_handle
        else:
            raise Exception("Failed to get the repository info。")

    def artifacts_info(self, project_name, repository_name):
        artifacts_url = '%s://%s/api/v2.0/projects/%s/repositories/%s/artifacts?page=1&page_size=10&with_tag=true' \
                   '&with_label=false&with_scan_overview=false&with_signature=false&with_immutable_status=false' % (
                       self.protocol, self.url, project_name, repository_name)
        headers = {
            'accept': 'application/json',
            'X-Accept-Vulnerabilities': 'application/vnd.scanner.adapter.vuln.report.harbor + json;version = 1.0'
        }
        resp = requests.get(artifacts_url, headers, auth=(self.username, self.passwd))
        req_handle = json.loads(resp.content.decode(encoding='utf-8'))
        if 200 == resp.status_code:
            return req_handle
        else:
            raise Exception("Failed to get the artifacts info。")
