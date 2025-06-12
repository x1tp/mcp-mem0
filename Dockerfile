FROM python:3.12-slim

ARG PORT=8050

ENV PORT=${PORT}
WORKDIR /app
ENV PYTHONPATH=/app/src

# Install uv
RUN pip install uv

# Copy the MCP server files
COPY . .

# Install packages
RUN python -m venv .venv
RUN uv pip install -r requirements.txt

EXPOSE ${PORT}

# Install net-tools for netstat
RUN apt-get update && apt-get install -y net-tools

# Check listening ports
RUN netstat -tulnp

# Command to run the MCP server
CMD /bin/sh -c "/app/.venv/bin/python src/main.py"