from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
repositories = OrderedDict({ \
"resevo-parent": "develop", "resevo-domain-lib": "develop", "resevo-core-lib": "develop", "resevo-context-lib": "develop", "resevo-messaging-lib": "develop", \
"resevo-saga-lib": "develop", "resevo-rule-lib": "develop", "resevo-testsupport-lib": "develop", "resevo-apigw-service": "develop", "resevo-booking-service": "develop", \
"resevo-db-manager": "master", "resevo-discovery-service": "develop", "resevo-freightbooking-service": "develop", "resevo-freightcompany-service": "develop", \
"resevo-freightpricing-service": "develop", "resevo-integration-service": "develop", "resevo-notification-service": "develop", "resevo-payment-service": "develop", \
"resevo-piletfeed-service": "develop", "resevo-port-service": "develop","resevo-pricing-service": "develop", "resevo-reportprint-service": "develop", \
"resevo-sbadmin-service": "develop", "resevo-ship-service": "develop", "resevo-testrunnere2e-app": "develop", "resevo-user-service": "develop", \
"resevo-voy-service": "develop", "resevo-config-service": "master", \
"reservation-cgi": "master","resevo-api-collections": "main", "resevo-cast": "develop","resevo-devops": "master", "resevo-eid-service": "develop"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-cast", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []