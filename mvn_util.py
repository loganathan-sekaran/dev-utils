import os
from config import modules_paths_list_in_order, git_base_dir
import argparse
from common_util import CommonUtil

parser=argparse.ArgumentParser()

parser.add_argument("--gitBaseDir", "-gbd", help="Git Base Directory", default=None)
parser.add_argument("--mvnCleanInstall", "-mci", help="Maven Clean Install", nargs='?', const="True")
parser.add_argument("--mvnCleanInstallSkipTests", "-mcist", help="Maven Clean Install with Skip tests and javadoc in build", nargs='?', const="True")
parser.add_argument("--listModules", "-lsm", help="List Modules", nargs='?', const="True")
parser.add_argument("--startIndex", "-si", help="The start index of module from which build to start", default=1, nargs='?', const="True")
parser.add_argument("--index", "-i", help="The index of module from which specifically needs to be built", default=None, nargs='?', const="True")


args=parser.parse_args()

util = CommonUtil(args)
modules_to_build=util.modules_to_build

mvnBuildCommand = []


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

if args.index is None:
    module_start_index=int(args.startIndex) - 1
    modules_to_build=modules_paths_list_in_order[module_start_index::]
else:
    index = int(args.index) - 1
    modules_to_build=[modules_paths_list_in_order[index]]

def buildAll():
    for i, module in enumerate(modules_to_build):
        buildModule(i, module)

def buildModule(index, modulePath):
    print(">>>>>>> Building module [" + str(index + 1) + "/" + str(len(modules_to_build))  + "]: " + modulePath)
    moduleFullPath=util.getFullPath(modulePath)
    util.runCommand(mvnBuildCommand, moduleFullPath)


def main():

    print("Args: " + str(args))
        
    if len(mvnBuildCommand) > 0:
        buildAll()
        print(">>>>>>> Build completed.")
        
    if args.listModules is not None:
        util.listModules()


main()
