import streamlit as st
import openai

def generate_llm_response(client, system_prompt, user_input):

    messages = [{"role": "system", "content": system_prompt}]

    for msg in st.session_state.messages[-6:]:
        content = msg["content"]
        if len(content) > 500:
            content = content[:500] + "..."
        messages.append({"role": msg["role"], "content": content})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1,
        max_tokens=1500
    )

    reply = response.choices[0].message.content

    return reply