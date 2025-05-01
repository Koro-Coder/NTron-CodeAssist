import chainlit as cl
from Groq_LLM import chat_with_groq
from Retrieve_Code_Snippet import search_code_snippet

@cl.on_message
async def handle_message(message: cl.Message):
    # Retrieve the selected snippet from the user session
    selected_snippet = cl.user_session.get("selected_snippet")

    if selected_snippet is None:
        # Step 1: Perform search based on query
        results = search_code_snippet(message.content)

        if not results:
            await cl.Message("❌ No relevant code snippets found.").send()
            return

        # Step 2: Display results and offer selection buttons
        elements = []
        for idx, result in enumerate(results):
            # Extract relevant fields from the result object
            summary = result.get("Summary", "No summary available")
            code_snippet = result.get("Code Snippet", "No code snippet available")
            document_id = result.get("Document ID", "Unknown file")
            preview = code_snippet[:200] + "..."  # Limit preview to 200 characters

            # Create a text element for each snippet
            el = cl.Text(
                name=f"Snippet {idx+1}",
                content=f"**Summary:** {summary}\n**File:** {document_id}\n\n```python\n{preview}\n```"
            )
            elements.append(el)

        # Send the main message and get its ID
        main_message = await cl.Message(content="🔍 Top 3 matches:").send()

        # Send each element associated with the main message
        for element in elements:
            await element.send(for_id=main_message.id)

        # Provide options for user to select snippet, including "None of the above"
        actions = [
            cl.Action(name=f"select_snippet_{i}", icon="code", payload={"index": i}, label=f"Use Snippet {i+1}")
            for i in range(len(results))
        ]
        actions.append(cl.Action(name="none_of_above", icon="x-circle", payload={}, label="None of the above"))
        await cl.Message("Choose one of the snippets to proceed:", actions=actions).send()

        # Temporarily store the results for callback access
        cl.user_session.set("_last_results", results)

    else:
        # Step 3: Chat mode with the selected snippet
        system_prompt = f"""
        You are a helpful coding assistant. The user is asking questions about this code:

        ```python
        {selected_snippet['Code Snippet']}
        ```

        Provide helpful, concise answers or code modifications when asked.
        """

        # Retrieve or initialize chat history
        chat_history = cl.user_session.get("chat_history", [{
            "role": "system",
            "content": system_prompt
        }])
        if len(chat_history) == 0:
            chat_history = [{
                "role": "system",
                "content": system_prompt
            }]

        # Append user message
        chat_history.append({"role": "user", "content": message.content})

        # Generate a response
        response = chat_with_groq(chat_history)
        chat_history.append({"role": "assistant", "content": response})
        cl.user_session.set("chat_history", chat_history)

        await cl.Message(content=response).send()


@cl.action_callback("none_of_above")
async def handle_none_of_above(action: cl.Action):
    # Handle "None of the above" selection
    await cl.Message("❌ Sorry, please try another query.").send()


@cl.action_callback("select_snippet_0")
@cl.action_callback("select_snippet_1")
@cl.action_callback("select_snippet_2")
async def handle_snippet_selection(action: cl.Action):
    # Retrieve the results from the user session
    results = cl.user_session.get("_last_results")

    # Get the selected snippet based on the payload index
    selected_snippet = results[action.payload["index"]]

    # Store the selected snippet in the user session
    cl.user_session.set("selected_snippet", selected_snippet)

    # Start the chat phase
    cl.user_session.set("chat_history", [])
    await cl.Message(f"✅ You selected Snippet {action.payload['index']+1}. You can now ask questions about this code or ask me to generate tests.").send()


@cl.on_chat_start
async def start():
    # Clear the user session at the start of a new chat
    cl.user_session.set("selected_snippet", None)
    cl.user_session.set("chat_history", [])
    await cl.Message("👋 Welcome! Ask me to find code snippets from your repositories. I'll fetch the top 3 relevant pieces.").send()