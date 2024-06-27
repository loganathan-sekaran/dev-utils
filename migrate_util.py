import argparse
import os
import subprocess

import pom_migrator
from text_changes import pom_changes_dict, java_file_changes_dict, docker_file_changes_dict, push_trigger_changes_dict
from common_util import CommonUtil


parser=argparse.ArgumentParser()

parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--listModules", "-lsm", help="List Modules", nargs='?', const="True")
parser.add_argument("--listGitRepos", "-lsr", help="List Git Repos", nargs='?', const="True")
parser.add_argument("--startIndex", "-si", help="The start index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--index", "-i", help="The index of module from which specifically needs to be built", default=None, nargs='?', const="True")
parser.add_argument("--migrate", "-mig", help="Migrate", nargs='?', const="True")

args=parser.parse_args()

util = CommonUtil(args)
modules_to_build=util.modules_to_build
gitBaseDir = util.gitBaseDir

print("Git Base Directory: " + gitBaseDir)


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
    if util.gitBaseDir is not None:
        for i, module in enumerate(util.git_repos):
            migratePushTriggerFilesInRepos(i, module)
        
def migratePushTriggerFilesInRepos(index, repoPath):
    if util.gitRepos is not None:
        print(">>>>>>> Migrating push trigger files in git repo [" + str(index + 1) + "/" + str(len(util.gitRepos))  + "]: " + repoPath)
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
    
    if args.listModules is not None:
        util.listModules()

    if args.migrate is not None:
        migrate();        
    
    if args.listGitRepos is not None:
        util.listGitRepos()


main()
