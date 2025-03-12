import enum
from datetime import datetime, timedelta

SUBSCRIPTION_PLAN_ERROR_MESSAGE = "Incorrect Value"


class PlanType(enum.Enum):
    """
    Types of Subscription Plan.
    """
    ANNUAL = 1
    MONTHLY = 2


class Language(enum.Enum):
    """
    Language of Subscriptions.
    """
    ENG = 1
    AR = 2


class SubscriptionName(enum.Enum):
    """
    Name of Subscription.
    """
    NETFLIX = 1
    AMAZON_PRIME = 2


PLANS_MAPPERS_DURATION = {
    PlanType.ANNUAL: timedelta(days=365),
    PlanType.MONTHLY: timedelta(days=30),
}


class SubscriptionPlans:
    def __init__(self, plan_type: PlanType, features: list, price: float, active: bool = True):
        self.plan_type = plan_type
        self.features = features
        self.price = price
        self.active = active


class Subscription(object):
    """
    Subscription class, Manage different plans.
    """

    def __init__(
            self,
            plan_type: SubscriptionPlans,
            subscription_name: SubscriptionName,
            language: Language = Language.AR,
            start_data: datetime = datetime.now()
    ):
        self.subscription_name = subscription_name
        if isinstance(plan_type, SubscriptionPlans):
            self.plan_type = plan_type
        else:
            raise TypeError(SUBSCRIPTION_PLAN_ERROR_MESSAGE)
        self.language = language
        self.start_date = start_data
        self.end_date = self.start_date + PLANS_MAPPERS_DURATION.get(self.plan_type.plan_type)

    def cancel(self) -> None:
        """
        Cancel subscription.
        :return: None
        """
        self.plan_type.active = False

    def activate(self) -> None:
        """
        Activate subscription.
        :return: None
        """
        self.plan_type.active = True

    def renew(self):
        if not self.plan_type.active:
            self.activate()
        self.start_date = datetime.now()
        self.end_date = self.start_date + PLANS_MAPPERS_DURATION.get(self.plan_type.plan_type)

    def current_subscription_time(self):
        return self.start_date
