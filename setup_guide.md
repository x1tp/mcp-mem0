# MCP-Mem0 Server Setup Guide

This guide provides instructions for setting up a PostgreSQL database and configuring the `.env` file for the `mcp-mem0` server.

## Prerequisites

*   Basic understanding of command-line interfaces.
*   (For local setup) Administrator privileges for installing software.
*   (For cloud setup) An account with a cloud provider (e.g., Supabase).

## 1. PostgreSQL Database Setup

Choose one of the following options to set up your PostgreSQL database.

### Option A: Local PostgreSQL Installation

For local development and testing, you can install PostgreSQL directly on your machine.

1.  **Download PostgreSQL**:
    Visit the official PostgreSQL website ([https://www.postgresql.org/download/](https://www.postgresql.org/download/)) and download the installer for your operating system.

2.  **Run the Installer**:
    Follow the on-screen instructions. During the installation, you will be prompted to:
    *   Choose components (ensure "PostgreSQL Server" and "pgAdmin 4" are selected).
    *   Set a data directory.
    *   Create a password for the `postgres` superuser. **Remember this password**, as you will need it to connect to the database.
    *   Specify the port (default is `5432`).

3.  **Verify Installation**:
    After installation, you can use `pgAdmin 4` (a graphical interface) or the `psql` command-line tool to connect to your database.
    Open a terminal and try:
    ```bash
    psql -U postgres
    ```
    Enter the password you set during installation.

### Option B: Cloud PostgreSQL (e.g., Supabase)

For production environments or easier management, cloud-hosted PostgreSQL services are recommended. Supabase is a popular choice that provides a PostgreSQL database with additional features.

1.  **Create a Supabase Account**:
    Go to [https://supabase.com/](https://supabase.com/) and sign up for a free account.

2.  **Create a New Project**:
    Once logged in, create a new project. Supabase will provision a new PostgreSQL database for you.

3.  **Obtain Connection String**:
    Navigate to your project's settings in the Supabase dashboard. Under "Database" -> "Connection String", you will find the connection details. Look for the "URI" or "Connection String" which typically looks like:
    `postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE_NAME]`
    **Copy this URI**, as it will be your `DATABASE_URL` for the `.env` file.

## 2. Configuring the `.env` File for MCP-Mem0

The `mcp-mem0` server uses environment variables to connect to the database and configure LLM settings. You will need to create a file named `.env` in the root directory of your `mcp-mem0` server (e.g., `MCP/mcp-mem0/.env`).

### Environment Variables

Here's a breakdown of the essential environment variables:

*   `DATABASE_URL`:
    *   **Description**: The connection string for your PostgreSQL database. This tells the `mcp-mem0` server how to connect to your database.
    *   **Format**: `postgresql://user:password@host:port/database_name`
    *   **Example (Local)**: `postgresql://postgres:your_password@localhost:5432/mem0_db`
    *   **Example (Supabase)**: `postgresql://postgres:[YOUR_SUPABASE_PASSWORD]@db.[YOUR_PROJECT_REF].supabase.co:5432/postgres`

*   `LLM_PROVIDER`:
    *   **Description**: Specifies the Large Language Model (LLM) provider you intend to use.
    *   **Accepted Values**: `openai`, `anthropic`, `google`, `ollama`, `azure_openai`, `cohere`, `huggingface`, `groq`, `mistral`, `together_ai`, `perplexity`, `open_router`, `custom`
    *   **Example**: `LLM_PROVIDER=openai`

*   `LLM_API_KEY`:
    *   **Description**: Your API key for the chosen LLM provider. This is crucial for authenticating your requests to the LLM service.
    *   **Example**: `LLM_API_KEY=sk-your_openai_api_key_here`

*   `LLM_CHOICE`:
    *   **Description**: The specific LLM model you want to use from your chosen provider.
    *   **Example (OpenAI)**: `LLM_CHOICE=gpt-4o`
    *   **Example (Anthropic)**: `LLM_CHOICE=claude-3-opus-20240229`
    *   **Example (Google)**: `LLM_CHOICE=gemini-pro`

*   `EMBEDDING_MODEL_CHOICE`:
    *   **Description**: The embedding model to be used for converting text into numerical vectors, which is essential for semantic search and memory retrieval.
    *   **Example (OpenAI)**: `EMBEDDING_MODEL_CHOICE=text-embedding-ada-002`
    *   **Example (Cohere)**: `EMBEDDING_MODEL_CHOICE=embed-english-v3.0`

### Example `.env` File

Here's a complete example of what your `.env` file might look like. Replace the placeholder values with your actual credentials and choices.

```dotenv
# Database Configuration
DATABASE_URL="postgresql://postgres:your_password@localhost:5432/mem0_db"

# LLM Configuration
LLM_PROVIDER="openai"
LLM_API_KEY="sk-your_openai_api_key_here"
LLM_CHOICE="gpt-4o"
EMBEDDING_MODEL_CHOICE="text-embedding-ada-002"
```

Remember to keep your `.env` file secure and never commit it to version control (e.g., Git).