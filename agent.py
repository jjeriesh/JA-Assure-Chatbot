import anthropic

from config import ANTHROPIC_API_KEY
from email_tool import send_report_email


client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY
)


SYSTEM_PROMPT = """
You are JA Assure AI Assistant.

Your job is to:

1. Understand the user's request.
2. Provide clear and helpful answers.
3. Be professional and friendly.
4. If the user asks to send a report by email,
   use the send_report_email tool.
5. Never expose API keys or passwords.
6. If required information for sending an email is missing,
   ask the user for it.
"""


tools = [
    {
        "name": "send_report_email",

        "description": """
        Send a report or message to an email address.

        Use this tool when the user explicitly asks
        to send information or a report by email.
        """,

        "input_schema": {
            "type": "object",

            "properties": {

                "recipient": {
                    "type": "string",
                    "description": "Email address of the recipient"
                },

                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },

                "body": {
                    "type": "string",
                    "description": "Email content"
                }

            },

            "required": [
                "recipient",
                "subject",
                "body"
            ]
        }
    }
]


def run_agent(user_message):

    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.messages.create(

        model="claude-sonnet-5",

        max_tokens=2000,

        system=SYSTEM_PROMPT,

        messages=messages,

        tools=tools
    )

    # Check if Claude wants to use a tool

    for block in response.content:

        if block.type == "tool_use":

            if block.name == "send_report_email":

                result = send_report_email(
                    recipient=block.input["recipient"],
                    subject=block.input["subject"],
                    body=block.input["body"]
                )

                # Send tool result back to Claude

                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        }
                    ]
                })

                final_response = client.messages.create(

                    model="claude-sonnet-5",

                    max_tokens=2000,

                    system=SYSTEM_PROMPT,

                    messages=messages,

                    tools=tools
                )

                for final_block in final_response.content:

                    if final_block.type == "text":
                        return final_block.text

    # Normal chatbot response

    text_response = ""

    for block in response.content:

        if block.type == "text":
            text_response += block.text

    return text_response
