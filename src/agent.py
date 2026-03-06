from google import genai
from google.genai import types
from src.server import search_records, list_tables, list_columns

class DBridgerAgent:
    def __init__(self, api_key: str):
        """Initializes the Gemini model and gives it access to our secure tools."""
        self.client = genai.Client(api_key=api_key)
        print("🗺️ Building schema map for the AI...")
        schema_map = "DATABASE SCHEMA:\n"
        try:
            tables_str = list_tables().replace("Available Tables: ", "")
            for table in tables_str.split(", "):
                if table.strip():
                    cols_str = list_columns(table.strip()).replace("Columns: ", "")
                    schema_map += f"- Table '{table.strip()}': {cols_str}\n"
        except Exception as e:
            schema_map += f"Error loading schema: {e}"

        config = types.GenerateContentConfig(
            system_instruction=(
                "You are DBridger, a secure local database assistant.\n"
                f"Here is the exact map of the database you are working with:\n{schema_map}\n\n"
                "IMPORTANT RULES:\n"
                "1. You already have the schema. Do not guess table names.\n"
                "2. Use the `search_records` tool to find the actual data.\n"
                "3. ENTITY RESOLUTION (CRITICAL): If a user's query mentions multiple distinct concepts, you must query the specific table for each one. Do not take shortcuts by reusing identically-named columns (e.g., 'status', 'name', 'type') from related or parent tables. Always locate and query the most specific table that matches the user's requested entity.\n"
                "4. Present the final masked data clearly to the user without explaining your internal steps."
            ),
            tools=[search_records],
            temperature=0.1, # we are keeping this at 0.1 instead of 0.0 because we don't have a join function yet, so the AI needs to stay a bit creative right now
        )

        self.chat = self.client.chats.create(
            model='gemini-3.1-flash-lite-preview',
            config=config
        )

    def ask_question(self, user_query: str) -> str:
        """Sends the question to Gemini and returns the final response."""
        try:
            response = self.chat.send_message(user_query)
            return response.text
        except Exception as e:
            return f"Agent Error: {str(e)}"
