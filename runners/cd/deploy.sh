#!/bin/bash


cd ../..

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Git if not installed
if ! command_exists git; then
    echo "Git is not installed. Installing..."
    if command_exists apt; then
        sudo apt update && sudo apt install -y git
    elif command_exists yum; then
        sudo yum install -y git
    elif command_exists brew; then
        brew install git
    else
        echo "Unsupported package manager. Install Git manually."
        exit 1
    fi
else
    echo "Git is already installed."
fi

# Check if SSH key exists
SSH_KEY="$HOME/.ssh/id_rsa"
if [ ! -f "$SSH_KEY" ]; then
    echo "No SSH key found. Generating a new SSH key..."
    echo "Enter your GitHub email:"
    read -r GIT_EMAIL
    ssh-keygen -t rsa -b 4096 -C "$GIT_EMAIL" -f "$SSH_KEY" -N ""
    eval "$(ssh-agent -s)"
    ssh-add "$SSH_KEY"

    # Display the public key
    echo "Copy the following SSH key and add it to your GitHub SSH settings:"
    cat "${SSH_KEY}.pub"
    echo ""
    echo "Go to https://github.com/settings/keys and add it as a new SSH key."
    read -p "Press Enter after adding the SSH key to GitHub..."
else
    echo "SSH key already exists."
fi

# Test GitHub SSH connection
echo "Testing SSH connection to GitHub..."
ssh -T git@github.com
if [ $? -eq 1 ]; then
    echo "SSH authentication with GitHub successful!"
else
    echo "Something went wrong. Ensure your SSH key is added to GitHub."
fi

# Install Docker if not installed
if ! command_exists docker; then
    echo "Docker is not installed. Installing..."
    if command_exists apt; then
        sudo apt update && sudo apt install -y docker.io
    elif command_exists yum; then
        sudo yum install -y docker
    elif command_exists brew; then
        brew install docker
    else
        echo "Unsupported package manager. Install Docker manually."
        exit 1
    fi
    sudo systemctl enable --now docker
    echo "Docker installed successfully."
else
    echo "Docker is already installed."
fi

echo "Setup complete! Git, SSH, and Docker are configured."


# Installing dependencies


