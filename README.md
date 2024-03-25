# java-migration-utility
Java Migration utility from Java 11 to Java 21

# To get command line usage
```
python java-migration-util.py -h
```

# To migrate
1. Update `migration_config.py` to configure the `git_base_dir`, `modules_paths_list_in_order` and `git_repos_in_order`. Optionally configure `branch` to perform bulk code commit and push.
2. Run command to apply the changes to the pom, java files, dockers and push triggers.
````
python java-migration-utility.py --migrate
````
