# Docker Setup Guide for PDF Summarizer

This guide will help you set up and run the PDF Summarizer application using Docker. The application will be containerized, and the browser will automatically open when the container starts.

## Prerequisites

1. **Docker** - Must be installed on your system
2. **Docker Compose** - Usually comes with Docker Desktop
3. **Git** - For cloning the repository (optional)

## Installation Instructions

### 1. Install Docker

#### For Ubuntu/Debian Linux:
```bash
# Update package index
sudo apt-get update

# Install required packages
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add your user to the docker group
sudo usermod -aG docker $USER

# Start and enable Docker service
sudo systemctl enable --now docker

# Verify installation
docker --version
docker-compose --version
```

#### For Windows:
1. Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Enable WSL 2 (Windows Subsystem for Linux 2) if prompted
3. Start Docker Desktop from the Start menu

#### For macOS:
1. Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Open Docker Desktop from Applications

### 2. Clone the Repository (if not already done)
```bash
git clone <repository-url>
cd pdf-summarizer
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with your Gemini API key:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Running the Application

### For Linux Users:
```bash
# Allow Docker to access the X server
xhost +local:docker

# Build and start the container
docker-compose up --build
```

### For Windows/WSL2 Users:
1. Make sure Docker Desktop is running
2. In WSL2 terminal:
```bash
# Set the DISPLAY variable
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# Allow X11 connections
xhost +

# Build and start the container
docker-compose up --build
```

### For macOS Users:
```bash
# Install XQuartz if not already installed
brew install --cask xquartz

# Allow connections from network clients
defaults write org.xquartz.X11 app_to_run /usr/bin/true

# Restart XQuartz
osascript -e 'quit app "XQuartz"'
open -a XQuartz

# Set DISPLAY variable
export DISPLAY=host.docker.internal:0

# Allow connections from localhost
xhost + 127.0.0.1

# Build and start the container
docker-compose up --build
```

## Accessing the Application

1. The application should automatically open in your default browser at `http://localhost:8000`
2. If it doesn't open automatically, you can manually navigate to `http://localhost:8000`

## Stopping the Application

Press `Ctrl+C` in the terminal where Docker is running, then run:
```bash
docker-compose down
```

## Troubleshooting

### Browser doesn't open automatically
- Ensure X11 forwarding is properly set up
- Try manually opening `http://localhost:8000` in your browser
- Check Docker logs for any errors:
  ```bash
  docker-compose logs
  ```

### Permission Issues
If you get permission errors when running Docker commands:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### X11 Forwarding Issues
For Linux/macOS, ensure X11 is properly configured:
```bash
echo $DISPLAY  # Should return a display number like :0 or :1
xhost +       # Allow connections to the X server
```

## Common Issues and Solutions

### "Cannot connect to the Docker daemon"
- Make sure Docker service is running
- Try running with `sudo` or add your user to the docker group

### "X11 connection rejected"
- Ensure X11 forwarding is enabled in your SSH client (if connecting remotely)
- Run `xhost +` on the host machine

### "Connection refused" when accessing the application
- Check if the container is running: `docker ps`
- Look for port conflicts (is something else using port 8000?)

## Advanced Configuration

### Building a Production Image
To create a production-ready image:
```bash
docker build -t pdf-summarizer:latest .
```

### Running the Production Image
```bash
docker run -d -p 8000:8000 --env-file .env pdf-summarizer:latest
```

## Support
If you encounter any issues, please check the [GitHub Issues](https://github.com/yourusername/pdf-summarizer/issues) or open a new issue.
