import argparse
import subprocess
import os

from common_util import CommonUtil
from config import branch

parser=argparse.ArgumentParser()

parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--addCommitAndPushToOrigin", "-acp", help="Add changes, commit and push to origin", nargs='?', const="True")
parser.add_argument("--fetchMerge", "-fm", help="Fetch upstream and merge develop-java21 branch", nargs='?', const="True")
parser.add_argument("--add", "-ad", help="Add changes", nargs='?', const="True")
parser.add_argument("--commit", "-cm", help="Commit", nargs='?', const="True")
parser.add_argument("--pushToOrigin", "-po", help="push to origin", nargs='?', const="True")
parser.add_argument("--commitMessage", "-m", help="Commit and push to origin", default='Committing changes.')
parser.add_argument("--listModules", "-lsm", help="List Modules", nargs='?', const="True")
parser.add_argument("--listGitRepos", "-lsr", help="List Git Repos", nargs='?', const="True")
parser.add_argument("--startIndex", "-si", help="The start index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--index", "-i", help="The index of module from which specifically needs to be built", default=None, nargs='?', const="True")

parser.add_argument("--status", "-st", help="git status on all modules", nargs='?', const="True")

parser.add_argument("--diff", "-df", help="git diff on all modules", nargs='?', const="True")



args=parser.parse_args()

util = CommonUtil(args)
modules_to_build=util.modules_to_build
git_repos=util.gitRepos

if util.gitBaseDir is None:
    gitBaseDir = os.getcwd()
else:
    gitBaseDir = util.gitBaseDir

mvnBuildCommand = []

gitAddAllCommand = ['git', 'add', '-u']
gitCommitCommand = ['git', 'commit', '-s', '--allow-empty', '-m', args.commitMessage]
if branch is not None:
    gitPushCommand =  ['git', 'push', 'origin', branch]
else:
    gitPushCommand =  ['git', 'push', 'origin']
gitStatusCommand = ['git', 'status']
gitDiffCommand = ['git', '--no-pager', 'diff']
gitFetchUpstreamCommand = ['git', 'fetch', 'upstream']
gitMergeUpstreamJava21Command = ['git', 'merge', 'upstream/develop-java21']  



print("Git Base Directory: " + gitBaseDir)
   
def listGitRepos():
    util.listGitRepos()

def addCommitAndPushAll():
    for i, repo in enumerate(git_repos):
        addCommitAndPushRepo(i, repo)

def addCommitAndPushRepo(index, repo):
    print(">>>>>>> Working on repo [" + str(index + 1) + "/" + str(len(git_repos))  + "]: " + repo)
    repoFullPath=getFullPath(repo)
    
    if args.add is not None:
        print("Adding all tracked changes")
        runCommand(gitAddAllCommand, repoFullPath)
    
    if args.commit is not None:
        print("Committing changes")
        runCommand(gitCommitCommand, repoFullPath)
        
    if args.pushToOrigin is not None:
        print("Pushing changes")
        runCommand(gitPushCommand, repoFullPath)
    
    
def gitStatusRepos():
    for i, repo in enumerate(git_repos):
        gitStatusRepo(i, repo)

def gitStatusRepo(index, repo):
    print(">>>>>>> Status of Repo [" + str(index + 1) + "/" + str(len(git_repos))  + "]: " + repo)
    repoFullPath=getFullPath(repo)
    runCommand(gitStatusCommand, repoFullPath)
    
    
def gitDiffRepos():
    for i, repo in enumerate(git_repos):
        gitDiffRepo(i, repo)

def gitDiffRepo(index, repo):
    print(">>>>>>> Diff of Repo [" + str(index + 1) + "/" + str(len(git_repos))  + "]: " + repo)
    repoFullPath=getFullPath(repo)
    runCommand(gitDiffCommand, repoFullPath)

def gitFetchMergeRepos():
    for i, repo in enumerate(git_repos):
        gitFetchMergeRepo(i, repo)
    
def gitFetchMergeRepo(index, repo):
    print(">>>>>>> Git Fetch and Merge to develop-java21 branch for Repo [" + str(index + 1) + "/" + str(len(git_repos))  + "]: " + repo)
    repoFullPath=getFullPath(repo)
    runCommand(gitFetchUpstreamCommand, repoFullPath)
    runCommand(gitMergeUpstreamJava21Command, repoFullPath)
    
    
def getFullPath(relativePath):
    return gitBaseDir + '/' + relativePath
    
def runCommand(command, moduleFullPath):
    subprocess.run(command, cwd=moduleFullPath, shell=True, check=True)

def main():

    print("Args: " + str(args))

    if args.add is not None or args.commit is not None or args.pushToOrigin is not None:
        addCommitAndPushAll()
        print(">>>>>>> Commit completed.")
    
    if args.addCommitAndPushToOrigin is not None:
        args.add = True
        args.commit = True
        args.pushToOrigin = True
        addCommitAndPushAll()
        print(">>>>>>> Commit and Push to Origin completed.")
        
    if args.fetchMerge is not None:
        gitFetchMergeRepos()
        
    if args.listModules is not None:
        util.listModules()
        
    if args.listGitRepos is not None:
        listGitRepos()
        
    if args.status is not None:
        gitStatusRepos()
        
    if args.diff is not None:
        gitDiffRepos()


main()
