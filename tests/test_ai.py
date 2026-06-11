# tests/test_ai.py
import os
import sys

print("cwd =", os.getcwd())
print("sys.path =", sys.path)
from unittest.mock import MagicMock, patch

import app.ai as ai


def test_summarize_article_returns_summary_text():
    # Arrange: mock Claude API response
    fake_message = MagicMock()
    fake_message.content[0].text = "Short summary."

    # Act: change on time block to substitute real call with fake
    with patch.object(ai.client.messages, "create", return_value=fake_message):
        result = ai.summarize_article("текст статьи")

    # Assert: function returned summary text
    assert result == "Short summary."
