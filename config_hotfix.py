from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
repositories = OrderedDict({ \
"resevo-parent": "hotfix/RESEVO-4.259", "resevo-domain-lib": "hotfix/RESEVO-4.259", "resevo-core-lib": "hotfix/RESEVO-4.259", \
"resevo-context-lib": "hotfix/RESEVO-4.259", "resevo-messaging-lib": "hotfix/RESEVO-4.259", \
"resevo-saga-lib": "hotfix/RESEVO-4.259", "resevo-rule-lib": "hotfix/RESEVO-4.259", "resevo-testsupport-lib": "hotfix/RESEVO-4.259", \
"resevo-apigw-service": "hotfix/RESEVO-4.259", "resevo-booking-service": "hotfix/RESEVO-4.259", \
"resevo-db-manager": "master", "resevo-discovery-service": "hotfix/RESEVO-4.259", "resevo-freightbooking-service": "hotfix/RESEVO-4.259", \
"resevo-freightcompany-service": "hotfix/RESEVO-4.259", "resevo-freightpricing-service": "hotfix/RESEVO-4.259", "resevo-integration-service": "hotfix/RESEVO-4.259", \
"resevo-notification-service": "hotfix/RESEVO-4.259", "resevo-payment-service": "hotfix/RESEVO-4.259", \
"resevo-piletfeed-service": "hotfix/RESEVO-4.259", "resevo-port-service": "hotfix/RESEVO-4.259","resevo-pricing-service": "hotfix/RESEVO-4.259", \
"resevo-reportprint-service": "hotfix/RESEVO-4.259", "resevo-sbadmin-service": "hotfix/RESEVO-4.259", "resevo-ship-service": "hotfix/RESEVO-4.259", \
"resevo-testrunnere2e-app": "feature/cucumber", "resevo-user-service": "hotfix/RESEVO-4.259", \
"resevo-voy-service": "hotfix/RESEVO-4.259", "resevo-config-service": "master", "resevo-cart-lib": "hotfix/RESEVO-4.259", \
"resevo-policies-lib": "hotfix/RESEVO-4.259", "reservation-cgi": "master","resevo-api-collections": "main", "resevo-cast": "hotfix/RESEVO-4.259", \
"resevo-devops": "master", "resevo-eid-service": "hotfix/RESEVO-4.259", "resevo-regulatory-service": "hotfix/RESEVO-4.259"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-cast", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []