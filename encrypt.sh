#!/bin/bash

set -xe

FOLDER="lsf"
TARGET=$1

#
# Start with a fresh KEYRING
#
TEMPORARY_GNUPG_HOME="$(mktemp -d)"
export LC_ALL=en_US.UTF-8

# Import our keys #
RECPIENT_KEYS="public_recipient_keys/"
# Make sure you are at lsf-jenkins-config/
gpg --home="${TEMPORARY_GNUPG_HOME}" --import ${RECPIENT_KEYS}/*

# Retrieve most recent SEEDing key, used for credential decryption on CPEs end
# argument k is passed as curl (by default) doesn't accept websites without certificate verification. India folks need this.
curl -k https://ci.z.westeurope.blue-yonder.cloud/seed/${FOLDER}.asc -o "${TEMPORARY_GNUPG_HOME}/seedjob_pub_key.asc"
gpg --home="${TEMPORARY_GNUPG_HOME}" --import "${TEMPORARY_GNUPG_HOME}/seedjob_pub_key.asc"

#
# Perform encryption
#
gpg --home="${TEMPORARY_GNUPG_HOME}" --always-trust --multifile --encrypt $(gpg --home="${TEMPORARY_GNUPG_HOME}" --list-keys --with-colons | awk -F: '/^pub/{printf "-r %s ", $5}') ${TARGET}

#
# Perform cleanup
#
rm -rf "${FOLDER}.asc"
#rm -rf ${TARGET}