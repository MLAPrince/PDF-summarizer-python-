#!/bin/bash

# Start the FastAPI server in the background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for the server to start
sleep 3

# Try to open the browser with different commands based on OS
if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:8000" &
elif command -v open > /dev/null; then
    open "http://localhost:8000" &
else
    echo "Could not detect the browser open command. Please open http://localhost:8000 in your browser."
fi

# Keep the container running
wait
