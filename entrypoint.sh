#!/bin/sh

if [ "$FLASK_ENV" = "production" ]; then
  # Check if the database file doesn't exist
  if [ ! -f "$SQLITE_DATABASE_NAME" ]; then
    # Attempt to restore the database from the replica
    litestream restore -if-replica-exists -o "$SQLITE_DATABASE_NAME" "$REPLICA_URL"
  fi

  # Print notice and ASCII art
  echo "
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║   Litestream is running in PRODUCTION!    ║
  ║                                           ║
  ║    _     _ _            _                 ║
  ║   | |   (_) |          | |                ║
  ║   | |    _| |_ ___  ___| |_ _ __ ___  __ _║
  ║   | |   | | __/ _ \/ __| __| '__/ _ \/ _\`║
  ║   | |___| | ||  __/\__ \ |_| | |  __/ (_| ║
  ║   \_____/_|\__\___||___/\__|_|  \___|\__,_║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
  "

  # Start replication
  litestream replicate "$SQLITE_DATABASE_NAME" "$REPLICA_URL"
fi
