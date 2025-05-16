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
  echo "Assumes that the AWS CLI and sufficient programmatic credentials (either as"
  echo "environment variables or a named configuration profile) are available."
  echo
  fn_print_warning "Usage:"
  fn_print_warning "  $0 [-l]"
  fn_print_warning "  $0 [-dqrv] INSTANCE_ID"
  fn_print_warning "  $0 [-dqrv] INSTANCE_NAME_TAG"
  echo
  echo -e  "\033[1;36m""Options${COLOUR_OFF}"
  fn_print_tabbed_message "-d          Dry run mode (no actual connection is made)"
  fn_print_tabbed_message "-h          Show this usage message and exit"
  fn_print_tabbed_message "-l          List instances (\"Name\" tags) and exit"
  fn_print_tabbed_message "-q          Quiet mode"
  fn_print_tabbed_message "-r REGION   AWS region [${DEFAULT_AWS_REGION}]"
  fn_print_tabbed_message "-v          Verbose mode"
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

fn_check_requirements() {
  (
    AWS=$(command -v aws)
    if [[ -z "${AWS:-}" ]]
    then
      fn_print_error "ERROR the AWS CLI was not found!"
      exit 1
    fi
  ) && true

  fn_check_env_var "${BWHITE}AWS_ACCESS_KEY_ID${COLOUR_OFF} is not defined" "${AWS_ACCESS_KEY_ID:-}"
  fn_check_env_var "${BWHITE}AWS_SECRET_ACCESS_KEY${COLOUR_OFF} is not defined" "${AWS_SECRET_ACCESS_KEY:-}"
}

fn_list_instances() {
  echo TODO
}

############
# ENTRY

DEFAULT_AWS_REGION="eu-west-2"

fn_check_requirements

# Parse command line
aws_region="${DEFAULT_AWS_REGION}"
dryrun_mode=false
list_mode=false
quiet_mode=false
verbose_mode=false
while getopts "dhlqr:v" opt; do
  case "${opt}" in
  d)
    dryrun_mode=true
    ;;
  h | \?)
    fn_usage
    exit 0
    ;;
  l)
    list_mode=true
    ;;
  q)
    quiet_mode=true
    ;;
  r)
    aws_region=$OPTARG
    ;;
  v)
    verbose_mode=true
    ;;
  [?])
    shift
    ;;
  esac
done

if [ "${list_mode}" ]
then
  fn_list_instances
  exit 0
fi

exit 0

