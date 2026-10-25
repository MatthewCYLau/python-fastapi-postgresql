GRANT "fastapi-db-iam-user@open-source-apps-001.iam" TO postgres;
REASSIGN OWNED BY "fastapi-db-iam-user@open-source-apps-001.iam" TO postgres;
DROP OWNED BY "fastapi-db-iam-user@open-source-apps-001.iam";