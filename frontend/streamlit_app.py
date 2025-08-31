import os
from typing import Dict, Any, List

import streamlit as st

from bikes import recommend_bikes, summarize_bike
from intents import parse_preferences
from llm import chat


st.set_page_config(page_title="Bike Purchase Assistant", page_icon="🚲")

# Subtle theming tweaks
st.markdown(
    """
    <style>
    .stChatFloatingInputContainer { border-top: 1px solid #eee; }
    .chip {display:inline-block;padding:4px 10px;margin:2px;border-radius:16px;background:#eef3ff;color:#2b4eff;font-size:12px;border:1px solid #dbe4ff}
    .spec {display:inline-block;padding:2px 8px;margin:2px;border-radius:12px;background:#f6f6f6;font-size:11px;border:1px solid #eee}
    .price {font-weight:700;color:#1f7a1f}
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []  # List[Dict[str, str]] with role/content
    if "prefs" not in st.session_state:
        st.session_state.prefs = {}
    if "shortlist" not in st.session_state:
        st.session_state.shortlist = []  # List[str] of bike ids


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
        base = "Here are some options based on what I understood:" if rec_summaries else "Tell me your budget, terrain, and category to suggest bikes."
        local = base + ("\n" + "\n".join(rec_summaries) if rec_summaries else "")
        return local + f"\n\n(Note: LLM unavailable: {e})"


def render_recommendations(prefs: Dict[str, Any]) -> None:
    recs = recommend_bikes(prefs, limit=3) if prefs else []
    if not recs:
        st.info("Provide details like budget, terrain, and category to get recommendations.")
        return
    for b in recs:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(f"{b['name']} · {b['brand']}")
                st.caption(f"Category: {b['category']} · Terrain: {', '.join(b['terrain'])}")
                st.markdown(f"**Specs**: " + " ".join([f"<span class='spec'>{s}</span>" for s in [b['frame'], b['groupset'], f"{b['wheel_size']} wheels", f"{b['suspension']} suspension", f"{b['brakes']} brakes"]]), unsafe_allow_html=True)
                if b.get("motor"):
                    st.markdown(" ".join([f"<span class='spec'>motor: {b['motor']}</span>", f"<span class='spec'>{b.get('battery_wh','')}Wh</span>"]), unsafe_allow_html=True)
                st.markdown(f"Price: <span class='price'>$ {b['price_usd']}</span>", unsafe_allow_html=True)
            with c2:
                ask_key = f"ask_{b['id']}"
                short_key = f"short_{b['id']}"
                if st.button("Ask about this", key=ask_key, use_container_width=True):
                    question = f"Can you tell me more about {b['name']} by {b['brand']} and whether it fits my needs?"
                    st.session_state.messages.append({"role": "user", "content": question})
                    reply = make_assistant_reply(question, st.session_state.prefs)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                in_shortlist = b['id'] in st.session_state.shortlist
                label = "Remove from shortlist" if in_shortlist else "Add to shortlist"
                if st.button(label, key=short_key, type="secondary", use_container_width=True):
                    if in_shortlist:
                        st.session_state.shortlist = [bid for bid in st.session_state.shortlist if bid != b['id']]
                    else:
                        st.session_state.shortlist.append(b['id'])
                    st.rerun()


def main() -> None:
    initialize_state()

    st.title("🚲 Bike Purchase Assistant")
    st.write(
        "Tell me how you'll ride (terrain), your budget, and any preferences."
        " Examples: 'I commute in the city under $1000', 'I want a gravel bike around 2500',"
        " or 'an e-bike for urban rides under 3k'."
    )

    with st.sidebar:
        st.header("Preferences")
        budget = st.text_input("Budget (e.g., 1200 or 1,200 or 2k)")
        category = st.selectbox(
            "Category",
            ["", "road", "mountain", "hybrid", "gravel", "city", "e-bike"],
            index=0,
        )
        terrain = st.selectbox(
            "Terrain",
            ["", "paved", "gravel", "trail", "urban"],
            index=0,
        )
        brand = st.text_input("Brand (optional)")
        motorized = st.selectbox("Electric Assist", ["", "Yes", "No"], index=0)
        lightweight = st.checkbox("Prefer lightweight")

        manual_prefs: Dict[str, Any] = {}
        if budget.strip():
            t = budget.lower().replace(",", "").replace(" ", "")
            try:
                if t.endswith("k"):
                    manual_prefs["budget"] = int(float(t[:-1]) * 1000)
                else:
                    manual_prefs["budget"] = int(t)
            except Exception:
                pass
        if category:
            manual_prefs["category"] = category
        if terrain:
            manual_prefs["terrain"] = terrain
        if brand.strip():
            manual_prefs["brand"] = brand.strip()
        if motorized == "Yes":
            manual_prefs["motorized"] = True
        elif motorized == "No":
            manual_prefs["motorized"] = False
        if lightweight:
            manual_prefs["lightweight"] = True

        if st.button("Apply Preferences"):
            st.session_state.prefs = merge_prefs(st.session_state.prefs, manual_prefs)

        st.divider()
        st.subheader("Shortlist")
        if not st.session_state.shortlist:
            st.caption("No bikes shortlisted yet.")
        else:
            for bid in st.session_state.shortlist:
                st.write("- ", bid)

        st.divider()
        with st.expander("Environment"):
            st.write("OPENAI_MODEL:", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
            st.write("API Key set:", bool(os.getenv("OPENAI_API_KEY")))

    # Chat interface
    # Preference badges
    if st.session_state.prefs:
        chips = []
        for k in ["budget", "category", "terrain", "brand", "motorized", "lightweight"]:
            if k in st.session_state.prefs:
                chips.append(f"<span class='chip'>{k}: {st.session_state.prefs[k]}</span>")
        if chips:
            st.markdown(" ".join(chips), unsafe_allow_html=True)

    # Chat messages with avatars
    for msg in st.session_state.messages:
        avatar = "🧑" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about bikes, budget, terrain, or preferences...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        extracted = parse_preferences(user_input)
        st.session_state.prefs = merge_prefs(st.session_state.prefs, extracted)
        reply = make_assistant_reply(user_input, st.session_state.prefs)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # Quick suggestions
    st.caption("Try quick suggestions:")
    col1, col2, col3 = st.columns(3)
    if col1.button("City under $800"):
        q = "I commute in the city under $800"
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.prefs = merge_prefs(st.session_state.prefs, parse_preferences(q))
        st.session_state.messages.append({"role": "assistant", "content": make_assistant_reply(q, st.session_state.prefs)})
        st.rerun()
    if col2.button("Gravel ~2500"):
        q = "I want a gravel bike around 2500"
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.prefs = merge_prefs(st.session_state.prefs, parse_preferences(q))
        st.session_state.messages.append({"role": "assistant", "content": make_assistant_reply(q, st.session_state.prefs)})
        st.rerun()
    if col3.button("Urban e-bike 3k"):
        q = "an e-bike for urban rides under 3k"
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.prefs = merge_prefs(st.session_state.prefs, parse_preferences(q))
        st.session_state.messages.append({"role": "assistant", "content": make_assistant_reply(q, st.session_state.prefs)})
        st.rerun()

    st.divider()
    st.subheader("Top Recommendations")
    render_recommendations(st.session_state.prefs)


if __name__ == "__main__":
    main()


