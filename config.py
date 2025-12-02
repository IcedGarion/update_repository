from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
repositories = OrderedDict({ \
"resevo-parent": "develop", "resevo-domain-lib": "develop", "resevo-core-lib": "develop", "resevo-context-lib": "develop", "resevo-messaging-lib": "develop", \
"resevo-saga-lib": "develop", "resevo-rule-lib": "develop", "resevo-testsupport-lib": "develop", "resevo-cart-lib": "develop", "resevo-policies-lib": "develop", \
"resevo-db-manager": "master", "resevo-testrunnere2e-app": "feature/cucumber", "resevo-config-service": "master", \
"reservation-cgi": "master", "resevo-api-collections": "main", "resevo-devops": "master"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-devops", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []

# maven custom settings file
mvn_settings = "C:\\Users\\iTuna\\.m2\\settings.xml"
mvn_compiler = "C:\\Users\\iTuna\\.jdks\\jdk-17.0.2\\bin\\javac.exe"