import unittest

from . import settings
from .data import valid_data
from .data import invalid_data
from craftai.client import CraftAIClient
from craftai import errors as craft_err


class TestGetDecisionTreeSuccess(unittest.TestCase):
    """Checks that the client succeeds when retrieving an agent's decision tree
    at a given timestamp, with OK input.
    """
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_decision_tree_with_correct_input(self):
        """get_decision_tree should succeed when given proper ID and timestamp.

        It should give a proper JSON list response with 3 elements.
        """
        decision_tree = self.client.get_decision_tree(
            valid_data.VALID_ID,
            valid_data.VALID_TIMESTAMP)

        self.assertIsInstance(decision_tree, list)
        self.assertEqual(len(decision_tree), 3)


class TestGetDecisionTreeFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent's decision
    tree at a given timestamp with bad input."""
    @classmethod
    def setUpClass(self):
        self.client = CraftAIClient(settings.CRAFT_CFG)

    def setUp(self):
        self.client.delete_agent(valid_data.VALID_ID)
        self.client.create_agent(valid_data.VALID_MODEL, valid_data.VALID_ID)
        self.client.add_operations(
            valid_data.VALID_ID,
            valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        self.client.delete_agent(valid_data.VALID_ID)

    def test_get_decision_tree_with_invalid_id(self):
        """get_decision_tree should fail when given a non-string/empty string ID

        It should raise an error upon request for retrieval of an agent's
        decision tree with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.get_decision_tree,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_TIMESTAMP)

    def test_get_decision_tree_with_unknown_id(self):
        """get_decision_tree should fail when given an unknown agent ID

        It should raise an error upon request for the retrieval of an agent
        that doesn't exist.
        """
        self.assertRaises(
            craft_err.CraftAINotFoundError,
            self.client.get_decision_tree,
            invalid_data.UNKNOWN_ID,
            valid_data.VALID_TIMESTAMP)

    def test_get_decision_tree_with_invalid_timestamp(self):
        for inv_ts in invalid_data.INVALID_TIMESTAMPS:
            self.assertRaises(
                craft_err.CraftAIBadRequestError,
                self.client.get_decision_tree,
                valid_data.VALID_ID,
                invalid_data.INVALID_TIMESTAMPS[inv_ts])