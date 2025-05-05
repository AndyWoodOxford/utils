#!/usr/bin/env bash

#------------------------------------------------------------------------------
# Template for a bash shell script. Basic short-form args are provided.
# This template does not emit any shellcheck warnings.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
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

#------------------------------------------------------------------------------
# Usage. This code uses functions from "coloured-text.bash".
#------------------------------------------------------------------------------

function fn_usage() {
  echo
  echo "This script does something useful."
  echo
  fn_print_warning "Usage: $0 [-ahqv]"
  echo
  fn_print_tabbed_message "-a  VALUE  Argument taking a value [${DEFAULT_ARGUMENT}]"
  fn_print_tabbed_message "-h         Show this usage message and exit"
  fn_print_tabbed_message "-q         Quiet mode"
  fn_print_tabbed_message "-v         Verbose mode"
  echo
}

#------------------------------------------------------------------------------
# Short-form arguments and defaults
#------------------------------------------------------------------------------

DEFAULT_ARGUMENT="hello"

argument="${DEFAULT_ARGUMENT}"
quiet_mode=false
verbose_mode=false
while getopts "a:hqv" opt; do
  case "${opt}" in
  a)
    argument=$OPTARG
    ;;
  h | \?)
    fn_usage
    exit 0
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

# Arbitrary usage of args to avoid shellcheck warnings against the template
echo "${argument}" "${quiet_mode}" "${verbose_mode}" >/dev/null
