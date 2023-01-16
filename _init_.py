# -*- coding: utf-8 -*-
# @Time : 2023/01/16 14:30
# @Author : Mr Lai
# @FileName: harbor_api.py
# @Software: Pycharm
import json
import urllib3
import requests

urllib3.disable_warnings()


class HarborApi(object):
    def __init__(self, url, username, passwd, page_size, protocol="https"):
        """
        init the request
        :param url: IP Address
        :param username: harbor username
        :param passwd: harbor password
        :param page_size: query page_size
        :param protocol: http or https
        """
        self.url = url
        self.username = username
        self.passwd = passwd
        self.protocol = protocol
        self.page_size = page_size

    def request_loop(self, api_url):
        request_loop = True
        req_handle = []
        while request_loop:
            request_url = "%s://%s%s" % (
                self.protocol, self.url, api_url)
            headers = {
                'accept': 'application/json'
            }
            resp = requests.get(request_url, headers, auth=(self.username, self.passwd))
            header_link = resp.headers['link']
            if header_link.find('rel="next"') == -1:
                request_loop = False
            else:
                api_url = header_link.split(',')[-1].strip(' ').split(';')[0].strip('<').strip('>')
            req_handle = json.loads(resp.content.decode(encoding='utf-8')) + req_handle
        if 200 == resp.status_code:
            return req_handle
        else:
            raise Exception('Failed to Parse  the request of the' + api_url + 'response。')

    def get_all_project(self):
        api_new = '/api/v2.0/projects?page=1&page_size=' + str(self.page_size) + '&with_detail=false'
        return  self.request_loop(api_new)

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
        api_new = '/api/v2.0/projects/' + project_name + '/repositories?page=1&page_size=' + str(self.page_size) + ''
        return self.request_loop(api_new)

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
