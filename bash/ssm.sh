#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

cwd=$(cd "$(dirname "${0}")" && pwd)
# See https://www.shellcheck.net/wiki/SC1091 (or, use 'shellcheck -x')
# shellcheck source=/dev/null
source "${cwd}/coloured-text.bash"

# shellcheck disable=SC2317
function fn_abort() {
  fn_print_warning "$0: Interrupt signal detected!"
  echo
  exit 2
}

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
  echo -e "${BWHITE}NB${COLOUR_OFF} In the case of identically-named instances, e.g. those managed by an"
  echo    "auto-scaling group, the script will show the InstanceIds and prompt for a target."
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
  awscli="$(command -v aws)" || true
  if [[ -z "${awscli:-}" ]]
  then
    fn_print_error "Cannot find the AWS CLI command!"
    exit 1
  fi
  fn_check_env_var "${BWHITE}AWS_ACCESS_KEY_ID${COLOUR_OFF} is not defined" "${AWS_ACCESS_KEY_ID:-}"
  fn_check_env_var "${BWHITE}AWS_SECRET_ACCESS_KEY${COLOUR_OFF} is not defined" "${AWS_SECRET_ACCESS_KEY:-}"
}

fn_list_instances() {
  local aws_region=$1
  local verbose=$2

  if [ "${verbose}" = true ]
  then
    echo -e "Executing \"${AWS} ec2 describe-instances\" in the ${aws_region} region..."
  fi
  set +o errexit
  # shellcheck disable=SC2086
  IFS=$'\n' read -d '' -r -a name_tags < <("${AWS}"                    \
    ec2 describe-instances --region "${aws_region}"                    \
    --filters "Name=instance-state-name,Values=running"                \
    --query "Reservations[*].Instances[*].Tags[?Key=='Name'].Value"    \
    --output text | sort)
  set -o errexit

  if [ ${#name_tags[@]} -eq 0 ]
  then
    fn_print_warning "No instances found - quitting"
    exit 0
  fi

  printf_fmt="  ${BIGREEN}%-32s${COLOUR_OFF} ${BWHITE}%s"
  for name_tag in "${name_tags[@]}"
  do
    # shellcheck disable=SC2059
    instance_info=$(printf "${printf_fmt}" "${name_tag}")
    echo -e "${instance_info}"
  done
}

############
# ENTRY
trap fn_abort INT TERM

fn_check_requirements

AWS=$(command -v aws)
DEFAULT_AWS_REGION="eu-west-2"
AWS_COMMAND_PREFIX=""

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
    AWS_COMMAND_PREFIX="${YELLOW}DRY RUN${COLOUR_OFF}"
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

if [ "${quiet_mode}" = true ] && [ "${verbose_mode}" = true ]
then
  fn_print_error "ERROR: the '-q' and '-v' options are mutually exclusive"
  exit 1
fi

if [ "${list_mode}" = true ]
then
  fn_list_instances "${aws_region}" "${verbose_mode}"
  exit 0
fi

# Positional argument is an instance Name or ID
shift $(( OPTIND-1 ))
if [[ $# -eq 0 ]]
then
  fn_print_warning "I have nothing to do! Please provide an instance id or name, or the '-l' option for listing instances."
  exit 0
fi
instance=$1

# ID
if [[ "${instance}" = i-* ]]
then
  if [[ "${verbose_mode}" = true ]]
  then
    echo -e "Starting an SSM session with  ${BWHITE}${instance}${COLOUR_OFF} in ${BWHITE}$aws_region${COLOUR_OFF}"
  fi

  aws_cmd="${AWS} ssm start-session --region ${aws_region} --target ${instance}"
  if [[ "$dryrun_mode" = true ]]
  then
    echo -e "${AWS_COMMAND_PREFIX} ${aws_cmd}"
  else
    eval "${aws_cmd}"
  fi

# Name
else
  if [[ "${verbose_mode}" = true ]]
  then
    echo -e "Getting the InstanceId for the instance(s) with the \"Name\" tag set to \"${BGREEN}${instance}${COLOUR_OFF}\""
  fi

  set +o errexit
  # shellcheck disable=SC2086
  IFS=$'\n' read -d '' -r -a instance_ids < <(
    aws ec2 describe-instances ${aws_profile_option:-}  \
      --region "${aws_region}"                          \
      --filters                                         \
          "Name=instance-state-name,Values=running"     \
          "Name=tag:Name,Values=${instance}"            \
      --query "Reservations[*].Instances[*].InstanceId" \
      --output text)
  set -o errexit

  instance_count=${#instance_ids[@]}

  if [[ "${instance_count}" -eq 0 ]]
  then
    fn_print_error "ERROR: Could not find an instance having the \"Name\" tag set to \"${instance}\""
    exit 2

  elif [[ "${instance_count}" -eq 1 ]]
  then
    instance_id="${instance_ids[0]}"
    if [[ "${verbose_mode}" = true ]]
    then
      echo -e "The InstanceId for \"${BGREEN}${instance}${COLOUR_OFF}\" is \"${BGREEN}${instance_id}${COLOUR_OFF}\""
    fi
    aws_cmd="${AWS} ssm start-session --region ${aws_region} --target ${instance_id}"
    if [[ "$dryrun_mode" = true ]]
    then
      echo -e "${AWS_COMMAND_PREFIX} ${aws_cmd}"
    else
      eval "${aws_cmd}"
    fi

  else
    echo -e "I have found ${BGREEN}${instance_count}${COLOUR_OFF} instances with a \"Name\" tag set to \"${BGREEN}${instance}${COLOUR_OFF}:"
    echo
    instance_index=0
    for instance_id in "${instance_ids[@]}"
    do
      (( instance_index++ )) || true
      echo -e "\t${BWHITE}${instance_index}${COLOUR_OFF}\t${BGREEN}${instance_id}${COLOUR_OFF}"
    done
    echo
    while true
    do
      read -r -p "Choose an index between 1 and ${instance_count}: " instance_index
      if [[ ${instance_index} =~ ^[0-9]+$ && ${instance_index} -ge 1 && ${instance_index} -le ${instance_count} ]]
      then
        break
      fi
    done
    index=$(( instance_index -1 ))
    instance_id="${instance_ids[${index}]}"

    if [[ "${verbose_mode}" = true ]]
    then
      echo -e "Starting an SSM session with ${BWHITE}${instance_id}${COLOUR_OFF} in ${BWHITE}$aws_region${COLOUR_OFF}"
    fi
    aws_cmd="${AWS} ssm start-session --region ${aws_region} --target ${instance_id}"
    if [[ "$dryrun_mode" = true ]]
    then
      echo -e "${AWS_COMMAND_PREFIX} ${aws_cmd}"
    else
      eval "${aws_cmd}"
    fi
  fi
fi

exit 0

