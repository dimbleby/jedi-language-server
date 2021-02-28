"""Tests for document completion requests."""

import copy

from hamcrest import assert_that, is_

from tests import TEST_DATA
from tests.lsp_test_client import session
from tests.lsp_test_client.defaults import VSCODE_DEFAULT_INITIALIZE
from tests.lsp_test_client.utils import as_uri

COMPLETION_TEST_ROOT = TEST_DATA / "completion"


def test_lsp_completion() -> None:
    """Test a simple completion request.

    Test Data: tests/test_data/completion/completion_test1.py
    """

    with session.LspSession() as ls_session:
        ls_session.initialize()
        uri = as_uri(COMPLETION_TEST_ROOT / "completion_test1.py")
        actual = ls_session.text_document_completion(
            {
                "textDocument": {"uri": uri},
                "position": {"line": 8, "character": 2},
                "context": {"triggerKind": 1},
            }
        )

        expected = {
            "isIncomplete": False,
            "items": [
                {
                    "label": "my_function",
                    "kind": 3,
                    "detail": None,
                    "documentation": None,
                    "deprecated": False,
                    "preselect": False,
                    "sortText": "z",
                    "filterText": "my_function",
                    "insertText": "my_function()$0",
                    "insertTextFormat": 2,
                    "textEdit": None,
                    "additionalTextEdits": None,
                    "commitCharacters": None,
                    "command": None,
                    "data": None,
                }
            ],
        }
        assert_that(actual, is_(expected))

        actual = ls_session.completion_item_resolve(
            {
                "label": "my_function",
                "kind": 3,
                "sortText": "z",
                "filterText": "my_function",
                "insertText": "my_function()$0",
                "insertTextFormat": 2,
            }
        )
        expected = {
            "label": "my_function",
            "kind": 3,
            "detail": "def my_function",
            "documentation": {
                "kind": "markdown",
                "value": "```\nmy_function()\n\nSimple test function.\n```\n",
            },
            "deprecated": None,
            "preselect": None,
            "sortText": "z",
            "filterText": "my_function",
            "insertText": "my_function()$0",
            "insertTextFormat": 2,
            "textEdit": None,
            "additionalTextEdits": None,
            "commitCharacters": None,
            "command": None,
            "data": None,
        }
        assert_that(actual, is_(expected))


def test_eager_lsp_completion() -> None:
    """Test a simple completion request, with eager resolution.

    Test Data: tests/test_data/completion/completion_test1.py
    """

    with session.LspSession() as ls_session:
        # Initialize, asking for eager resolution.
        initialize_params = copy.deepcopy(VSCODE_DEFAULT_INITIALIZE)
        initialize_params["initializationOptions"] = {
            "completion": {"resolveEagerly": True}
        }
        ls_session.initialize(initialize_params)

        uri = as_uri(COMPLETION_TEST_ROOT / "completion_test1.py")
        actual = ls_session.text_document_completion(
            {
                "textDocument": {"uri": uri},
                "position": {"line": 8, "character": 2},
                "context": {"triggerKind": 1},
            }
        )

        # pylint: disable=line-too-long
        expected = {
            "isIncomplete": False,
            "items": [
                {
                    "label": "my_function",
                    "kind": 3,
                    "detail": "def my_function",
                    "documentation": {
                        "kind": "markdown",
                        "value": "```\nmy_function()\n\nSimple test function.\n```\n",
                    },
                    "deprecated": False,
                    "preselect": False,
                    "sortText": "z",
                    "filterText": "my_function",
                    "insertText": "my_function()$0",
                    "insertTextFormat": 2,
                    "textEdit": None,
                    "additionalTextEdits": None,
                    "commitCharacters": None,
                    "command": None,
                    "data": None,
                }
            ],
        }
        assert_that(actual, is_(expected))
