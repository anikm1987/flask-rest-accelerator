
    REVOKE ALL ON DATABASE "{{database}}" FROM PUBLIC;
    REVOKE CREATE ON SCHEMA public FROM PUBLIC;
    CREATE SCHEMA IF NOT EXISTS {{schema_name}};
    ALTER DATABASE "{{database}}" SET search_path TO "$user",{{schema_name}};
    
    
    DO $$
    BEGIN
    CREATE ROLE readonly WITH NOLOGIN;
    EXCEPTION WHEN DUPLICATE_OBJECT THEN
    RAISE NOTICE 'not creating role readonly -- it already exists';
    END
    $$;
    GRANT CONNECT ON DATABASE "{{database}}" TO readonly;
    GRANT USAGE ON SCHEMA {{schema_name}} TO readonly;
    GRANT SELECT ON ALL TABLES IN SCHEMA {{schema_name}} TO readonly;
    ALTER DEFAULT PRIVILEGES IN SCHEMA {{schema_name}} GRANT SELECT ON TABLES TO readonly;
    
    DO $$
    BEGIN
    CREATE ROLE readwrite WITH NOLOGIN;
    EXCEPTION WHEN DUPLICATE_OBJECT THEN
    RAISE NOTICE 'not creating role readwrite -- it already exists';
    END
    $$;
    GRANT CONNECT ON DATABASE "{{database}}" TO readwrite;
    GRANT USAGE, CREATE ON SCHEMA {{schema_name}} TO readwrite;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {{schema_name}} TO readwrite;
    ALTER DEFAULT PRIVILEGES IN SCHEMA {{schema_name}} GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO readwrite;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA {{schema_name}} TO readwrite;
    ALTER DEFAULT PRIVILEGES IN SCHEMA {{schema_name}} GRANT USAGE ON SEQUENCES TO readwrite;
    
    
    