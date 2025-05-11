import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_PROMPT = """You are a Homer, AI that is designed to assist students (of all ages) with creative and academic writing.
1. Always begin the conversation by asking the student to state their thesis and provide outline and general plan before writing.
2. In case the user asks you help with an ongoing project, skip the plan part.
3. Decompose each writing task into distinct steps such as topic exploration, argument development, paragraph structuring, drafting, revision.
4. When you see systemic flaws in students' writing, point them out in a gentle way.
5. Explain writing principles (e.g., structure, transitions, citation conventions) and show brief examples.
5.1 Never provide full paragraphs or complete essays, unless the students asks for very minor changes (spelling, grammar, formatting)
6. Limit AI generated text and focus on providing students with tips. If a bigger example needed, make it distinct from the original student's text and theme so that it will be unsuitable for the student while providing an insight
Never provide full paragraphs even as example.
7. Ask students if they want to engage in a review, ask them if they need feedback. Do not force students into answering questions unless prompted.
7.1 You can offer students to engage in a Socratic dialogue where you will ask them various questions to help them sharpen their arguments.
8. Maintain a direct, no-nonsense talk focused on helping students to develop their skills. You are meant to write anything for students, only assist them.
9. When starting conversation, explain your role to students in a few short sentence.
"""
MODEL = "gemini-2.0-flash"

class App:
    def __init__(self, root):
        root.title("Gemini Client")
        root.geometry("900x600")
        style = ttk.Style(root)
        style.theme_use('vista')
        style.configure('TLabel', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.chat = None

        self.container = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.left = ttk.Frame(self.container, width=300)
        self.right = ttk.Frame(self.container)
        self.container.add(self.left, weight=1)
        self.container.add(self.right, weight=2)

        ttk.Label(self.left, text="Prompt").pack(anchor='w')
        self.prompt = scrolledtext.ScrolledText(self.left, wrap='word', font=('Segoe UI', 10), height=15)
        self.prompt.pack(fill=tk.BOTH, expand=True, pady=(5,10))

        self.send_btn = ttk.Button(self.left, text="Send", command=self.send)
        self.send_btn.pack(anchor='e')

        ttk.Label(self.right, text="Response").pack(anchor='w')
        self.response = scrolledtext.ScrolledText(self.right, wrap='word', font=('Segoe UI', 10), state='disabled')
        self.response.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.status = ttk.Label(root, text="Ready", anchor='w')
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def send(self):
        text = self.prompt.get("1.0", "end").strip()
        if not text:
            return
        self.send_btn.state(['disabled'])
        self.status.config(text="Processing…")
        self.response.config(state='normal')
        self.response.delete("1.0", "end")
        self.response.insert("end", "…")
        self.response.config(state='disabled')
        threading.Thread(target=self._send, args=(text,), daemon=True).start()

    def _send(self, text):
        try:
            client = genai.Client(api_key=API_KEY)
            if self.chat is None:
                self.chat = client.chats.create(
                    model=MODEL,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )
            resp = self.chat.send_message(text)
            result = resp.text
        except Exception as e:
            result = str(e)

        self.response.after(0, self._update_response, result)

    def _update_response(self, text):
        self.response.config(state='normal')
        self.response.delete("1.0", "end")
        self.response.insert("end", text)
        self.response.config(state='disabled')
        self.status.config(text="Done")
        self.send_btn.state(['!disabled'])

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
