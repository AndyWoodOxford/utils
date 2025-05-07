#!/usr/bin/env bash

#------------------------------------------------------------------------------
# Template for a bash shell script. Basic short-form args are provided.
# This template does not emit any shellcheck warnings.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# "Strict Mode" (unset vars, quit upon errors, avoid masked pipeline errors)
#------------------------------------------------------------------------------

set -o nounset
set -o errexit
set -o pipefail

#------------------------------------------------------------------------------
# Pull in external code from the current folder
#------------------------------------------------------------------------------

# The shellcheck tool cannot follow a non-constant source so need to ignore for each inclusion
cwd=$(cd "$(dirname "${0}")" && pwd)
# shellcheck source=/dev/null
source "${cwd}/coloured-text.bash"

#---------------------------------------------------------------------------------------------
# Usage. This code uses functions from "coloured-text.bash" as well as hardwired colour macros
#---------------------------------------------------------------------------------------------

function fn_usage() {
  echo
  echo "This script does something useful."
  echo
  fn_print_warning "Usage: $0 [-ahqv] ARG"
  echo
  echo -e  "\033[1;36m""Positional arguments${COLOUR_OFF}"  # Bold Cyan
  fn_print_tabbed_message "ARG  argument (required)"
  echo
  echo -e  "\033[1;36m""Options${COLOUR_OFF}"
  fn_print_tabbed_message "-a  OPTIONAL   Optional argument [${DEFAULT_ARGUMENT}]"
  fn_print_tabbed_message "-h             Show this usage message and exit"
  fn_print_tabbed_message "-m  MANDATORY  Mandatory argument"
  fn_print_tabbed_message "-q             Quiet mode"
  fn_print_tabbed_message "-v             Verbose mode"
  echo
  echo -e "The ${BWHITE}MANDATORY${COLOUR_OFF} value must be one of the following:"
  fn_print_tabbed_message "${ALLOWED_MANDATORY_VALUES[*]}"
  echo
  echo -e "The ${BWHITE}-q${COLOUR_OFF} and ${BWHITE}-v${COLOUR_OFF} arguments are mutually exclusive."
  echo
}

#------------------------------------------------------------------------------
# Check that bash version supports associative arrays (v4 or above).
# Call is skipped since I am currently running 3.2.57.
#------------------------------------------------------------------------------

fn_check_bash_version() {
  BASH="$(command -v bash)"
  set +o errexit # read hits EOF and returns non-zero exit code
  IFS=$'\n' read -d '' -r -a bash_version_stdout < <("${BASH}" --version)
  set -o errexit
  bash_version_stdout_header="${bash_version_stdout[0]}"
  bash_version_full="${bash_version_stdout_header//GNU bash, version /}"
  bash_version_major="${bash_version_full:0:1}"
  if (( $(echo "${bash_version_major} < 4" | bc -l) ))
  then
    fn_print_error "ERROR! bash version 4 or higher is needed to run this script - found \"${bash_version_full}\""
    exit 1
  fi
}

false && fn_check_bash_version

#------------------------------------------------------------------------------
# Short-form arguments and defaults
#------------------------------------------------------------------------------

DEFAULT_ARGUMENT="hello"

ALLOWED_MANDATORY_VALUES=("foo" "bar")

optional_arg="${DEFAULT_ARGUMENT}"
mandatory_arg=
quiet_mode=false
verbose_mode=false
while getopts "a:hm:qv" opt; do
  case "${opt}" in
  a)
    optional_arg=$OPTARG
    ;;
  h | \?)
    fn_usage
    exit 0
    ;;
  m)
    mandatory_arg=$OPTARG
    ;;
  q)
    quiet_mode=true
    ;;
  v)
    verbose_mode=true
    ;;
  *)
    fn_usage
    ;;
  esac
done

# Assert that the mandatory argument is defined
if [[ -z "${mandatory_arg:-}" ]]
then
  fn_print_error "ERROR: the 'MANDATORY' arg must be defined ('-m' option)"
  exit 1
fi

# Assert that the mandatory argument is defined (using a function)
function fn_fail_if_missing() {
  local message=$1
  local string=$2
  if [[ -z "${string}" ]]
  then
    fn_print_error "ERROR: ${message}"
    exit 1
  fi
}

fn_fail_if_missing "${BRED}mandatory_arg${COLOUR_OFF} is not defined" "${mandatory_arg:-}"

# Assert that the mandatory argument has an allowed value
  if [[ ! "${ALLOWED_MANDATORY_VALUES[*]}" =~ ${mandatory_arg} ]]
  then
    fn_print_error "ERROR: \"${mandatory_arg}\" is not an allowed value."
    fn_usage
    exit 1
  fi

# Check for mutually exclusive options
if [[ "${quiet_mode}" = true ]] && [[ "${verbose_mode}" = true ]]
then
  fn_print_error "ERROR: the '-q' and '-v' options are mutually exclusive"
  exit 1
fi

#------------------------------------------------------------------------------
# Mandatory positional argument
#------------------------------------------------------------------------------
shift
echo COUNT = $#

# Arbitrary usage of args to avoid shellcheck warnings against the template
echo "${mandatory_arg}" "${optional_arg}" "${quiet_mode}" "${verbose_mode}" >/dev/null

#------------------------------------------------------------------------------
# Intercept abort signal
#------------------------------------------------------------------------------

# Signal handler appears as unreachable to shellcheck
# shellcheck disable=SC2317
function fn_aborted() {
  fn_print_warning "$0: Script aborted!!!"
  echo
  fn_print_warning "Warning e.g. Terraform state could be corrupted"
  exit 2
}

trap fn_aborted INT TERM
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Measuring the elapsed running time
#------------------------------------------------------------------------------

function fn_goodbye() {
  local started_at=$1

  ended_at=$(date +%s)
  running_time=$((ended_at - started_at))
  echo
  echo -e "Total running time was ${GREEN}${running_time}${COLOUR_OFF} seconds. Goodbye!"
  echo
  exit 0
}

started_at=$(date +%s)
sleep 2
fn_goodbye "${started_at}"
