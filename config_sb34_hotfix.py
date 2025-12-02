from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\resevo-sb34"

# Repositories and their branches to git-pull + to mvn install
hotfix_branch = "hotfix/RESEVO-5.424"
hotfix_lib_branch = "hotfix/2.130.0"
repositories = OrderedDict({ \
"resevo-parent": hotfix_branch, "resevo-parent-lib": hotfix_lib_branch, "resevo-domain-lib": hotfix_lib_branch, "resevo-core-lib": hotfix_lib_branch, \
"resevo-context-lib": hotfix_lib_branch, "resevo-messaging-lib": hotfix_lib_branch, "resevo-saga-lib": hotfix_lib_branch, "resevo-rule-lib": hotfix_lib_branch, \
"resevo-testsupport-lib": hotfix_lib_branch, "resevo-cart-lib": hotfix_lib_branch, "resevo-policies-lib": hotfix_lib_branch, \
"resevo-apigw-service": hotfix_branch, "resevo-booking-service-sb34": hotfix_branch, "resevo-discovery-service": hotfix_branch, \
"resevo-freightbooking-service-sb34": hotfix_branch, "resevo-freightcompany-service-sb34": hotfix_branch, "resevo-freightpricing-service-sb34": hotfix_branch, \
"resevo-integration-service": hotfix_branch, "resevo-notification-service": hotfix_branch, "resevo-port-service": hotfix_branch, \
"resevo-pricing-service": hotfix_branch, "resevo-reportprint-service": hotfix_branch, "resevo-sbadmin-service": hotfix_branch, "resevo-ship-service": hotfix_branch, \
"resevo-user-service-sb34": hotfix_branch, "resevo-voy-service": hotfix_branch, "resevo-payment-service-sb34": hotfix_branch, "resevo-regulatory-service": hotfix_branch, \
"resevo-api-collections": "main", "resevo-devops": "master", "resevo-eid-service": "develop"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "resevo-api-collections", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []

# maven custom settings file
mvn_settings = "C:\\Users\\iTuna\\.m2\\settings_sb34.xml"
mvn_compiler = "C:\\Users\\iTuna\\.jdks\\openjdk-22.0.1\\bin\\javac.exe"