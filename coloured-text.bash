#!/usr/bin/env bash

# A collection of macros that can be used in ANSI escape sequences to generate coloured text.
#
# Includes a selection of functions for canned formatting, e.g. warnings.
#
# Including these macros and functions in a bash script (assuming a "functions" subfolder):
#
#   cwd=$(cd "$(dirname "${0}")" && pwd)
#   source "${cwd}/functions/colours.bash"
#
# To avoid shellcheck warnings, insert this comment immediately before the source command:
#   # shellcheck source=/dev/null

#------------------------------------------------------------------------------
# Macros
#------------------------------------------------------------------------------

# Reset
COLOUR_OFF='\033[0m'

export COLOUR_OFF

# Regular
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'

export BLACK RED GREEN YELLOW BLUE PURPLE CYAN WHITE

# Bold
BBLACK='\033[1;30m'
BRED='\033[1;31m'
BGREEN='\033[1;32m'
BYELLOW='\033[1;33m'
BBLUE='\033[1;34m'
BPURPLE='\033[1;35m'
BCYAN='\033[1;36m'
BWHITE='\033[1;37m'

export BBLACK BRED BGREEN BYELLOW BBLUE BPURPLE BCYAN BWHITE

# Bold High Intensity
BIBLACK='\033[1;90m'
BIRED='\033[1;91m'
BIGREEN='\033[1;92m'
BIYELLOW='\033[1;93m'
BIBLUE='\033[1;94m'
BIPURPLE='\033[1;95m'
BICYAN='\033[1;96m'
BIWHITE='\033[1;97m'

export BIBLACK BIRED BIGREEN BIYELLOW BIBLUE BIPURPLE BICYAN BIWHITE

# Underline
UBLACK='\033[4;30m'
URED='\033[4;31m'
UGREEN='\033[4;32m'
UYELLOW='\033[4;33m'
UBLUE='\033[4;34m'
UPURPLE='\033[4;35m'
UCYAN='\033[4;36m'
UWHITE='\033[4;37m'

export UBLACK URED UGREEN UYELLOW UBLUE UPURPLE UCYAN UWHITE

#------------------------------------------------------------------------------
# Functions for pre-canned formatting
#------------------------------------------------------------------------------

function fn_print_message() {
  echo -ne "${BGREEN}$1${COLOUR_OFF}\n"
}

function fn_print_tabbed_message() {
  echo -ne "\t${CYAN}$1${COLOUR_OFF}\n"
}

function fn_print_warning() {
  echo -ne "${BIYELLOW}$1${COLOUR_OFF}\n"
}

function fn_print_error() {
  echo -ne "${BIRED}$1${COLOUR_OFF}\n"
}

