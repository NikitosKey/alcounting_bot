#!/bin/bash

if  [ "" == "${BOT_TOKEN}" ];
then 
  echo "variable BOT_TOKEN doesn't exist, see README.md, to get more info."
  echo "shutting down"
  exit
fi

SCRIPT_PATH="${BASH_SOURCE}"
while [ -L "${SCRIPT_PATH}" ]; do
  SCRIPT_DIR="$(cd -P "$(dirname "${SCRIPT_PATH}")" >/dev/null 2>&1 && pwd)"
  SCRIPT_PATH="$(readlink "${SCRIPT_PATH}")"
  [[ ${SCRIPT_PATH} != /* ]] && SCRIPT_PATH="${SCRIPT_DIR}/${SCRIPT_PATH}"
done
SCRIPT_PATH="$(readlink -f "${SCRIPT_PATH}")"
SCRIPT_DIR="$(cd -P "$(dirname -- "${SCRIPT_PATH}")" >/dev/null 2>&1 && pwd)"

python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install python-telegram-bot==21.0.1
pip install setproctitle
cd ..
screen -S 'alcounting_bot' python -m bot.__main__
