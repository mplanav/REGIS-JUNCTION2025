def mock_chat_reply(user_message: str) -> str:
    """
    Temporary mock response so frontend can proceed while Gemini is not active.
    """
    return (
        "This is a temporary mock response from the REGIS AI assistant. "
        "Your message was: " + user_message
    )
