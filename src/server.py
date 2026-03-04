import sqlite3
import os
from fastmcp import FastMCP
from src.security import mask_pii

mcp = FastMCP("DeadConn")

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "company_vault.db")
    return sqlite3.connect(db_path)

@mcp.tool()
def fetch_client_record(client_name: str) -> str:
    """
    Retrieves records from the legacy vault by client name.
    Includes automated PII masking.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM orders WHERE customer LIKE ?"
        cursor.execute(query, (f"%{client_name}%",))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            raw_response = f"ID: {result[0]} | Client: {result[1]} | Status: {result[2]} | Notes: {result[4]}"
            return mask_pii(raw_response)
        
        return f"No record found for '{client_name}'."
    except Exception as e:
        return f"Database Connection Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
