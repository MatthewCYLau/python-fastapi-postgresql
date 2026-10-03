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