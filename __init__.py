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
'''
