import sqlite3
from unittest.mock import MagicMock

import pytest

from subscription_system.subscription_sqlite import create_connection, create_subscription_table


@pytest.fixture(scope='module')
def mocked_sqlite():
    sqlite3.connect = MagicMock()
    return sqlite3


def test_create_connection_connection(mocked_sqlite):
    expected_db_name = 'subscription.db'
    create_connection()
    mocked_sqlite.connect.assert_called_with(expected_db_name)


def test_create_table(mocked_sqlite):
    create_table_statement = "CREATE TABLE IF NOT EXISTS subscription(plan_type, subscription_name, language, created_at, updated_at, start_date, end_date, active)"
    create_subscription_table()
    mocked_sqlite.connect.return_value.cursor.return_value.execute.assert_called_with(create_table_statement)
    mocked_sqlite.connect.return_value.commit.assert_called()
