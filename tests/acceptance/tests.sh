#!/bin/bash
ACCOUNT=${1}
echo ${ACCOUNT}
ACCOUNT_ID=${ACCOUNT} pytest -vvvv -s tests/acceptance
