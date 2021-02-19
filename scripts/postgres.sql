
    REVOKE ALL ON DATABASE "postgres" FROM PUBLIC;
    REVOKE CREATE ON SCHEMA public FROM PUBLIC;
    CREATE SCHEMA IF NOT EXISTS demorest;
    ALTER DATABASE "postgres" SET search_path TO "$user",demorest;
    
    
    DO $$
    BEGIN
    CREATE ROLE readonly WITH NOLOGIN;
    EXCEPTION WHEN DUPLICATE_OBJECT THEN
    RAISE NOTICE 'not creating role readonly -- it already exists';
    END
    $$;
    GRANT CONNECT ON DATABASE "postgres" TO readonly;
    GRANT USAGE ON SCHEMA demorest TO readonly;
    GRANT SELECT ON ALL TABLES IN SCHEMA demorest TO readonly;
    ALTER DEFAULT PRIVILEGES IN SCHEMA demorest GRANT SELECT ON TABLES TO readonly;
    
    DO $$
    BEGIN
    CREATE ROLE readwrite WITH NOLOGIN;
    EXCEPTION WHEN DUPLICATE_OBJECT THEN
    RAISE NOTICE 'not creating role readwrite -- it already exists';
    END
    $$;
    GRANT CONNECT ON DATABASE "postgres" TO readwrite;
    GRANT USAGE, CREATE ON SCHEMA demorest TO readwrite;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA demorest TO readwrite;
    ALTER DEFAULT PRIVILEGES IN SCHEMA demorest GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO readwrite;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA demorest TO readwrite;
    ALTER DEFAULT PRIVILEGES IN SCHEMA demorest GRANT USAGE ON SEQUENCES TO readwrite;
    
    
    