name "maint"
description "class2go maintenance node"

override_attributes \
    "system" => {
        "admin_user" => "ubuntu",
        "admin_group" => "ubuntu",
        "admin_home" => "/home/ubuntu"
    }

override_attributes \
    "main" => {
        "maint" => "True"
    }

run_list(
    "recipe[class2go-apt-update]",
    "recipe[class2go-base-ubuntu]",
    "recipe[class2go-apache]",
    "recipe[class2go-python]",
    "recipe[class2go-deploy]",
    "recipe[class2go-logging]",
    "recipe[class2go-ops-dns]",
    "recipe[class2go-database-config]",
)
