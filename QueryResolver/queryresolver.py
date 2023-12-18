# -*- coding: utf-8 -*-
"""QueryResolver.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RoX-m5iVvkUjzBVT0tbAgt6LZu0aHuIV
"""

import sqlite3

db_file = 'chinook.db'
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

#decription of the table

table_name='albums'
cursor.execute(f"PRAGMA table_info({table_name})")

rows = cursor.fetchall()
for row in rows:
    print(row)

def getTables(db_file):

  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch all table names
  table_names = cursor.fetchall()

  # Print or process the table names
  for table_name in table_names:
        print(table_name[0])

getTables(db_file)

#get relations between the tables
def getRelations(table_name):
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()

  for table in tables:
      table_name = table[0]

      # Get primary key information
      cursor.execute(f"PRAGMA table_info({table_name})")
      columns = cursor.fetchall()
      primary_key_columns = [column[1] for column in columns if column[5] == 1]


      print(f"Table: {table_name}")
      print(f"Primary Key: {', '.join(primary_key_columns)}")

      # Get foreign key information
      cursor.execute(f"PRAGMA foreign_key_list({table_name})")
      foreign_keys = cursor.fetchall()

      for foreign_key in foreign_keys:
          print(f"Foreign Key: {foreign_key[3]} references {foreign_key[2]}({foreign_key[4]})")

      print("\n")

getRelations(table_name)

#function to get the column names in a table
def getColumnNames(db_file, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')

    # Fetch all rows
    columns_info = cursor.fetchall()

    if not columns_info:
        print(f"No information available for table '{table_name}'.")
        return

    # Print column names and their datatypes
    print(f"Column information for table '{table_name}':")
    for column_info in columns_info:
        column_name = column_info[1]
        data_type = column_info[2]
        print(f" {column_name}, Data Type: {data_type}")

getColumnNames(db_file,'invoices')

old_column_name='ArtistId'
new_column_name='ArtId'


#function to rename a column in the table
def rename_column(db_file, table_name, old_column_name, new_column_name):


    cursor.execute(f'PRAGMA table_info({table_name})')

    # Fetch all rows to get column names
    columns_info = cursor.fetchall()
    column_names = [column[1] for column in columns_info]

    # Create a new table with the desired column names and structure
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name}_new AS
        SELECT
            {', '.join(f'{col} AS {col}' if col != old_column_name else f'{col} AS {new_column_name}' for col in column_names)}
        FROM {table_name}
    ''')

    # Copy data from the old table to the new table
    cursor.execute(f'INSERT INTO {table_name}_new SELECT * FROM {table_name}')

    # Drop the old table
    cursor.execute(f'DROP TABLE {table_name}')

    # Rename the new table to the original table name
    cursor.execute(f'ALTER TABLE {table_name}_new RENAME TO {table_name}')# Execute PRAGMA statement to get table information
    cursor.execute(f'PRAGMA table_info({table_name})')

    # Fetch all rows to get column names
    columns_info = cursor.fetchall()
    column_names = [column[1] for column in columns_info]

    # Create a new table with the desired column names and structure
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name}_new AS
        SELECT
            {', '.join(f'{col} AS {col}' if col != old_column_name else f'{col} AS {new_column_name}' for col in column_names)}
        FROM {table_name}
    ''')

    # Copy data from the old table to the new table
    cursor.execute(f'INSERT INTO {table_name}_new SELECT * FROM {table_name}')

    # Drop the old table
    cursor.execute(f'DROP TABLE {table_name}')

    # Rename the new table to the original table name
    cursor.execute(f'ALTER TABLE {table_name}_new RENAME TO {table_name}')

rename_column(db_file,table_name,old_column_name,new_column_name)

#function to delete the table from the database

def delete_table(db_file, table_name):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to drop the table
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

        # Commit the changes
        conn.commit()
        print(f'Table {table_name} deleted successfully.')

    except sqlite3.Error as e:
        print(f'Error deleting table {table_name}: {e}')

#function to rename the table in .db file
old_table_name='artists'
new_table_name='artists1'
def rename_table(db_file, old_table_name, new_table_name):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute SQL query to rename the table
        cursor.execute(f'ALTER TABLE {old_table_name} RENAME TO {new_table_name}')

        # Commit the changes
        conn.commit()
        print(f'Table {old_table_name} renamed to {new_table_name} successfully.')

    except sqlite3.Error as e:
        print(f'Error renaming table {old_table_name}: {e}')

