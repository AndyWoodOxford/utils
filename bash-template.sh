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
# Pull in external code from a "functions" subfolder
#------------------------------------------------------------------------------

# The shellcheck tool cannot follow a non-constant source so need to ignore for each inclusion
cwd=$(cd "$(dirname "${0}")" && pwd)
# shellcheck source=/dev/null
source "${cwd}/functions/colours.bash"

#------------------------------------------------------------------------------
# Usage
#------------------------------------------------------------------------------

function fn_usage() {
  echo
  echo "This script does something useful."
  echo
  print_warning "Usage: $0 [-ahqv]"
  echo
  print_tabbed_message "-h   Show this usage message and exit"
  echo
}

#------------------------------------------------------------------------------
# Short-form arguments and defaults
#------------------------------------------------------------------------------

DEFAULT_ARGUMENT="hello"

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
