from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
hotfix_branch = "hotfix/RESEVO-4.1309"
hotfix_lib_branch = "hotfix/RESEVO-4.1309"
repositories = OrderedDict({ \
"resevo-parent": hotfix_branch, "resevo-domain-lib": hotfix_lib_branch, "resevo-core-lib": hotfix_lib_branch, "resevo-context-lib": hotfix_lib_branch, \
"resevo-messaging-lib": hotfix_lib_branch, "resevo-saga-lib": hotfix_lib_branch, "resevo-rule-lib": hotfix_lib_branch, "resevo-testsupport-lib": hotfix_lib_branch, \
"resevo-cart-lib": hotfix_branch, "resevo-policies-lib": hotfix_branch, \
"resevo-db-manager": "master", "resevo-testrunnere2e-app": "feature/cucumber", "resevo-config-service": "master", \
"reservation-cgi": "master","resevo-api-collections": "main", "resevo-devops": "master"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-devops", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []

# maven custom settings file
mvn_settings = "C:\\Users\\iTuna\\.m2\\settings.xml"
mvn_compiler = "C:\\Users\\iTuna\\.jdks\\jdk-17.0.2\\bin\\javac.exe"