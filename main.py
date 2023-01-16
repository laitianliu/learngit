# This is a get Harbor Artifacts Information Api
import harborapi


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import requests
# import json


def get_artifacts_tag(artifact_list):
    tag_name_list = []
    for x in artifact_list:
        tag_name_list.append(x.get('tags')[0].get('name'))
    return tag_name_list


def get_repository_list(project_name, with_project=True):
    repository_lists = harbor_enty.repository_info(project_name)
    repo_name_list = []
    for x in repository_lists:
        repo_items = x.get('name')
        if with_project:
            repo_name_list.append(repo_items)
        else:
            repo_item = repo_items.split('/')[1]
            repo_name_list.append(repo_item)
    return repo_name_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    harbor_url = ""
    harbor_user = ""
    harbor_passwd = ""
    page_size = 50
    harbor_protocol = "http"
    harbor_enty = harborapi.HarborApi(harbor_url, harbor_user, harbor_passwd, page_size, harbor_protocol)
    # 获取harbor所有项目
    # project_list = harbor_enty.get_all_project()
    # for i in range(len(project_list)):
    #     # print(test[i-1].get('name'))
    #     with open("project_all.txt", "a+") as f:
    #         f.write(project_list[i-1].get('name') + '\n')

    # 获取项目下所有仓库
    # repository_list = get_repository_list('adc', with_project=True)
    # for i in repository_list:
    #     with open("repolist_all.txt", "a+") as f:
    #         f.write(i + '\n')

    # 根据项目和仓库名称查询制品信息，并获取最近10个tag信息。
    artifacts_info_list = harbor_enty.artifacts_info('adc', 'yms-ai-adc-frontend-pipline-uac')
    tag_infos = get_artifacts_tag(artifacts_info_list)
    for i in tag_infos:
        with open("tag_info.txt", "a+") as f:
            f.write(i + '\n')
