#!/usr/bin/env bash

set -o errexit
set -o pipefail
# set -o xtrace

# set output color
NC='\033[0m'
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'

log::err() {
  printf "[$(date +'%Y-%m-%dT%H:%M:%S.%2N%z')][${RED}ERROR${NC}] %b\n" "$@"
}

log::info() {
  printf "[$(date +'%Y-%m-%dT%H:%M:%S.%2N%z')][INFO] %b\n" "$@"
}

log::warning() {
  printf "[$(date +'%Y-%m-%dT%H:%M:%S.%2N%z')][${YELLOW}WARNING${NC}] \033[0m%b\n" "$@"
}

check_file() {
  if [[ ! -r ${1} ]]; then
    log::err "can not find ${1}"
    exit 1
  fi
}

check::backup_file() {
  local file=${1}
  if [[ ! -e ${file}.old-$(date +%Y%m%d) ]]; then
    cp -rp "${file}" "${file}.old-$(date +%Y%m%d)"
    log::info "backup ${file} to ${file}.old-$(date +%Y%m%d)"
  else
    log::warning "does not backup, ${file}.old-$(date +%Y%m%d) already exists"
  fi
}



check::cpu() {
  if [ `uname` != "Linux" ];then
    log::err "check os not linux."
    exit 1
  fi
  which vmstat &>/dev/null
  if [ $? -ne 0 ];then
    log::err "vmstat command no found, please install procps package."
    exit 1
  fi
  ##################################################
  cpu_us=`vmstat | awk '{print $13}' | sed -n '$p'`
  cpu_sy=`vmstat | awk '{print $14}' | sed -n '$p'`
  cpu_id=`vmstat | awk '{print $15}' | sed -n '$p'`
  cpu_wa=`vmstat | awk '{print $16}' | sed -n '$p'`   #等待I/0完成
  cpu_sum=$(($cpu_us+$cpu_sy))
  log::info "CPU_Sum : $cpu_sum% ( CPU_Use:${cpu_us}% , CPU_System:${cpu_sy}% )"
  log::info "CPU_Idle : ${cpu_id}%"
  log::info "CPU_Wait : ${cpu_wa}"
  if [ $cpu_sum -ge 90 ];then
          log::warning "CPU utilization $cpu_sum."
  fi
}

check::memory() {
  which bc &>/dev/null
  if [ $? -ne 0 ];then
    echo "bc command no found, Please install bc package."
    exit 1
  fi
  Date=`date +%F" "%H:%M`
  HOSTNAME=`hostname`
  Total=`free -m | grep Mem | awk '{print $2}'`
  Use=`free -m | grep Mem | awk '{print $3}'`
  Free=`free -m | grep Mem | awk '{print $4}'`
  Total_conv=`echo "scale=2;$Total/1024" | bc | awk '{print $1"G"}'`  #通过bc计算，保留小数点后两位（scale）
  Content=`echo -e "Date : $Date \nHost : $IP \nTotal : ${Total_conv} \nUse : ${Use}M \nFree : ${Free}M"`
  echo $Content
  if [ $Free -lt 200 ];then
    Content=`echo -e "Date : $Date \nHost : $HOSTNAME \nTotal : ${Total_conv} \nUse : ${Use}M \nFree : ${Free}M"`
    log::warning "$Content"
  fi
}


check::store() {
  # 获取当前磁盘
  use_percent=`df -h . |awk '{print $5}' |sed -n '$p'`
  use_number=${use_percent:0:-1}
  if [ $use_number -gt 90 ];then
    log::warning "disk storage utilization: $size_content"
  fi
  # 获取home目录大小
  home_size=`du -s ~ --exclude .snapshot | awk '{print $1}'`
  size_content=`echo "scale=2;$home_size/1000" | bc | awk '{print $1"M"}'`
  log::info "home storage utilization: ${size_content}"
  if [ $size_content -gt 1000 ];then
    log::warning "home storage utilization: $size_content"
  fi

  # 获取用户quota
  # 获取局点信息
  check_file ~/.ws_area
  site=`cat ~/.ws_area |awk -F "=" '{print $2}'`
  log::info "query_quota_result"
  /software/hicad/insight/1.0/bin/query_quota -s $site -d $PWD -u '$USER'
}

main() {
  local check_type=$1


  case ${check_type} in
  
  all)
    # check certificates expiration
    check::cpu
    check::memory
    check::store
    ;;
  cpu)
    # check certificates expiration
    check::cpu
    ;;
  memory)
    # check certificates expiration
    check::memory
    ;;
  store)
    # check certificates expiration
    check::store
    ;;
  *)
    log::err "unknown, unsupported check type: ${check_type}, supported type: \"all\", \"cpu\", \"memory\", \"store\""
    printf "example:
    '\033[32m./check.sh all\033[0m' 
    '\033[32m./check.sh cpu\033[0m' 
    '\033[32m./check.sh memory\033[0m' 
    '\033[32m./check.sh store\033[0m' 
"
    exit 1
    ;;
  esac
}

main "$@"
