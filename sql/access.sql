REVOKE CONNECT ON DATABASE python_fastapi FROM PUBLIC;

GRANT CONNECT
ON DATABASE python_fastapi
TO "fastapi-db-iam-user@open-source-apps-001.iam";

REVOKE ALL
ON ALL TABLES IN SCHEMA public 
FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public 
TO "fastapi-db-iam-user@open-source-apps-001.iam";

GRANT USAGE, CREATE ON SCHEMA public TO "fastapi-db-iam-user@open-source-apps-001.iam";

CREATE SCHEMA IF NOT EXISTS app_schema;

GRANT USAGE, CREATE ON SCHEMA app_schema 
TO "fastapi-db-iam-user@open-source-apps-001.iam";

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA app_schema 
TO "fastapi-db-iam-user@open-source-apps-001.iam";

ALTER DEFAULT PRIVILEGES IN SCHEMA app_schema 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES 
TO "fastapi-db-iam-user@open-source-apps-001.iam";

ALTER DEFAULT PRIVILEGES IN SCHEMA app_schema 
GRANT USAGE, SELECT, UPDATE ON SEQUENCES 
TO "fastapi-db-iam-user@open-source-apps-001.iam";