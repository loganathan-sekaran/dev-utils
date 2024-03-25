import os
import subprocess
import sys
from migration_config import modules_paths_list_in_order
from migration_config import git_base_dir
import argparse

parser=argparse.ArgumentParser()

parser.add_argument("--mvnCleanInstall", "-mci", help="Maven Clean Install", nargs='?', const="True")
parser.add_argument("--mvnCleanInstallSkipTests", "-mcist", help="Maven Clean Install with Skip tests and javadoc in build", nargs='?', const="True")
parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--commitAndPushToOrigin", "-cpo", help="Commit and push to origin", nargs='?', const="True")
parser.add_argument("--commitMessage", "-msg", help="Commit and push to origin", default='Committing changes.')
parser.add_argument("--listModules", "-ls", help="List Modules", nargs='?', const="True")
parser.add_argument("--buildFromIndex", "-i", help="The index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--migrate", "-mig", help="Migrate", nargs='?', const="True")

args=parser.parse_args()

mvnBuildCommand = []

gitAddAllCommand = ['git', 'add', '-u']
gitCommitCommand = ['git', 'commit','--allow-empty', '-m', args.commitMessage]
gitPushCommand = ['git', 'push', 'origin']

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

module_start_index=int(args.buildFromIndex) - 1
modules_to_build=modules_paths_list_in_order[module_start_index::]


def buildAll():
    for i, module in enumerate(modules_to_build):
        buildModule(i, module)
        
def listModules():
    print("List of modules:")
    for i, module in enumerate(modules_to_build):
        print("[" + str(i + 1) + "/" + str(len(modules_to_build))  + "]: " + module)

def buildModule(index, modulePath):
    print(">>>>>>> Building module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getModuleFullPath(modulePath)
    runCommand(mvnBuildCommand, moduleFullPath)
   
def pushAll():
    for i, module in enumerate(modules_to_build):
        pushModule(i, module)

def pushModule(index, modulePath):
    print(">>>>>>> Pushing module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getModuleFullPath(modulePath)
    print("Committing")
    runCommand(gitAddAllCommand, moduleFullPath)
    runCommand(gitCommitCommand, moduleFullPath)
    runCommand(gitPushCommand, moduleFullPath)
    
def getModuleFullPath(modulePath):
    return gitBaseDir + '/' + modulePath
    
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
    for i, module in enumerate(modules_to_build):
        migratePomInModule(i, module)
        
def migratePomInModule(index, modulePath):
    print(">>>>>>> Migrating POM in module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=getModuleFullPath(modulePath)
    replace_text_in_folder(moduleFullPath, "<maven.compiler.source>11</maven.compiler.source>", "<maven.compiler.source>21</maven.compiler.source>", "pom.xml")
    replace_text_in_folder(moduleFullPath, "<maven.compiler.target>11</maven.compiler.target>", "<maven.compiler.target>21</maven.compiler.target>", "pom.xml")
    replace_text_in_folder(moduleFullPath, "1.2.1-SNAPSHOT", "1.2.1-java21-SNAPSHOT", "pom.xml")

def migrate():
    print(f"Migrating to Java 21")
    migratePoms()

def main():

    print("Args: " + str(args))

    if args.migrate is not None:
        migrate();
        
    if len(mvnBuildCommand) > 0:
        buildAll()
        print(">>>>>>> Build completed.")
    
    if args.commitAndPushToOrigin is not None:
        pushAll()
        print(">>>>>>> Push to Origin completed.")
        
    if args.listModules is not None:
        listModules()


main()
