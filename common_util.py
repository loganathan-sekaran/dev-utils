import subprocess
import os
from config import git_base_dir,modules_paths_list_in_order
from collections import OrderedDict


class CommonUtil:
    def __init__(self, args):
        if args.gitBaseDir is not None:
            self.gitBaseDir = args.gitBaseDir
        elif  git_base_dir is not None:
            self.gitBaseDir = git_base_dir
        else:
            self.gitBaseDir=None
                    
        if args.index is None:
            module_start_index=int(args.startIndex) - 1
            self.modules_to_build=modules_paths_list_in_order[module_start_index::]
        else:
            index = int(args.index) - 1
            self.modules_to_build=[modules_paths_list_in_order[index]]
            
        self.gitRepos=set(self.getGitRepos(self.modules_to_build))
        self.modules_to_build = list(OrderedDict.fromkeys([m for m in self.modules_to_build if self.check_pom_exists(m)]))
        
        
    def check_pom_exists(self, module_path):
        pom_path = (self.gitBaseDir+ '/' + module_path + "/" + 'pom.xml').replace('\\', '/')
        return os.path.isfile(pom_path)

            
    def getGitRepos(self, modules_paths_list):
        # Initialize an empty list to store distinct values in order
        gitRepos = []
    
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
                gitRepos.append(first_part)
                seen_values.add(first_part)
    
        # Return the list
        return gitRepos

    def listModules(self):
        print("List of modules:")
        for i, module in enumerate(self.modules_to_build):
            print("[" + str(i + 1) + "/" + str(len(self.modules_to_build))  + "]: " + module)
            
    def listGitRepos(self):
        print("List of Git Repositoris:")
        for i, module in enumerate(self.gitRepos):
            print("[" + str(i + 1) + "/" + str(len(self.gitRepos))  + "]: " + module)
    
    def getFullPath(self, relativePath):
        return self.gitBaseDir + '/' + relativePath
        
    def runCommand(self, command, moduleFullPath):
        subprocess.run(command, cwd=moduleFullPath, shell=True, check=True)
