import sqlite3

class Subscription:
    ...



def create_connection():
    return sqlite3.connect('subscription.db')


def create_subscription_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS subscription(plan_type, subscription_name, language, created_at, updated_at, start_date, end_date, active)")
    conn.commit()


if __name__ == '__main__':
    print(Subscription().__str__())

    # create_subscription_table()