rename_table(db_file,old_table_name,new_table_name)

column_to_delete='ArtId'
#function to delete the column in the database
def delete_column(db_file, table_name, column_to_delete):


    try:
        # Execute PRAGMA statement to get table information
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns_info = cursor.fetchall()

        # Get column names excluding the one to be deleted
        column_names = [column[1] for column in columns_info if column[1] != column_to_delete]

        # Execute SQL query to create a new table without the specified column
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}_new AS
            SELECT {', '.join(column_names)}
            FROM {table_name}
        ''')

        # Execute SQL query to copy data from the old table to the new table
        cursor.execute(f'INSERT INTO {table_name}_new SELECT * FROM {table_name}')

        # Execute SQL query to drop the old table
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

        # Execute SQL query to rename the new table to the original table name
        cursor.execute(f'ALTER TABLE {table_name}_new RENAME TO {table_name}')

        # Commit the changes
        connection.commit()
        print(f'Column {column_to_delete} deleted from table {table_name} successfully.')

    except sqlite3.Error as e:
        print(f'Error deleting column {column_to_delete} from table {table_name}: {e}')

delete_column(db_file,table_name,column_to_delete)

def print_table_contents(db_file, table_name):
    # Connect to the database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    try:
        # Execute SQL query to fetch all records from the table
        cursor.execute(f'SELECT * FROM {table_name}')
        records = cursor.fetchall()

        # Get column names
        cursor.execute(f'PRAGMA table_info({table_name})')
        column_names = [column[1] for column in cursor.fetchall()]

        # Print column names
        print(f"Column names: {', '.join(column_names)}")

        # Print records
        print("Table contents:")
        for record in records:
            print(record)

    except sqlite3.Error as e:
        print(f'Error fetching records from table {table_name}: {e}')

print_table_contents(db_file,table_name)

column_to_update='AlbumId'
new_value=101
condition_column='AlbumId'
condition_value=200
condition_operator='>'
#function to edit the table

def edit_table(db_file, table_name, column_to_update, new_value, condition_column, condition_operator, condition_value):
    # Connect to the database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    try:
        # Execute SQL query to update the table based on conditions
        cursor.execute(f'''
            UPDATE {table_name}
            SET {column_to_update} = ?
            WHERE {condition_column} {condition_operator} ?
        ''', (new_value, condition_value))

        # Commit the changes
        connection.commit()
        print(f'Table {table_name} updated successfully.')

    except sqlite3.Error as e:
        print(f'Error updating table {table_name}: {e}')

edit_table(db_file, table_name, column_to_update, new_value, condition_column, condition_operator, condition_value)

def delete_record(db_file, table_name, condition_column, condition_operator, condition_value):
    # Connect to the database


    try:
        # Execute SQL query to delete records based on conditions
        cursor.execute(f'''
            DELETE FROM {table_name}
            WHERE {condition_column} {condition_operator} ?
        ''', (condition_value,))

        # Commit the changes
        connection.commit()
        print(f'Record(s) deleted successfully from table {table_name}.')

    except sqlite3.Error as e:
        print(f'Error deleting record(s) from table {table_name}: {e}')

delete_record(db_file, table_name, condition_column, condition_operator, condition_value)



print_table_contents(db_file,'invoices')

values=(201,'Hello',701)

def insert_record(db_file, table_name, values):
    # Connect to the database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    try:
        # Execute SQL query to insert a record into the table
        cursor.execute(f'''
            INSERT INTO {table_name} VALUES {tuple(values)}
        ''')

        # Commit the changes
        connection.commit()
        print(f'Record inserted successfully into table {table_name}.')

    except sqlite3.Error as e:
        print(f'Error inserting record into table {table_name}: {e}')

insert_record(db_file,table_name,values)

print_table_contents(db_file,table_name)

column_defintions=['id INTEGER PRIMARY KEY',
    'name TEXT',
    'age INTEGER',
    'email TEXT']

def create_table(db_file, table_name, column_defintions):


    try:
        # Execute SQL query to create a table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(column_defintions)}
            )
        ''')

        # Commit the changes
        connection.commit()
        print(f'Table {table_name} created successfully.')

    except sqlite3.Error as e:
        print(f'Error creating table {table_name}: {e}')

create_table(db_file,'test',column_defintions)

getTables(db_file)

connection.close
