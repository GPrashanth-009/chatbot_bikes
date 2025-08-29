import os
import sys
from typing import Dict, Any

from bikes import recommend_bikes, summarize_bike
from intents import parse_preferences
from llm import chat


WELCOME = (
    "Welcome to the Bike Finder! Tell me how you'll ride (terrain), budget, and any preferences.\n"
    "Examples: 'I commute in the city under $1000', 'I want a gravel bike around 2500',\n"
    "or 'an e-bike for urban rides under 3k'. Type 'quit' to exit."
)


def merge_prefs(state: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(state)
    for k, v in new.items():
        if v is not None and v != "":
            merged[k] = v
    return merged


def make_assistant_reply(user_text: str, prefs: Dict[str, Any]) -> str:
    recs = recommend_bikes(prefs, limit=3) if prefs else []
    rec_summaries = [f"- {summarize_bike(b)}" for b in recs]

    sys_prompt = (
        "You are a helpful bike-purchasing assistant.\n"
        "- Be concise (<= 6 sentences).\n"
        "- If you have recommendations, list them as short bullets.\n"
        "- If information is missing (budget, terrain, category), ask a brief follow-up.\n"
        "- Do not invent bikes; rely on provided summaries.\n"
    )

    context = (
        "Current interpreted preferences (may be partial):\n"
        f"{prefs}\n\n"
        "Top matches in our catalog:\n" + ("\n".join(rec_summaries) if rec_summaries else "(none yet)")
    )

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_text},
        {"role": "system", "content": context},
    ]
    try:
        return chat(messages)
    except Exception as e:
        # Fallback if OpenAI isn't configured: produce a simple local reply
        base = "Here are some options based on what I understood:" if rec_summaries else "Tell me your budget, terrain, and category to suggest bikes."
        local = base + ("\n" + "\n".join(rec_summaries) if rec_summaries else "")
        return local + f"\n\n(Note: LLM unavailable: {e})"


def main() -> None:
    print(WELCOME)
    prefs: Dict[str, Any] = {}
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if line.lower() in {"quit", "exit"}:
            print("Goodbye!")
            return
        if not line:
            continue

        extracted = parse_preferences(line)
        prefs = merge_prefs(prefs, extracted)
        reply = make_assistant_reply(line, prefs)
        print(reply)


if __name__ == "__main__":
    main()


