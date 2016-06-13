
import os

from github import Github

here = os.path.dirname(os.path.abspath(__file__))

g = Github(open(os.path.join(here,'..','.github_token'), 'r').read())

repo = g.get_repo('cacahootie/modly')

print repo.get_contents('test/tmod.py').content
