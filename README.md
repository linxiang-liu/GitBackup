# GitBackup

备份GitLab/GitHub仓库到本地。

支持的参数如下：

| 参数 | 描述 |
| ------------- | ------------- |
| --gitlab_url | GitLab服务器地址，默认为<https://gitlab.com> |
| --gitlab_token | GitLab private token |
| --gitlab_backup_dir | 本地GitLab备份文件夹路径 |
| --github_token | GitHub private token |
| --github_backup_dir |本地GitHub备份文件夹路径 |
| --gitea_url | Gitea服务器地址 |
| --gitea_token | Gitea private token |
| --gitea_backup_dir | 本地Gitea备份文件夹路径 |

查看帮助：

```bash
GitBackup.py --help
```

示例：

```bash
GitBackup.py --gitlab_token=gitlab_token --gitlab_backup_dir=/gitlab/backup/dir/ --github_token=github_token --github_backup_dir=/github/backup/dir/
```
