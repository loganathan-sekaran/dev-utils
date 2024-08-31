# dev-utils
* This contains “mvn_util” Python based util that can do batch maven build, of multiple modules across multiple repositories. 
* This also contain “git_util” Python based utility that can do batch git fetch, merge, add to index, commit, push across multiple git repositories together.  
* This also contains “migarte-util” that will help the effort needed in Java 21 migration by automating many textual changes in the Java 11 code in Springboot applications.

## mvn_util Usage:
mvn_util.py [-h] [--gitBaseDir GITBASEDIR]
                   [--mvnCleanInstall [MVNCLEANINSTALL]]
                   [--mvnCleanInstallSkipTests [MVNCLEANINSTALLSKIPTESTS]]
                   [--listModules [LISTMODULES]] [--startIndex [STARTINDEX]]
                   [--index [INDEX]]

options:
  -h, --help            show this help message and exit
  --gitBaseDir GITBASEDIR, -gbd GITBASEDIR
                        Git Base Directory
  --mvnCleanInstall [MVNCLEANINSTALL], -mci [MVNCLEANINSTALL]
                        Maven Clean Install
  --mvnCleanInstallSkipTests [MVNCLEANINSTALLSKIPTESTS], -mcist [MVNCLEANINSTALLSKIPTESTS]
                        Maven Clean Install with Skip tests and javadoc in
                        build
  --listModules [LISTMODULES], -lsm [LISTMODULES]
                        List Modules
  --startIndex [STARTINDEX], -si [STARTINDEX]
                        The start index of module from which build to start
  --index [INDEX], -i [INDEX]
                        The comma separated indices of module from which
                        specifically needs to be built

## git-util Usage:
git_util.py [-h] [--gitBaseDir GITBASEDIR]
                   [--addModifiedCommitAndPushToOrigin [ADDMODIFIEDCOMMITANDPUSHTOORIGIN]]
                   [--addAllCommitAndPushToOrigin [ADDALLCOMMITANDPUSHTOORIGIN]]
                   [--fetchMerge [FETCHMERGE]] [--addModified [ADDMODIFIED]]
                   [--addAll [ADDALL]] [--commit [COMMIT]]
                   [--pushToOrigin [PUSHTOORIGIN]]
                   [--commitMessage COMMITMESSAGE]
                   [--listModules [LISTMODULES]]
                   [--listGitRepos [LISTGITREPOS]] [--startIndex [STARTINDEX]]
                   [--index [INDEX]] [--status [STATUS]] [--diff [DIFF]]
                   [--cdToRepoIndex [CDTOREPOINDEX]]

options:
  -h, --help            show this help message and exit
  --gitBaseDir GITBASEDIR, -gbd GITBASEDIR
                        Git Base Directory
  --addModifiedCommitAndPushToOrigin [ADDMODIFIEDCOMMITANDPUSHTOORIGIN], -amcp [ADDMODIFIEDCOMMITANDPUSHTOORIGIN]
                        Add changes, commit and push to origin
  --addAllCommitAndPushToOrigin [ADDALLCOMMITANDPUSHTOORIGIN], -aacp [ADDALLCOMMITANDPUSHTOORIGIN]
                        Add changes, commit and push to origin
  --fetchMerge [FETCHMERGE], -fm [FETCHMERGE]
                        Fetch upstream and merge develop-java21 branch
  --addModified [ADDMODIFIED], -adm [ADDMODIFIED]
                        Add modified files
  --addAll [ADDALL], -ada [ADDALL]
                        Add all tracked and untracked files
  --commit [COMMIT], -cm [COMMIT]
                        Commit
  --pushToOrigin [PUSHTOORIGIN], -po [PUSHTOORIGIN]
                        push to origin
  --commitMessage COMMITMESSAGE, -m COMMITMESSAGE
                        Commit and push to origin
  --listModules [LISTMODULES], -lsm [LISTMODULES]
                        List Modules
  --listGitRepos [LISTGITREPOS], -lsr [LISTGITREPOS]
                        List Git Repos
  --startIndex [STARTINDEX], -si [STARTINDEX]
                        The start index of module from which build to start
  --index [INDEX], -i [INDEX]
                        The index of module from which specifically needs to
                        be built
  --status [STATUS], -st [STATUS]
                        git status on all modules
  --diff [DIFF], -df [DIFF]
                        git diff on all modules
  --cdToRepoIndex [CDTOREPOINDEX], -cdi [CDTOREPOINDEX]
                        Command to change directory to the repo index

## migrate-util Usage:
````
migrate_util.py [-h] [--gitBaseDir GITBASEDIR]
                       [--listModules [LISTMODULES]]
                       [--listGitRepos [LISTGITREPOS]]
                       [--startIndex [STARTINDEX]] [--index [INDEX]]
                       [--migrate [MIGRATE]]

options:
  -h, --help            show this help message and exit
  --gitBaseDir GITBASEDIR, -gbd GITBASEDIR
                        Git Base Directory
  --listModules [LISTMODULES], -lsm [LISTMODULES]
                        List Modules
  --listGitRepos [LISTGITREPOS], -lsr [LISTGITREPOS]
                        List Git Repos
  --startIndex [STARTINDEX], -si [STARTINDEX]
                        The start index of module from which build to start
  --index [INDEX], -i [INDEX]
                        The index of module from which specifically needs to
                        be built
  --migrate [MIGRATE], -mig [MIGRATE]
                        Migrate

````
