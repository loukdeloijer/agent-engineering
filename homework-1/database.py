import duckdb

# Initialize DuckDB connection
conn = duckdb.connect(database='grid.duckdb')

# Drop the database if it exists

def drop_schema(schema_name: str):
    conn.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;")

# Function to create schema and tables for a grid operator company
def init_schema():
    conn.execute("CREATE SCHEMA IF NOT EXISTS grid_ops;")
    # Substations
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grid_ops.substations (
            substation_id   INTEGER PRIMARY KEY,
            name            VARCHAR,
            location        VARCHAR,
            capacity_mw     DOUBLE
        );
    """)
    # Transmission lines
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grid_ops.transmission_lines (
            line_id         INTEGER PRIMARY KEY,
            from_sub_id     INTEGER REFERENCES grid_ops.substations(substation_id),
            to_sub_id       INTEGER REFERENCES grid_ops.substations(substation_id),
            length_km       DOUBLE,
            voltage_kv      DOUBLE
        );
    """)
    # Maintenance records
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grid_ops.maintenance_records (
            record_id       INTEGER PRIMARY KEY,
            line_id         INTEGER REFERENCES grid_ops.transmission_lines(line_id),
            date            DATE,
            description     VARCHAR
        );
    """)
    # Power generation units
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grid_ops.generators (
            generator_id    INTEGER PRIMARY KEY,
            name            VARCHAR,
            type            VARCHAR,
            max_output_mw   DOUBLE
        );
    """)
    # Generator to substation mapping
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grid_ops.generator_connections (
            conn_id         INTEGER PRIMARY KEY,
            generator_id    INTEGER REFERENCES grid_ops.generators(generator_id),
            substation_id   INTEGER REFERENCES grid_ops.substations(substation_id)
        );
    """)

# Insert sample data (optional)
def insert_sample_data():
    # Substations
    conn.executemany(
        "INSERT INTO grid_ops.substations VALUES (?, ?, ?, ?)",
        [
            (1, 'Amsterdam Zuid Substation', 'Amsterdam', 500.0),
            (2, 'Rotterdam Noord Substation', 'Rotterdam', 350.0),
            (3, 'Utrecht Lunetten Substation', 'Utrecht', 400.0)
        ]
    )
    # Transmission lines
    conn.executemany(
        "INSERT INTO grid_ops.transmission_lines VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, 2, 150.0, 220.0),
            (2, 2, 3, 200.0, 110.0),
            (3, 3, 1, 180.0, 220.0)
        ]
    )
    # Maintenance
    conn.executemany(
        "INSERT INTO grid_ops.maintenance_records VALUES (?, ?, ?, ?)",
        [
            (1, 1, '2025-01-15', 'Transformer replacement'),
            (2, 2, '2025-03-05', 'Line inspection'),
            (3, 1, '2025-05-10', 'Cable fault repair'),
            (4, 3, '2025-02-20', 'Tower maintenance'),
            (5, 2, '2025-06-01', 'Insulator cleaning'),
            (6, 3, '2025-04-15', 'Ground wire replacement')
        ]
    )
    # Generators
    conn.executemany(
        "INSERT INTO grid_ops.generators VALUES (?, ?, ?, ?)",
        [
            (1, 'WP-IJM-01', 'Wind', 180.0),
            (2, 'SP-EEM-01', 'Solar', 75.0)
        ]
    )
    # Connections
    conn.executemany(
        "INSERT INTO grid_ops.generator_connections VALUES (?, ?, ?)",
        [
            (1, 1, 1),
            (2, 2, 2)
        ]
    )

# Table-function wrappers for metadata introspection

def list_databases():
    """List accessible databases."""
    return conn.execute("SELECT * FROM duckdb_databases();").fetchall()


def list_schemas():
    """List schemas in the current database."""
    return conn.execute("SELECT * FROM duckdb_schemas();").fetchall()


def list_tables():
    """List base tables in the current database."""
    return conn.execute("SELECT * FROM duckdb_tables();").fetchall()


def list_views():
    """List views in the current database."""
    return conn.execute("SELECT * FROM duckdb_views();").fetchall()


def list_columns(table_name: str, schema: str = 'grid_ops'):
    """List columns for a given table."""
    return conn.execute(
        "SELECT * FROM duckdb_columns() WHERE schema_name = ? AND table_name = ?;",
        (schema, table_name)
    ).fetchall()


def list_dependencies():
    """List dependencies between objects."""
    return conn.execute("SELECT * FROM duckdb_dependencies();").fetchall()

# Example agent tool registry
tool_registry = {
    'list_databases': list_databases,
    'list_schemas': list_schemas,
    'list_tables': list_tables,
    'list_views': list_views,
    'list_columns': list_columns,
    'list_dependencies': list_dependencies
}

if __name__ == '__main__':
    # Optional sample run
    drop_schema('grid_ops')
    print('Dropped schema grid_ops')
    init_schema()
    print('Initialized schema grid_ops')
    insert_sample_data()
    print('Schemas:', list_schemas())
    print('Tables:', list_tables())
    print('Columns in substations:', list_columns('substations'))
    print('Inserted sample data')