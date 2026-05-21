import threading
import queue
from google import genai
import os

class DialogueAI:
    """Handles asynchronous communication with the modern google-genai SDK for NPC dialogues."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.is_active = False
        self.response_queue = queue.Queue()
        self.is_thinking = False
        
        if self.api_key:
            try:
                # Using the modern SDK syntax
                self.client = genai.Client(api_key=self.api_key)
                self.model_id = "gemini-1.5-flash"
                self.is_active = True
            except Exception as e:
                print(f"AI Error: Failed to initialize google-genai. {e}")

    def request_dialogue(self, npc_name, npc_role, player_message):
        """Triggers an async thread to fetch AI response."""
        if not self.is_active:
            self.response_queue.put(f"{npc_name}: [Sistem AI tidak terhubung. Masukkan API Key!]")
            return

        self.is_thinking = True
        thread = threading.Thread(target=self._fetch_ai_response, args=(npc_name, npc_role, player_message))
        thread.daemon = True
        thread.start()

    def _fetch_ai_response(self, npc_name, npc_role, player_message):
        """The worker thread logic."""
        prompt = f"""
        Kamu adalah NPC di dalam game survival pasca-apokaliptik bernama 'Project 23'.
        Dunia hancur karena wabah zombie, dan kamu berada di pemukiman aman bernama 'The Sanctuary'.
        
        Identitas Kamu:
        Nama: {npc_name}
        Peran: {npc_role}
        
        Aturan Bicara:
        1. Jawablah dengan singkat dan padat (maksimal 2 kalimat).
        2. Gunakan gaya bahasa yang sesuai dengan peranmu.
        3. Kamu sadar akan bahaya di luar gerbang Sanctuary.
        4. Jangan keluar dari karakter.
        
        Pesan dari pemain: "{player_message}"
        Jawablah sebagai {npc_name}:
        """
        
        try:
            # Modern SDK syntax: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            result = response.text.strip()
            self.response_queue.put(f"{npc_name}: {result}")
        except Exception as e:
            self.response_queue.put(f"{npc_name}: Maaf, otak robotku sedang error... (Error: {str(e)[:50]})")
        finally:
            self.is_thinking = False

    def get_latest_response(self):
        """Returns the response if available, otherwise None."""
        try:
            return self.response_queue.get_nowait()
        except queue.Empty:
            return None
