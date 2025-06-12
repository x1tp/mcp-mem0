#!/bin/bash

echo "Starting Mem0 Server Setup Automation"

# Step 1: Create .env file from .env.example
echo "Creating .env file from .env.example..."
cp .env.example .env

echo "Successfully created .env file."
echo "Please edit the .env file to add your sensitive information:"
echo "  - DATABASE_URL (e.g., PostgreSQL connection string)"
echo "  - LLM_PROVIDER (e.g., openai, ollama, openrouter)"
echo "  - LLM_API_KEY (Your API key)"
echo "  - LLM_CHOICE (Your preferred model)"
echo "  - EMBEDDING_MODEL_CHOICE (Your specific embedding model)"
echo ""
echo "Example .env content after manual edit:"
echo "DATABASE_URL='postgresql://user:password@host:port/database_name'"
echo "LLM_PROVIDER='openai'"
echo "LLM_API_KEY='sk-your_openai_api_key_here'"
echo "LLM_CHOICE='gpt-4'"
echo "EMBEDDING_MODEL_CHOICE='text-embedding-ada-002'"
echo ""

# Optional: Add steps for local PostgreSQL setup using Docker if desired
# For a full local PostgreSQL setup (requires Docker to be installed):
read -p "Do you want to start a local PostgreSQL database using Docker? (y/n): " confirm_pg
if [[ "$confirm_pg" == "y" || "$confirm_pg" == "Y" ]]; then
    echo "Attempting to start a local PostgreSQL database using Docker..."
    docker run --name mem0-postgres -e POSTGRES_PASSWORD=mem0password -e PGPASSWORD=mem0password -e PGUSER=postgres -e PGDATABASE=mem0db -p 5432:5432 -d postgres:latest
    if [ $? -eq 0 ]; then
        echo "PostgreSQL container 'mem0-postgres' started successfully on port 5432."
        echo "You can connect to it using: postgresql://postgres:mem0password@localhost:5432/mem0db"
        echo "Make sure to update DATABASE_URL in your .env file accordingly."
    else
        echo "Failed to start PostgreSQL container. Please check Docker status and try again."
    fi
else
    echo "Skipping local PostgreSQL database setup."
fi

echo "Setup automation complete. Remember to manually edit your .env file."