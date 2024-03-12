@echo off

IF "" == "%BOT_TOKEN%" (
  echo variable BOT_TOKEN doesn't exist, see README.md, to get more info.
  echo shutting down
  pause
  exit
)

python "%~dp0\..\src\main.py"
