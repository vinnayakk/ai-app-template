from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # reads .env and loads ANTHROPIC_API_KEY into the environment

client = Anthropic()  # automatically picks up ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What is FastAPI in one sentence?"}
    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)