import boto3
import streamlit as st

# Initialize the Bedrock client
bedrock_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    request_body = {
        "input": {
            "text": prompt
        },
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": "I3NKKULDXH",
                "modelArn": "anthropic.claude-v2:1"
            }
        }
    }

    response = bedrock_client.retrieve_and_generate(**request_body)

    generated_response = response['output']['text']

    print("Generated Response:", generated_response)

    assistant_message = st.chat_message("assistant")
    response_container = assistant_message.empty()

    response_container.write(generated_response)

    st.session_state.messages.append({"role": "assistant", "content": generated_response})