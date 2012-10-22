#!/bin/bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
echo "This script must be run as root" 1>&2
    exit 1
fi

# Need to have environment right for bitnami
. /opt/bitnami/scripts/setenv.sh

# Load configuration
. /etc/route53/config

# Export access key ID and secret for cli53
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

# Use command line scripts to get hostname and public hostname
HOSTNAME_FULL=`cat /etc/hostname`
HOSTNAME_PART=${HOSTNAME_FULL%%.$ZONE}
PUBLIC_HOSTNAME=$(ec2metadata | grep 'public-hostname:' | cut -d ' ' -f 2)

# Create a new CNAME record on Route 53, replacing the old entry if nessesary
cli53 rrcreate "$ZONE" "$HOSTNAME_PART" CNAME "$PUBLIC_HOSTNAME" --replace --ttl "$TTL"

