#!/bin/bash
python3 -u node_red_dg.py &
status=$?
if [ $status -ne 0 ]; then
    echo "Example service Failed on startup: $status"
    exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# The container exits with an error if it detects that either process has exited.
# Otherwise it loops forever, waking up every 60 seconds
while sleep 60; do
    ps aux | grep "python3 -u node_red_dg.py" | grep -q -v grep
    PROCESS_STATUS=$?

    # If the greps above find anything, they exit with 1 status
    # If they are not both 0, then something is wrong
    if [ $PROCESS_STATUS -ne 0 ]; then
        echo "Example service has exited, shutting down container"
        exit 1
    fi
done
