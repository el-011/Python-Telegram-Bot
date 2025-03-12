import json
import time
from datetime import datetime
from telegram.ext import Application, JobQueue
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Use your Groq API key

if not all([TOKEN, CHAT_ID, GROQ_API_KEY]):
    raise ValueError("One or more environment variables are missing. Please check your .env file.")

last_question = None

def generate_quiz_data():
    """
    Generate a challenging Data Structures and Algorithms quiz question with an explanation using Groq API.
    Implements a retry mechanism with exponential backoff to handle empty or invalid API responses.
    """
    prompt = """
    You are an expert in Data Structures and Algorithms.

    Generate a challenging multiple-choice quiz question for advanced programmers on DSA topics.

    Instructions:
    - The question should focus on advanced DSA topics like graph algorithms, dynamic programming, etc.
    - Provide 4 distinct options, each not exceeding 100 characters.
    - Specify the correct answer by its index (0-based).
    - Include a brief explanation (up to 200 characters) of the correct answer.
    - Vary topics across different areas of DSA, covering areas like sorting, searching, trees, graphs, dynamic programming, etc.

    Output a single JSON object (no extra text) with:
    - "question": The DSA question.
    - "options": A list of 4 possible answers.
    - "correct_option_id": Index (0-based) of the correct answer.
    - "explanation": A brief explanation of the correct answer.

    Example:
    {
      "question": "What is the worst-case time complexity of quicksort?",
      "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
      "correct_option_id": 1,
      "explanation": "Quicksort has O(n²) worst-case when the pivot selection consistently results in highly unbalanced partitions."
    }
    """

    # Try up to 3 times before falling back
    for attempt in range(3):
        try:
            # Groq API endpoint
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama3-70b-8192",  # Use an appropriate Groq model
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 250,
                "temperature": 0.8
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            response_data = response.json()
            
            # Check if response and content are valid
            if not response_data or "choices" not in response_data or not response_data["choices"]:
                raise ValueError("Empty response from API")
                
            gpt_content = response_data["choices"][0]["message"]["content"].strip()
            if not gpt_content:
                raise ValueError("Empty content received from API")

            quiz_data = json.loads(gpt_content)

            # Prevent repeated questions
            global last_question
            if quiz_data.get('question') == last_question:
                raise ValueError("Repeated question detected, regenerating...")

            last_question = quiz_data.get('question')
            return quiz_data

        except Exception as e:
            print(f"Attempt {attempt+1}: Error generating or parsing quiz data: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff

    # Fallback quiz question if all attempts fail
    return {
        "question": "What data structure is most efficient for implementing a priority queue?",
        "options": [
            "Binary Heap",
            "Linked List",
            "Array",
            "Stack"
        ],
        "correct_option_id": 0,
        "explanation": "Binary Heaps provide O(log n) insertion and extraction of the minimum/maximum element, making them ideal for priority queues."
    }

async def send_quiz(context):
    """
    Sends a quiz question (poll) in a Telegram group with multiple choices,
    using the 'quiz' type to show the correct answer and an explanation after the user answers.
    """
    quiz_data = generate_quiz_data()
    question = quiz_data.get("question", "Sample question")
    options = quiz_data.get("options", ["Option 1", "Option 2", "Option 3", "Option 4"])
    correct_id = quiz_data.get("correct_option_id", 0)
    explanation = quiz_data.get("explanation", "No explanation provided.")

    try:
        await context.bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            type="quiz",              # Enable quiz mode
            correct_option_id=correct_id,
            explanation=explanation,  # Provide explanation after answer
            is_anonymous=False
        )
        print(f"✅ DSA Quiz sent at {datetime.now()}: {question}")
    except Exception as e:
        print(f"❌ Failed to send quiz: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()

    job_queue = application.job_queue
    job_queue.run_repeating(send_quiz, interval=3600, first=10)  # Runs every 7200 seconds, starting after 10 seconds

    print("🚀 Job queue scheduled...")
    print("📡 Starting bot polling...")
    application.run_polling()
    print("🛑 Bot shutdown complete.")

if __name__ == "__main__":
    main()