import sys
import os


cur_path = os.getcwd()
sys.path.append(cur_path)

init_env = '''
    1. install git:
        sudo yum install git
    2. setup git:
        https://help.github.com/articles/set-up-git/
        https://help.github.com/articles/generating-ssh-keys/
    3. install Flask (python and pip were installed by aws default):
        sudo pup install Flask
    4. create project:
        https://github.com/tanchao/chaos.trade
    5. install mysql:
        sudo yum install mysql mysql-server mysql-libs mysql-devel
        sudo service mysqld start
        sudo chkconfig --level 35 mysqld on
        chkconfig --list | grep mysql
        http://jingyan.baidu.com/article/acf728fd10c3d6f8e510a3ef.html
        http://www.360doc.com/content/15/0516/11/14900341_470864335.shtml
    6. install web server
        yum install nginx
        sudo service nginx start
        sudo yum install gcc
        sudo CC=gcc pip install uwsgi
'''
