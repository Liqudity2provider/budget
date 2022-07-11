from datetime import datetime, timedelta

import requests
from django.core.exceptions import ImproperlyConfigured

from actions.models import Action
from integrations.models import UserIntegration


class IntegrationManager:
    def __init__(self, user):
        self.user = user
        self.integrations = UserIntegration.objects.filter(
            user=user)

    def process_integrations(self):
        # now only for monobank

        for integration in self.integrations:
            if integration.type_of_integration == "monobank":
                mim = MonobankIntegrationManager(integration.user_integration_info, user=self.user)
                mim.import_activities_from_bank()


class MonobankIntegrationManager:
    def __init__(self, user_integration_info, user, card_currency=980, days_ago=30):
        self.CARD_CURRENCY = card_currency
        self.DAYS_AGO = days_ago
        self.user = user

        self.user_integration_info = user_integration_info
        self.token = user_integration_info.get("token")
        if not self.token:
            raise ImproperlyConfigured(
                "can't find required filed 'token' for monobank integration")

    def import_activities_from_bank(self):

        json_data = self.get_json_data_from_bank_api()

        for activity in json_data:
            date = datetime.fromtimestamp(activity["time"]) if activity.get("time") else None

            if self.check_action_on_existance(date, activity):
                continue

            new_action = Action.objects.create(
                name=activity.get("description", "Please fill name"),
                date=date,
                amount=activity["amount"] / 100 if activity.get("amount") else None,
                user=self.user,
                details=activity.get("description", "Please fill description"),
            )
            new_action.save()

    def get_timestamp_timedelta(self):
        today = datetime.today()
        period_of_days = int((today - timedelta(days=self.DAYS_AGO)).timestamp())
        return period_of_days

    def get_json_data_from_bank_api(self):
        period_of_days = self.get_timestamp_timedelta()
        for i in range(2):
            try:
                acc_id = None
                client_info = requests.get(
                    "https://api.monobank.ua/personal/client-info",
                    headers={"X-Token": self.token})
                info_client_json = client_info.json()

                for acc in info_client_json["accounts"]:
                    if acc["currencyCode"] == self.CARD_CURRENCY and acc["type"] != 'eAid':
                        acc_id = acc["id"]
            except Exception as e:
                print(e.args)
            else:
                break

        res = requests.get(
            f"https://api.monobank.ua/personal/statement/{acc_id}/{period_of_days}",
            headers={"X-Token": self.token})
        return res.json()

    def check_action_on_existance(self, date, activity):
        existing_action = Action.objects.filter(
            date=date,
            user=self.user,
            amount=activity["amount"] / 100 if activity.get("amount") else None,
        )
        if existing_action:
            return True
