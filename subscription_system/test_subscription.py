import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from subscription_system.subscription import (
    Subscription, SubscriptionPlans,
    PLANS_MAPPERS_DURATION,
    PlanType,
    Language,
    SubscriptionName
)


class SubscriptionPlansTestCase(unittest.TestCase):
    def test_subscription_plans(self):
        subscription_plan = SubscriptionPlans(
            plan_type=PlanType.ANNUAL,
            price=150.0,
            features=[
                "annual_package", "discounted_total"
            ]
        )

        self.assertEqual(subscription_plan.plan_type, PlanType.ANNUAL)
        self.assertEqual(subscription_plan.price, 150.0)
        self.assertEqual(subscription_plan.features, ["annual_package", "discounted_total"])
        self.assertEqual(len(subscription_plan.features), 2)


class SubscriptionTestCase(unittest.TestCase):
    def test_subscription(self):
        subscription_plan = SubscriptionPlans(
            plan_type=PlanType.ANNUAL,
            price=150.0,
            features=[
                "annual_package", "discounted_total"
            ],
            active=False
        )
        start_date = datetime(2020, 1, 1)
        overdue_subscription = Subscription(
            subscription_name=SubscriptionName.AMAZON_PRIME,
            plan_type=subscription_plan,
            language=Language.AR,
            start_data=start_date,
        )
        self.assertEqual(overdue_subscription.subscription_name, SubscriptionName.AMAZON_PRIME)
        self.assertEqual(overdue_subscription.plan_type, subscription_plan)
        self.assertTrue(isinstance(overdue_subscription, Subscription))
        self.assertEqual(overdue_subscription.language, Language.AR)
        self.assertEqual(overdue_subscription.start_date, start_date)
        self.assertEqual(overdue_subscription.start_date.month, 1)
        self.assertEqual(overdue_subscription.start_date.day, 1)
        self.assertFalse(overdue_subscription.plan_type.active)
        overdue_subscription.renew()
        self.assertEqual(overdue_subscription.start_date.year, datetime.now().year)
        self.assertTrue(overdue_subscription.plan_type.active)
        annual_end_date = datetime.now() + timedelta(days=365)
        self.assertEqual(overdue_subscription.end_date.year, annual_end_date.year)

        default_subscription = Subscription(
            subscription_name=SubscriptionName.AMAZON_PRIME,
            plan_type=subscription_plan,
            language=Language.AR,
        )
        self.assertEqual(default_subscription.subscription_name, SubscriptionName.AMAZON_PRIME)
        self.assertEqual(default_subscription.start_date.year, datetime.now().year)
        self.assertEqual(default_subscription.start_date.month, datetime.now().month)
        self.assertEqual(default_subscription.start_date.day, datetime.now().day)
        one_year_from_now = datetime.now() + timedelta(days=365)
        self.assertEqual(default_subscription.end_date.year, one_year_from_now.year)

    def test_subscription_plans_annual_monthly(self):
        plans_annual = SubscriptionPlans(
            plan_type=PlanType.ANNUAL,
            price=150.0,
            features=[
                "annual_package", "discounted_amount"
            ]
        )
        plans_monthly = SubscriptionPlans(
            plan_type=PlanType.MONTHLY,
            price=200.0 / 12,
            features=[
                "monthly_package", "full_amount"
            ]
        )
        self.assertEqual(plans_annual.plan_type, PlanType.ANNUAL)
        self.assertEqual(len(plans_annual.features), 2)
        self.assertEqual(plans_monthly.plan_type, PlanType.MONTHLY)
        self.assertTrue(isinstance(plans_monthly, SubscriptionPlans))
        self.assertEqual(plans_monthly.active, True)

    def test_incorrect_plan_type(self):
        with self.assertRaises(TypeError) as exception_context:
            Subscription(
                subscription_name=SubscriptionName.AMAZON_PRIME,
                plan_type="Annual",
            )
        self.assertEqual(str(exception_context.exception), "Incorrect Value")

    def test_cancel_subscription(self):
        plans_monthly = SubscriptionPlans(
            plan_type=PlanType.MONTHLY,
            price=200.0 / 12,
            features=[
                "monthly_package", "full_amount"
            ]
        )
        monthly_subscription = Subscription(
            plan_type=plans_monthly,
            language=Language.AR,
            subscription_name=SubscriptionName.NETFLIX,
        )
        self.assertEqual(monthly_subscription.plan_type, plans_monthly)
        self.assertTrue(monthly_subscription.plan_type.active)
        self.assertEqual(monthly_subscription.subscription_name, SubscriptionName.NETFLIX)
        monthly_subscription.cancel()
        self.assertFalse(monthly_subscription.plan_type.active)

    def test_activate_subscription(self):
        plans_monthly = SubscriptionPlans(
            plan_type=PlanType.MONTHLY,
            price=200.0 / 12,
            features=[
                "monthly_package", "full_amount"
            ],
            active=False
        )
        monthly_subscription = Subscription(
            plan_type=plans_monthly,
            language=Language.AR,
            subscription_name=SubscriptionName.AMAZON_PRIME
        )
        self.assertEqual(monthly_subscription.plan_type, plans_monthly)
        self.assertEqual(monthly_subscription.subscription_name, SubscriptionName.AMAZON_PRIME)
        self.assertFalse(monthly_subscription.plan_type.active)
        monthly_subscription.activate()
        self.assertTrue(monthly_subscription.plan_type.active)

    def test_plan_mappers(self):
        plan_mapper = PLANS_MAPPERS_DURATION
        self.assertEqual(plan_mapper.get(PlanType.ANNUAL), timedelta(days=365))

@pytest.fixture(scope='module')
def subscription_fixture():
    Subscription = MagicMock()
    return Subscription

@pytest.fixture(scope='module')
def mock_datetime():
    mocked_datetime = MagicMock(return_value=datetime(2025, 3, 1 ))
    return mocked_datetime

def test_mocked_start_date(subscription_fixture, mock_datetime):
    plans_monthly = SubscriptionPlans(
        plan_type=PlanType.MONTHLY,
        price=200.0 / 12,
        features=[
            "monthly_package", "full_amount"
        ],
        active=False
    )
    subscription_fixture(
        subscription_plan=plans_monthly,
        language=Language.AR,
        start_date=mock_datetime,
    )

    subscription_fixture.assert_called_once_with(
        subscription_plan=plans_monthly,
        language=Language.AR,
        start_date=mock_datetime,
    )

if __name__ == '__main__':
    unittest.main()
