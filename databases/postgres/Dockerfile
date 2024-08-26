FROM postgres:14

# Install the pgvector extension
RUN apt-get update && apt-get install -y \
    postgresql-14-pgvector \
    && rm -rf /var/lib/apt/lists/*

# Copy the init scripts
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql