import os
import subprocess
import sys
from migration_config import modules_paths_list_in_order, git_base_dir, git_repos_in_order, branch
from text_changes import pom_changes_dict, java_file_changes_dict
import argparse

parser=argparse.ArgumentParser()

parser.add_argument("--mvnCleanInstall", "-mci", help="Maven Clean Install", nargs='?', const="True")
parser.add_argument("--mvnCleanInstallSkipTests", "-mcist", help="Maven Clean Install with Skip tests and javadoc in build", nargs='?', const="True")
parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--addCommitAndPushToOrigin", "-cpo", help="Add changes, commit and push to origin", nargs='?', const="True")
parser.add_argument("--add", "-ad", help="Add changes", nargs='?', const="True")
parser.add_argument("--commit", "-cm", help="Commit", nargs='?', const="True")
parser.add_argument("--pushToOrigin", "-po", help="push to origin", nargs='?', const="True")
parser.add_argument("--commitMessage", "-m", help="Commit and push to origin", default='Committing changes.')
parser.add_argument("--listModules", "-lsm", help="List Modules", nargs='?', const="True")
parser.add_argument("--listGitRepos", "-lsr", help="List Git Repos", nargs='?', const="True")
parser.add_argument("--moduleIndex", "-im", help="The index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--repoIndex", "-ir", help="The index of repo from which related git action to start", default=1, nargs='?', const="True")
parser.add_argument("--migrate", "-mig", help="Migrate", nargs='?', const="True")

parser.add_argument("--status", "-st", help="git status on all modules", nargs='?', const="True")

parser.add_argument("--diff", "-df", help="git diff on all modules", nargs='?', const="True")



args=parser.parse_args()

mvnBuildCommand = []

gitAddAllCommand = ['git', 'add', '-u']
gitCommitCommand = ['git', 'commit','--allow-empty', '-m', args.commitMessage]
gitPushCommand = ['git', 'push', 'origin', branch]
gitStatusCommand = ['git', 'status']
gitDiffCommand = ['git', '--no-pager', 'diff']

if args.mvnCleanInstall is not None:
    print("Maven Clean Install")
    mvnBuildCommand = ['mvn', 'clean', 'install', '-Dgpg.skip=true']
elif args.mvnCleanInstallSkipTests is not None:
    print("Skipping Tests and Javadoc build")
    mvnBuildCommand = ['mvn', 'clean', 'install', '-DskipTests', '-Dgpg.skip=true', '-Dmaven.javadoc.skip=true']

if args.gitBaseDir is not None:
    gitBaseDir = args.gitBaseDir
elif  git_base_dir is not None:
    gitBaseDir = git_base_dir
else:
    gitBaseDir=os.getcwd()
  

print("Git Base Directory: " + gitBaseDir)

module_start_index=int(args.moduleIndex) - 1
modules_to_build=modules_paths_list_in_order[module_start_index::]

repo_start_index=int(args.repoIndex) - 1
git_repos=git_repos_in_order[repo_start_index::]


def buildAll():
    for i, module in enumerate(modules_to_build):
        buildModule(i, module)
        
def listModules():
    print("List of modules:")
    for i, module in enumerate(modules_to_build):
        print("[" + str(i + 1) + "/" + str(len(modules_to_build))  + "]: " + module)
        
def listGitRepos():
    print("List of Git Repositoris:")
    for i, module in enumerate(git_repos):
        print("[" + str(i + 1) + "/" + str(len(git_repos))  + "]: " + module)

def buildModule(index, modulePath):
    print(">>>>>>> Building module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    runCommand(mvnBuildCommand, moduleFullPath)
   
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
    
    
def getFullPath(relativePath):
    return gitBaseDir + '/' + relativePath
    
def runCommand(command, moduleFullPath):
    subprocess.run(command, cwd=moduleFullPath, shell=True, check=True)


# Function to replace text in a file
def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(filedata)

def replace_text_in_folder(folder_path, old_text, new_text, file_extension):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(folder_path, filename)
            # Check if it's a file
            if os.path.isfile(file_path):
                replace_text_in_file(file_path, old_text, new_text)

    # Print a success message
    print(f"Replaced '{old_text}' with '{new_text}' in all '{file_extension}' files within '{folder_path}'.")

def migratePoms():
    print(">>>>>>> Migrating POMs")
    for i, module in enumerate(modules_to_build):
        migratePomsInModule(i, module)
        
def migratePomsInModule(index, modulePath):
    print(">>>>>>> Migrating POM in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    for key,value in pom_changes_dict.items():
        replace_text_in_folder(moduleFullPath, key, value, "pom.xml")

def migrateJavaFiles():
    print(">>>>>>> Migrating Java Files")
    for i, module in enumerate(modules_to_build):
        migrateJavaFilesInModule(i, module)
        
def migrateJavaFilesInModule(index, modulePath):
    print(">>>>>>> Migrating Java files in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    
    for key,value in java_file_changes_dict.items():
        replace_text_in_folder(moduleFullPath, key, value, ".java")


def migrate():
    print(f"Migrating to Java 21")
    migratePoms()
    migrateJavaFiles();

def main():

    print("Args: " + str(args))

    if args.migrate is not None:
        migrate();
        
    if len(mvnBuildCommand) > 0:
        buildAll()
        print(">>>>>>> Build completed.")
        
    if args.add is not None or args.commit is not None or args.pushToOrigin is not None:
        addCommitAndPushAll()
        print(">>>>>>> Commit completed.")
    
    if args.addCommitAndPushToOrigin is not None:
        args.add = True
        args.commit = True
        args.pushToOrigin = True
        addCommitAndPushAll()
        print(">>>>>>> Commit and Push to Origin completed.")
        
    if args.listModules is not None:
        listModules()
        
    if args.listGitRepos is not None:
        listGitRepos()
        
    if args.status is not None:
        gitStatusRepos()
        
    if args.diff is not None:
        gitDiffRepos()


main()
