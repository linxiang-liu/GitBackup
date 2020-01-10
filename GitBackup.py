import argparse
import gitlab
from github import Github
import giteapy
from giteapy.rest import ApiException
import os

def backup_git_project(local_git_path, http_url, ssh_url):
    if not os.path.exists(local_git_path):
        print("Create backup for " + http_url)
        os.system("git clone --mirror " + ssh_url + " " + local_git_path)
    else:
        print("Update backup for " + http_url)
        os.system("git --git-dir=" + local_git_path + " remote update")

def backup_gitlab(gitlab_url: str, gitlab_token: str, gitlab_backup_dir: str):
    gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
    max_projects_in_page = 20;

    page = 1;
    while True:
        projects = gl.projects.list(owned=True, page = page)
        projects_count = len( projects)
        if projects_count > 0:
            print( '----------------------page: %d ' % page)
            page += 1

            for project in projects:
                print( '----------------------')
                print( "id: %d " % project.id)
                print( "url: " + project.http_url_to_repo)
                print( "ssh: " + project.ssh_url_to_repo)
                print( "name: " + project.name)
                print( "namespace path: " + project.namespace['full_path'])
                print( "path with namespace: " + project.path_with_namespace)
                local_git_path = gitlab_backup_dir + '/' + project.path_with_namespace + ".git"
                local_namespace_path = gitlab_backup_dir  + '/' + project.namespace['full_path']
                if not os.path.exists( local_namespace_path):
                    os.makedirs( local_namespace_path)
                backup_git_project( local_git_path, project.http_url_to_repo, project.ssh_url_to_repo)

        if projects_count < max_projects_in_page:
            break;

    pass

def backup_github(github_token: str, github_backup_dir: str):
    g = Github(github_token)
    projects = g.get_user().get_repos();
    for project in projects:
        print( '----------------------')
        print( "id: %d " % project.id)
        print( "url: " + project.html_url)
        print( "ssh: " + project.ssh_url)
        print( "name: " + project.name)
        print( "namespace path: " + project.owner.login)
        print( "path with namespace: " + project.full_name)
        local_git_path = github_backup_dir + '/' + project.full_name + ".git"
        local_namespace_path = github_backup_dir  + '/' + project.owner.login
        if not os.path.exists( local_namespace_path):
            os.makedirs( local_namespace_path)
        backup_git_project( local_git_path, project.html_url, project.ssh_url)

    pass

def backup_gitea(gitea_url: str, gitea_token: str, gitea_backup_dir: str):
    configuration = giteapy.Configuration()
    configuration.host = gitea_url + "/api/v1"
    configuration.api_key['access_token'] = gitea_token
    api_instance = giteapy.UserApi(giteapy.ApiClient(configuration))
    
    api_response = api_instance.user_current_list_repos()
    print( f"{api_response}")
    for project in api_response:
        print( '----------------------')
        print( "id: %d " % project.id)
        print( "url: " + project.html_url)
        print( "ssh: " + project.ssh_url)
        print( "name: " + project.name)
        print( "path with namespace: " + project.full_name)
        local_git_path = gitea_backup_dir + '/' + project.full_name + ".git"
        local_namespace_path = gitea_backup_dir  + '/' + project.name
        if not os.path.exists( local_namespace_path):
            os.makedirs( local_namespace_path)
        backup_git_project( local_git_path, project.html_url, project.ssh_url)

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gitlab_url", help="the GitLab Server Url, default https://gitlab.com")
    parser.add_argument("--gitlab_token", help="the private token of your GitLab profile")
    parser.add_argument("--gitlab_backup_dir", help="the directory where repositories will be backup")
    parser.add_argument("--github_token", help="the private token of your GitHub profile")
    parser.add_argument("--github_backup_dir", help="the directory where repositories will be backup")
    parser.add_argument("--gitea_url", help="the Gitea Server Url")
    parser.add_argument("--gitea_token", help="the private token of your Gitea profile")
    parser.add_argument("--gitea_backup_dir", help="the directory where repositories will be backup")
    args = parser.parse_args()

    if args.gitlab_url is None:
        args.gitlab_url = "https://gitlab.com"

    if args.gitlab_token and args.gitlab_backup_dir:
        backup_gitlab( args.gitlab_url, args.gitlab_token, args.gitlab_backup_dir)

    if args.github_token and args.github_backup_dir:
        backup_github( args.github_token, args.github_backup_dir)

    if args.gitea_url and args.gitea_token and args.gitea_backup_dir:
        backup_gitea( args.gitea_url, args.gitea_token, args.gitea_backup_dir)
