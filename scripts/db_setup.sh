source .env
export PGPASSWORD=$DB_PASSWORD
psql --host=$DB_HOST --port=$DB_PORT --username=$DB_USER --dbname=$DB_NAME -f schema.sql