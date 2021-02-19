# This python code is to test the connectivity to local database instance.  
# This code can also be used to create primary users in your database if required. 
# make sure schema_user_create_flag=True is enabled.
# This is for local testing of postgres in local ubuntu system or installed using docker command - 
# docker run -p 5432:5432 --name mypostgres -e POSTGRES_PASSWORD=postgres -d postgres:11-alpine
# Initial draft - Aniket Mukherjee


import psycopg2
import getpass
from psycopg2 import extensions, sql
from jinja2 import Environment, FileSystemLoader


def setup_database_and_schema(connection,schema_name,database = "postgres"):
    """ Load sql template file, replace database and schema name and execute the SQL file. Retrun True if successful"""
    file_loader = FileSystemLoader('sql')
    env = Environment(loader=file_loader,autoescape=True)
    template = env.get_template('setup_database_schema.sql')
    template.stream(database=database,schema_name=schema_name).dump(f"{database}.sql")
    cursor = connection.cursor()
    cursor.execute(open(f"{database}.sql", "r").read())
    cursor.close()
    return True


def set_auto_commit(connection):
    """ Set auto commit for database connection"""
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    connection.set_isolation_level( autocommit )
    


def execute_postgresql(connection,sql_string):
    """ Execute SQL statement and return True if successful """
    cursor = connection.cursor()
    cursor.execute(sql_string)
    cursor.close()
    return True


def execute_select_postgresql(connection,sql_string):
    """ Execute SQL select statement, print all results and return True if successful """
    cursor = connection.cursor()
    cursor.execute(sql_string)
    records=cursor.fetchall()
    for row in records:
       print(row)
    cursor.close()
    return True

def revoke_user_role(user_name,role_name,connection):
    """ Revoke role from the user and return the user_name """
    execute_postgresql(connection, f"REVOKE {role_name} FROM {user_name};")
    return user_name

def assign_user_role(user_name,role_name,connection):
    """ Assign role to ther user and return the user_name """
    execute_postgresql(connection, f"GRANT {role_name} TO {user_name};")
    return user_name


def create_database_user(user_name,password,connection,database = "postgres"):
    """ Create initial user and return the user_name """
    execute_postgresql(connection, f"CREATE USER {user_name} WITH PASSWORD '{password}';")
    return user_name

def get_database_login_connection(user,password,host,database):
    """ Return database connection object based on user and database details provided """
    connection = psycopg2.connect(user = user,
                                    password = password,
                                    host = host,
                                    port = "5432",
                                    database = database,
                                    sslmode= "prefer")
    set_auto_commit(connection)
    return connection

def validate_database_connectivity(connection):
    """ Validate database connecttivity by executing SQL and fetching version of database"""
    cursor = connection.cursor()
    print ( connection.get_dsn_parameters(),"\n")

    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print ("You are connected to - ", record,"\n")
    cursor.close()
    return True

if __name__ == "__main__":
    """ Main function """
    schema_initial_setup=False
    schema_user_create_flag=True

    database_name = "postgres"
    database_schema_name= "demorest"
    database_server_name="localhost"
    database_server_fqdn = "localhost"
    database_admin="postgres"
    user=database_admin
    connection=None
    
    try:
        admin_password = getpass.getpass(
        prompt=f"Enter password for {database_admin}@{database_server_name} : "
        )
        
        connection=get_database_login_connection(user,admin_password,database_server_fqdn,database_name)
        if validate_database_connectivity(connection):
            print("Accessible schemas for user : ")
            execute_select_postgresql(connection,"SELECT nspname FROM pg_catalog.pg_namespace;")
            print("Default schemas for userin search path : ")
            execute_select_postgresql(connection,"SHOW search_path;")
            if (schema_initial_setup):
                setup_database_and_schema(connection,database_schema_name,database_name)
                print("Initial setup completed successfully")
            
            if(schema_user_create_flag):
                new_user_name=input('Enter new postgres database user name to be created:')
                user_password = getpass.getpass(
                prompt=f"Enter password for {new_user_name}@{database_server_name} : "
                )
                role_input=int(input(f"Press 1 for readwrite role on {database_schema_name} or any other number for readonly :"))
                
                new_user=create_database_user(new_user_name,user_password,connection,database_name)
                if(new_user):
                    print(f"{new_user} created successfully. Assiging role and verifying connectivity with new user.")
                    if role_input == 1:
                        assign_user_role(new_user,"readwrite",connection)
                    else:
                        assign_user_role(new_user,"readonly",connection)
                    
                    if(connection):
                            connection.close()
                    connection=get_database_login_connection(new_user,user_password,database_server_fqdn,database_name)
                    validate_database_connectivity(connection)

    except IOError:
        print("SQL file not accessible")
    except ValueError:
        print('Please enter a valid number for role assigment and try again')
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL",error)
    finally:
            if(connection):
                connection.close()
                print("PostgreSQL connection is closed")