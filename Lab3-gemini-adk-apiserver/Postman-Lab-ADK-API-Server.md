# Postman Lab: Testing a Google ADK Agent with the ADK API Server

> **Lab scenario:** Run the `first_agent` application locally, create an ADK session, and send a message through the `/run` endpoint using Postman.

**Project:** `Lab1-gemini-adk-first-agent`  
**Application name:** `first_agent`

## 1. Lab objectives

In this lab, you will:

- Start the ADK REST API server.
- Verify the server and discover available agent applications.
- Create an ADK session for a user.
- Send a message to the agent from Postman.
- Read the agent response and understand the request flow.
- Recognize and fix the `Session already exists` situation.

## 2. Prerequisites

- A working Python ADK agent.
- A Python virtual environment named `.venv`.
- `google-adk` and `python-dotenv` installed.
- Gemini credentials configured in the agent `.env` file.
- Postman installed.
- An agent application folder named `first_agent`.

Example project structure:

```text
Lab1-gemini-adk-first-agent/
|-- .venv/
|-- requirements.txt
`-- first_agent/
    |-- __init__.py
    |-- agent.py
    `-- .env
```

> **Security:** Do not commit the real `.env` file or API keys to Git. Keep `.env` ignored and commit only a safe `.env.example` template when needed.

## 3. Step-by-step procedure

### Step 1: Activate the virtual environment

Open PowerShell in the project directory, then activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Expected result:** The PowerShell prompt begins with `(.venv)`.

### Step 2: Start the ADK API server

Start the REST server:

```powershell
adk api_server
```

Keep this terminal open while completing the lab.

**Expected result:** Uvicorn reports that it is running on:

```text
http://127.0.0.1:8000
```

### Step 3: List available applications

In Postman, create a request with:

**Method:** `GET`

**URL:**

```text
http://127.0.0.1:8000/list-apps
```

No request body is required. Click **Send**.

Example response:

```json
[
  "first_agent"
]
```

This confirms that the application name is `first_agent`.

### Step 4: Create a session

Create another request in Postman.

**Method:** `POST`

**URL:**

```text
http://127.0.0.1:8000/apps/first_agent/users/u_123/sessions/s_123
```

Add this header:

```text
Content-Type: application/json
```

Select **Body > raw > JSON** and enter:

```json
{}
```

Click **Send**.

Example response:

```json
{
  "id": "s_123",
  "appName": "first_agent",
  "userId": "u_123",
  "state": {},
  "events": []
}
```

The identifiers used in this lab are:

```text
Application: first_agent
User:        u_123
Session:     s_123
```

Conceptually:

```text
first_agent
`-- user: u_123
    `-- session: s_123
```

### Step 5: Send a message to the agent

Create a **different** Postman request for `/run`.

**Method:** `POST`

**URL:**

```text
http://127.0.0.1:8000/run
```

Add the header:

```text
Content-Type: application/json
```

Select **Body > raw > JSON** and enter:

```json
{
  "appName": "first_agent",
  "userId": "u_123",
  "sessionId": "s_123",
  "newMessage": {
    "role": "user",
    "parts": [
      {
        "text": "Hello! Tell me about yourself."
      }
    ]
  }
}
```

Click **Send**.

**Expected result:** The response is an array of events. The model's natural-language response appears under:

```text
content
`-- parts
    `-- text
```

For example:

```json
{
  "content": {
    "parts": [
      {
        "text": "Hello! I am an AI assistant..."
      }
    ],
    "role": "model"
  },
  "author": "root_agent"
}
```

### Step 6: Continue the same conversation

You do not need to recreate `s_123` for each message.

Reuse:

- `appName`: `first_agent`
- `userId`: `u_123`
- `sessionId`: `s_123`

Change the message text:

```json
{
  "appName": "first_agent",
  "userId": "u_123",
  "sessionId": "s_123",
  "newMessage": {
    "role": "user",
    "parts": [
      {
        "text": "What kinds of tasks can you help me with?"
      }
    ]
  }
}
```

Send the request again to:

```text
POST http://127.0.0.1:8000/run
```

## 4. Troubleshooting

### `Session already exists`

You may receive:

```json
{
  "detail": "Session already exists: s_123"
}
```

This means the session-creation endpoint was called again with the same user ID and session ID.

The API server did **not** automatically create `s_123` merely because `adk api_server` was started. The first POST request to the session endpoint created it.

To continue talking to the agent, use:

```text
POST /run
```

Do not resend the session-creation request unless you intend to create a new session with a different ID.

For example:

```text
s_124
```

### Wrong endpoint used in Postman

Keep the two operations separate:

```text
Create session:
POST /apps/first_agent/users/u_123/sessions/s_123

Send message:
POST /run
```

Saving these as two separate Postman requests helps prevent accidentally attempting to recreate the same session.

### Server is not reachable

Check the following:

1. The terminal running `adk api_server` is still open.
2. The startup output shows port `8000`.
3. Test the following request:

```text
GET http://127.0.0.1:8000/list-apps
```

## 5. How the request flow works

```text
Postman
   |
   | HTTP POST /run
   v
ADK API Server
127.0.0.1:8000
   |
   v
first_agent
   |
   v
root_agent
   |
   v
Gemini
   |
   v
JSON event response
   |
   v
Postman
```

The key distinction is:

```text
Create conversation context
        |
        v
POST /apps/first_agent/users/u_123/sessions/s_123

Send messages
        |
        v
POST /run
```

## 6. Endpoint quick reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/list-apps` | List applications discovered by the server. |
| `POST` | `/apps/{app}/users/{user}/sessions/{session}` | Create a session with a specified ID. |
| `POST` | `/run` | Run the agent and return collected events. |
| `POST` | `/run_sse` | Run the agent using Server-Sent Events. |
| `GET` | `/docs` | Open the interactive Swagger documentation. |

## 7. Lab validation checklist

- [ ] The virtual environment is active.
- [ ] `adk api_server` starts successfully.
- [ ] `GET /list-apps` returns `first_agent`.
- [ ] Session `s_123` is created once.
- [ ] `POST /run` returns an agent response.
- [ ] The response text can be found under `content > parts > text`.
- [ ] A second message can reuse the same session.

## 8. Optional exploration

### Swagger API documentation

While the API server is running, open:

```text
http://127.0.0.1:8000/docs
```

### Try `/run_sse`

ADK also exposes:

```text
POST /run_sse
```

This can be explored after you are comfortable with `/run`.

### Create another session

Try creating another session, such as:

```text
s_124
```

Then compare it with `s_123`.

## 9. Summary

In this lab, you:

1. Activated the project's Python virtual environment.
2. Started the ADK API server.
3. Discovered `first_agent` using `/list-apps`.
4. Created an ADK session.
5. Sent a message using `/run`.
6. Received the agent's response as JSON.
7. Reused the same session for additional messages.

The complete workflow is:

```text
Activate environment
        |
        v
Start API server
        |
        v
List apps
        |
        v
Create session
        |
        v
POST /run
        |
        v
Read response
```

## Sources

- [Google ADK: API Server](https://adk.dev/runtime/api-server/)
- [Google ADK: REST API Reference](https://adk.dev/api-reference/rest/)
