from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\resevo-sb34"

# Repositories and their branches to git-pull + to mvn install
repositories = OrderedDict({ \
"resevo-parent": "develop", "resevo-parent-lib": "develop", "resevo-domain-lib": "develop", "resevo-core-lib": "develop", "resevo-context-lib": "develop", \
"resevo-messaging-lib": "develop", "resevo-saga-lib": "develop", "resevo-rule-lib": "develop", "resevo-testsupport-lib": "develop", "resevo-cart-lib": "develop", \
"resevo-policies-lib": "develop", \
"resevo-apigw-service": "develop", "resevo-booking-service-sb34": "develop", "resevo-discovery-service": "develop", \
"resevo-freightbooking-service-sb34": "develop", "resevo-freightcompany-service-sb34": "develop", "resevo-freightpricing-service-sb34": "develop", \
"resevo-integration-service": "develop", "resevo-notification-service": "develop", "resevo-port-service": "develop", "resevo-pricing-service": "develop", \
"resevo-reportprint-service": "develop", "resevo-sbadmin-service": "develop", "resevo-ship-service": "develop", "resevo-user-service-sb34": "develop", \
"resevo-payment-service-sb34": "develop", "resevo-voy-service": "develop", "resevo-regulatory-service": "develop", \
"resevo-api-collections": "main", "resevo-devops": "master", "resevo-eid-service": "develop"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "resevo-api-collections", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []

# maven custom settings file
mvn_settings = "C:\\Users\\iTuna\\.m2\\settings_sb34.xml"
mvn_compiler = "C:\\Users\\iTuna\\.jdks\\openjdk-22.0.1\\bin\\javac.exe"