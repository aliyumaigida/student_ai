
import re
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

MODEL = "gemini-2.5-flash"

# Persistent chat session
chat = client.chats.create(model=MODEL)


def call_genai(prompt_text):
    response = chat.send_message(prompt_text)
    return response.text.strip()


# ---------------------------
# 1️⃣ Question Generation
# ---------------------------
def generate_question(topic, history):

    formatted_history = []
    for item in history:
        formatted_history.append(f"AI: {item['question']}")
        formatted_history.append(f"User: {item['answer']}")

    prompt_text = f"""
        You are a Socratic tutor guiding a user to understand a topic through questioning.

        Topic: {topic}

        Conversation so far:
        {chr(10).join(formatted_history)}

        Your task:
        1. Ask ONE question that helps the user think deeper.
        2. Decide if the conversation should end.

        STRICT RULES:
        - Ask only ONE question.
        - Do NOT explain the answer.
        - Do NOT give hints.
        - Encourage deeper reasoning.

        If the user has demonstrated sufficient understanding,
        end the session.

        Return ONLY in this format:

        QUESTION: <one question>
        END_SESSION: <YES or NO>
        """

    response_text = call_genai(prompt_text)

    # robust extraction
    question_match = re.search(r"QUESTION:\s*(.+?)\s*END_SESSION:", response_text, re.DOTALL)
    end_match = re.search(r"END_SESSION:\s*(YES|NO)", response_text)

    question = question_match.group(1).strip() if question_match else "Can you elaborate on that?"
    end_session = end_match.group(1) if end_match else "NO"

    return question, end_session

# ---------------------------
# 2️⃣ Final Evaluation
# ---------------------------
def evaluate_conversation(topic, history):

    formatted_history = []
    for item in history:
        formatted_history.append(f"AI: {item['question']}")
        formatted_history.append(f"User: {item['answer']}")

    prompt_text = f"""
        You are an evaluator analyzing a user's reasoning ability.

        Topic: {topic}

        Full conversation:
        {chr(10).join(formatted_history)}

        Evaluate the user's reasoning based on:

        - Logical correctness
        - Depth of reasoning
        - Consistency with earlier answers
        - Use of evidence

        Score each from 0 to 100 percent.

        Return ONLY in this format:

        LOGICAL_CORRECTNESS: <percentage>
        DEPTH_OF_REASONING: <percentage>
        CONSISTENCY: <percentage>
        EVIDENCE_USE: <percentage>
        """

    response_text = call_genai(prompt_text)

    logic = re.search(r"LOGICAL_CORRECTNESS:\s*(\d+)", response_text)
    depth = re.search(r"DEPTH_OF_REASONING:\s*(\d+)", response_text)
    consistency = re.search(r"CONSISTENCY:\s*(\d+)", response_text)
    evidence = re.search(r"EVIDENCE_USE:\s*(\d+)", response_text)

    results = {
        "Logical Correctness": logic.group(1) + "%" if logic else "0%",
        "Depth of Reasoning": depth.group(1) + "%" if depth else "0%",
        "Consistency": consistency.group(1) + "%" if consistency else "0%",
        "Use of Evidence": evidence.group(1) + "%" if evidence else "0%"
    }

    return results