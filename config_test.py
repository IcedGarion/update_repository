from collections import OrderedDict

# Main directory containing all the projects
repo_main_dir = "C:\\Users\\iTuna\\Desktop\\ADESSO\\GNV\\RESEVO\\repository"

# Repositories and their branches to git-pull + to mvn install
repositories = OrderedDict({ \
"resevo-parent": "develop"
})

# Repositories to not mvn-install (not maven projects)
mvn_exclusions = [ "reservation-cgi", "resevo-api-collections", "resevo-cast", "resevo-devops", "resevo-eid-service", "resevo-project"]

# Repositories you want to manually exclude
blacklist = []