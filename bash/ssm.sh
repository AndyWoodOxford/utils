#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

cwd=$(cd "$(dirname "${0}")" && pwd)
# See https://www.shellcheck.net/wiki/SC1091 (or, use 'shellcheck -x')
# shellcheck source=/dev/null
source "${cwd}/coloured-text.bash"

fn_usage() {
  echo
  echo "Wrapper for the AWS System Manager SSM agent used to connect to EC2 instances."
  echo
  echo "Assumes that the AWS CLI is available and that sufficient programmatic credentials"
  echo "(either as environment variables or a named configuration profile) are available."
  echo
  fn_print_warning "Usage:"
  fn_print_warning "  $0 [-l]"
  fn_print_warning "  $0 [-dqprv] INSTANCE_ID"
  fn_print_warning "  $0 [-dqprv] INSTANCE_NAME_TAG"
  echo
  echo -e  "\033[1;36m""Options${COLOUR_OFF}"
  fn_print_tabbed_message "-d             Dry run mode (no actual connection is made)"
  fn_print_tabbed_message "-h             Show this usage message and exit"
  fn_print_tabbed_message "-q             Quiet mode"
  fn_print_tabbed_message "-p PROFILE     AWS profile [${DEFAULT_AWS_PROFILE}]"
  fn_print_tabbed_message "-r REGION      AWS region [${DEFAULT_AWS_REGION}]"
  fn_print_tabbed_message "-v             Verbose mode"
  echo
  echo -e "The ${BWHITE}-q${COLOUR_OFF} and ${BWHITE}-v${COLOUR_OFF} arguments are mutually exclusive."
  echo
  echo -e "${BWHITE}TODO${COLOUR_OFF} Note on ASG instances / instance id argument."
  echo
}

function fn_check_env_var() {
  local message=$1
  local env_var=$2
  if [[ -z "${env_var}" ]]
  then
    fn_print_error "ERROR: ${message}"
    exit 1
  fi
}

############
# ENTRY

DEFAULT_AWS_PROFILE="default"
DEFAULT_AWS_REGION="eu-west-2"
