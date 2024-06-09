import pyodbc

try:
    # Forming the connection string
    conn_str = ("Driver={SQL Server};"
                "Server=HAL9000;"
                "DATABASE=Finance_DEV;"
                "Trusted_Connection=yes;")

    # Establishing the connection
    conn = pyodbc.connect(conn_str)

    # If the connection is successful
    print("Connection was successful.")

    # Don't forget to close the connection when done
    conn.close()

except Exception as e:
    # If the connection fails
    print("An error occurred:", e)
