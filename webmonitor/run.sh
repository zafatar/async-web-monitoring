#! /usr/bin/env sh
# run.sh

# If there's a prestart.sh script in the /app directory or other path specified,
# run it before starting
PRE_START_PATH=${PRE_START_PATH:-/code/prestart.sh}  # 2
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

# export APP_MODULE=${APP_MODULE-src.main:api}
# export HOST=${HOST:-0.0.0.0}
# export PORT=${PORT:-80}  # 3

# run uvicorn
# exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT"

echo "Starting webmonitor service..."

exec python -m src.main
