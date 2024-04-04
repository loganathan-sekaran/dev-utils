import os
import subprocess
import sys
from migration_config import modules_paths_list_in_order, git_base_dir, branch
from text_changes import pom_changes_dict, java_file_changes_dict, docker_file_changes_dict, push_trigger_changes_dict
import argparse
import pom_migrator

parser=argparse.ArgumentParser()

parser.add_argument("--mvnCleanInstall", "-mci", help="Maven Clean Install", nargs='?', const="True")
parser.add_argument("--mvnCleanInstallSkipTests", "-mcist", help="Maven Clean Install with Skip tests and javadoc in build", nargs='?', const="True")
parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--addCommitAndPushToOrigin", "-acp", help="Add changes, commit and push to origin", nargs='?', const="True")
parser.add_argument("--add", "-ad", help="Add changes", nargs='?', const="True")
parser.add_argument("--commit", "-cm", help="Commit", nargs='?', const="True")
parser.add_argument("--pushToOrigin", "-po", help="push to origin", nargs='?', const="True")
parser.add_argument("--commitMessage", "-m", help="Commit and push to origin", default='Committing changes.')
parser.add_argument("--listModules", "-lsm", help="List Modules", nargs='?', const="True")
parser.add_argument("--listGitRepos", "-lsr", help="List Git Repos", nargs='?', const="True")
parser.add_argument("--index", "-i", help="The index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--migrate", "-mig", help="Migrate", nargs='?', const="True")

parser.add_argument("--status", "-st", help="git status on all modules", nargs='?', const="True")

parser.add_argument("--diff", "-df", help="git diff on all modules", nargs='?', const="True")



args=parser.parse_args()

mvnBuildCommand = []

gitAddAllCommand = ['git', 'add', '-u']
gitCommitCommand = ['git', 'commit', '-s', '--allow-empty', '-m', args.commitMessage]
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

module_start_index=int(args.index) - 1
modules_to_build=modules_paths_list_in_order[module_start_index::]


def getGitRepos(modules_paths_list):
    # Initialize an empty list to store distinct values in order
    git_repos = []

    # Initialize a set to keep track of seen values
    seen_values = set()

    # Iterate over each element in the list
    for module_path in modules_paths_list:
        # Split the element by '/'
        parts = module_path.split('/')
        # Get the first part
        first_part = parts[0]
        # If it's not seen before, add it to the list and set
        if first_part not in seen_values:
            git_repos.append(first_part)
            seen_values.add(first_part)

    # Return the list
    return git_repos


git_repos=getGitRepos(modules_to_build)


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
    with open(file_path, 'r', encoding="utf8", errors="ignore") as file:
        filedata = file.read()
    filedata = filedata.replace(old_text, new_text)
    with open(file_path, 'w', encoding="utf8", errors="ignore") as file:
        file.write(filedata)

def replace_text_in_folder(folder_path, old_text, new_text, file_extension):
    iterate_files_in_folder_and_apply(folder_path, file_extension, lambda file_path: replace_text_in_file(file_path, old_text, new_text))
    # Print a success message
    print(f"Replaced '{old_text}' with '{new_text}' in all '{file_extension}' files within '{folder_path}'.")

def processPomsInFolder(folder_path):
    iterate_files_in_folder_and_apply(folder_path, "pom.xml", lambda file_path: pom_migrator.addKernelBomToDependencyMgnt(file_path))
    # Print a success message
    print(f"Added kernel-bom dependency in all 'pom.xml' files within '{folder_path}'.")
                
def iterate_files_in_folder_and_apply(folder_path, file_extension, func):
    # Iterate over all files in the folder
    #print("Working on folder : " + folder_path + " for file ending with: " + file_extension)
    for resname in os.listdir(folder_path):
        res_path = os.path.join(folder_path, resname)
        # Check if it's a file
        if os.path.isfile(res_path):
           # print("Located file: " + res_path)
            if resname.endswith(file_extension):
                #print("Working on file : " + res_path)
                func(res_path)
        elif os.path.isdir(res_path):
            #print("Located folder : " + res_path)
            iterate_files_in_folder_and_apply(res_path, file_extension, func)

def migratePoms():
    print(">>>>>>> Migrating POMs")
    for i, module in enumerate(modules_to_build):
        migratePomsInModule(i, module)
        
def migratePomsInModule(index, modulePath):
    print(">>>>>>> Migrating POM in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    for key,value in pom_changes_dict.items():
        replace_text_in_folder(moduleFullPath, key, value, "pom.xml")
    
    #processPomsInFolder(moduleFullPath)


def migrateJavaFiles():
    print(">>>>>>> Migrating Java Files")
    for i, module in enumerate(modules_to_build):
        migrateJavaFilesInModule(i, module)
        
def migrateJavaFilesInModule(index, modulePath):
    print(">>>>>>> Migrating Java files in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    
    for key,value in java_file_changes_dict.items():
        replace_text_in_folder(moduleFullPath, key, value, ".java")
        
def migrateDockerFiles():
    print(">>>>>>> Migrating Docker Files")
    for i, module in enumerate(modules_to_build):
        migrateDockerFilesInModule(i, module)
        
def migrateDockerFilesInModule(index, modulePath):
    print(">>>>>>> Migrating Docker files in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getFullPath(modulePath)
    
    for key,value in docker_file_changes_dict.items():
        replace_text_in_folder(moduleFullPath, key, value, "Dockerfile")


def migratePushTriggerFiles():
    print(">>>>>>> Migrating Java Files")
    for i, module in enumerate(git_repos):
        migratePushTriggerFilesInRepos(i, module)
        
def migratePushTriggerFilesInRepos(index, repoPath):
    print(">>>>>>> Migrating push trigger files in git repo [" + str(index + 1) + "/" + str(len(git_repos))  + "]: " + repoPath)
    workflowFullPath=getFullPath(repoPath) + "/.github/workflows"
    
    for key,value in push_trigger_changes_dict.items():
        replace_text_in_folder(workflowFullPath, key, value, ".yml")

def migrate():
    print(f"Migrating to Java 21")
    migratePoms()
    migrateJavaFiles();
    migrateDockerFiles();
    migratePushTriggerFiles();

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
