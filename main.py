# This is a sample Python script.
import harborapi
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json


def get_artifacts_tag(artifact_list):
    tag_name_list = []
    for x in artifact_list:
        tag_name_list.append(x.get('tags')[0].get('name'))
    print(tag_name_list)


def get_repository_list(project_name):
    repository_list = harbor_enty.repository_info(project_name)
    repo_name_list = []
    for x in repository_list:
        repo_items = x.get('name')
        repo_item = repo_items.split('/')[1]
        repo_name_list.append(repo_item)
    print(repo_name_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    harbor_url = ""
    harbor_user = ""
    harbor_passwd = ""
    harbor_protocol = ""
    harbor_enty = harborapi.HarborApi(harbor_url, harbor_user, harbor_passwd, harbor_protocol)
    test = harbor_enty.project_info('adc')
    print(test)
    # get_repository_list('adc')
    # artifacts_list = harbor_enty.artifacts_info('adc', 'yms-ai-adc-frontend-pipline-uac')
    # get_artifacts_tag(artifacts_list)
