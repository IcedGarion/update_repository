from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
hotfix_branch = "hotfix/RESEVO-4.1309"
hotfix_lib_branch = "hotfix/RESEVO-4.1309"
repositories = OrderedDict({ \
"resevo-parent": hotfix_branch, "resevo-domain-lib": hotfix_lib_branch, "resevo-core-lib": hotfix_lib_branch, \
"resevo-context-lib": hotfix_lib_branch, "resevo-messaging-lib": hotfix_lib_branch, \
"resevo-saga-lib": hotfix_lib_branch, "resevo-rule-lib": hotfix_lib_branch, "resevo-testsupport-lib": hotfix_lib_branch, \
"resevo-apigw-service": hotfix_branch, "resevo-booking-service": hotfix_branch, \
"resevo-db-manager": "master", "resevo-discovery-service": hotfix_branch, \
"resevo-integration-service": hotfix_branch, \
"resevo-notification-service": hotfix_branch, "resevo-payment-service": hotfix_branch, \
"resevo-piletfeed-service": hotfix_branch, "resevo-pricing-service": hotfix_branch, \
"resevo-sbadmin-service": hotfix_branch, \
"resevo-testrunnere2e-app": "feature/cucumber", \
"resevo-config-service": "master", "resevo-cart-lib": hotfix_branch, \
"resevo-policies-lib": hotfix_branch, "reservation-cgi": "master","resevo-api-collections": "main", "resevo-cast": hotfix_branch, \
"resevo-devops": "master", "resevo-eid-service": hotfix_branch, "resevo-regulatory-service": hotfix_branch
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-cast", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []

# maven custom settings file
mvn_settings = "C:\\Users\\iTuna\\.m2\\settings.xml"
mvn_compiler = "C:\\Users\\iTuna\\.jdks\\jdk-17.0.2\\bin\\javac.exe"