# java-migration-utility
Java Migration utility from Java 11 to Java 21

Usage:
````
usage: java-migration-util.py [-h] [--gitBaseDir GIT_BASE_DIR]
                              [--listModules]
                              [--listGitRepos]
                              [--startIndex [START_INDEX]] [--index [INDEX]]
                              [--migrate]
                              [--fetchMerge] [--status]
                              [--diff]
                              [--mvnCleanInstall]
                              [--mvnCleanInstallSkipTests]
                              [--addCommitAndPushToOrigin]
                              [--add] [--commit]
                              [--commitMessage COMMIT_MESSAGE]
                              [--pushToOrigin]

options:
  -h, --help            show this help message and exit
  --gitBaseDir GIT_BASE_DIR, -gbd GIT_BASE_DIR
                        Git Base Directory
  --listModules, -lsm
                        List Modules
  --listGitRepos, -lsr
                        List Git Repos
  --startIndex [START_INDEX], -si [START_INDEX]
                        The start index of module from which build to start
  --index [INDEX], -i [INDEX]
                        The index of module from which specifically needs to
                        be built
  --migrate, -mig
                        Migrate
  --fetchMerge, -fm
                        Fetch upstream and merge develop-java21 branch
  --status, -st
                        git status on all modules
  --diff, -df
                        git diff on all modules
  --mvnCleanInstall, -mci
                        Maven Clean Install
  --mvnCleanInstallSkipTests, -mcist
                        Maven Clean Install with Skip tests and javadoc in
                        build
  --addCommitAndPushToOrigin, -acp
                        Add changes, commit and push to origin
  --add, -ad
                        Add changes
  --commit, -cm
                        Commit
  --commitMessage COMMIT_MESSAGE, -m COMMIT_MESSAGE
                        Commit and push to origin
  --pushToOrigin, -po
                        push to origin

````
