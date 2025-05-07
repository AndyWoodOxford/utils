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
}

#------------------------------------------------------------------------------
# Interrupt abort signal (also needs the 'trap' command below)
#------------------------------------------------------------------------------

# Signal handler appears as unreachable to shellcheck
# shellcheck disable=SC2317
function fn_aborted() {
  fn_print_warning "$0: Script aborted!!!"
  echo
  fn_print_warning "Warning e.g. Terraform state could be corrupted"
  exit 2
}

#------------------------------------------------------------------------------
# Short-form arguments and defaults
#------------------------------------------------------------------------------

DEFAULT_ARGUMENT="hello"

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

# Assert that the mandatory argument is defined (using a function) *NEXT*


# Arbitrary usage of args to avoid shellcheck warnings against the template
echo "${mandatory_arg}" "${optional_arg}" "${quiet_mode}" "${verbose_mode}" >/dev/null

#------------------------------------------------------------------------------
# Mandatory positional argument
#------------------------------------------------------------------------------
shift
echo COUNT = $#

#------------------------------------------------------------------------------
# Intercept abort signal

trap fn_aborted INT TERM
#------------------------------------------------------------------------------

sleep 5

exit 0