"""Blocking API operation; callers must run it off the GUI thread."""
import openai


def execute_query(query, model, api_key):
    try:
        # A per-request client avoids process-global key state and closes
        # its transport even on errors. Do not retry paid requests silently.
        with openai.OpenAI(api_key=api_key, timeout=30.0, max_retries=0,
                           base_url='https://api.openai.com/v1') as client:
            response = client.responses.create(
                model=model,
                input=query,
                store=False,
            )
        if response.status == 'incomplete':
            return 'Error: The response was incomplete. Try a shorter request.', False
        if response.status != 'completed':
            return 'Error: The API did not complete the response.', False
        response_text = response.output_text
        if not response_text or not response_text.strip():
            return 'Error: The API returned no text response.', False
        return response_text, True
    except openai.AuthenticationError:
        return 'Error: Authentication failed. Check your API key.', False
    except openai.RateLimitError:
        return 'Error: Rate or quota limit reached. Check your API account.', False
    except openai.APITimeoutError:
        return 'Error: The API request timed out. Try again later.', False
    except openai.APIConnectionError:
        return 'Error: Could not connect to OpenAI. Check your connection.', False
    except openai.APIStatusError:
        return 'Error: The API rejected the request. Check the model ID and account access.', False
    except Exception:
        # Provider error bodies may contain prompt content or credentials.
        return 'Error: The request failed unexpectedly.', False

