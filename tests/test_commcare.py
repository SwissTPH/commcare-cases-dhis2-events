import pytest

from app.commcare import CommcareHandler


class TestCommcareHandler:
    @pytest.fixture
    def cc_response_with(self):
        ex_response = {
            "meta": {
                'total_count': 3
            },
            "cases": [
                {
                    "case_id": "45WKYXQRFFU3AT4Y022EX7HF2",
                    "closed": False,
                    "date_closed": None,
                    "date_modified": "2012-03-13T18:21:52Z",
                    "domain": "demo",
                    "indices": {},
                    "properties": {
                        "case_name": "ryan",
                        "case_type": "programmer",
                        "date_opened": "2012-03-13T18:21:52Z",
                        "external_id": "45WKYXQRFFU3AT4Y022EX7HF2",
                        "gender": "m",
                        "languages": "python java javascript c php erlang love",
                        "owner_id": None,
                        "role": "artisan"
                    },
                    "server_date_modified": "2012-04-05T23:56:41Z",
                    "server_date_opened": "2012-04-05T23:56:41Z",
                    "user_id": "06414101dc45bcfdc963b8cb1a1ebdfd",
                    "version": "1.0",
                    "xform_ids": [
                        "3HQEXR2S0GIRFY2GF40HAR7ZE"
                    ]
                },
                {
                    "case_id": "45WKYXQRFFU2AT4Y022EX7HF2",
                    "closed": False,
                    "date_closed": None,
                    "date_modified": "2012-03-13T18:21:52Z",
                    "domain": "demo",
                    "indices": {},
                    "properties": {
                        "case_name": "ryan",
                        "case_type": "programmer",
                        "date_opened": "2012-03-13T18:21:52Z",
                        "external_id": "45WKYXQRFFU3AT4Y022EX7HF2",
                        "gender": "m",
                        "languages": "python java javascript c php erlang love",
                        "owner_id": None,
                        "role": "artisan"
                    },
                    "server_date_modified": "2012-04-05T23:56:41Z",
                    "server_date_opened": "2012-04-05T23:56:41Z",
                    "user_id": "06414101dc45bcfdc963b8cb1a1ebdfd",
                    "version": "1.0",
                    "xform_ids": [
                        "3HQEXR2S0GIRFY2GF40HAR7ZE"
                    ]
                },
                {
                    "case_id": "45WKYXQSADF34Y022EX7HF2",
                    "closed": False,
                    "date_closed": None,
                    "date_modified": "2012-03-13T18:21:52Z",
                    "domain": "demo",
                    "indices": {},
                    "properties": {
                        "case_name": "ryan",
                        "case_type": "programmer",
                        "date_opened": "2012-03-13T18:21:52Z",
                        "external_id": "45WKYXQRFFU3AT4Y022EX7HF2",
                        "gender": "m",
                        "languages": "python java javascript c php erlang love",
                        "owner_id": None,
                        "role": "artisan"
                    },
                    "server_date_modified": "2012-04-05T23:56:41Z",
                    "server_date_opened": "2012-04-05T23:56:41Z",
                    "user_id": "06414101dc45bcfdc963b8cb1a1ebdfd",
                    "version": "1.0",
                    "xform_ids": [
                        "3HQEXR2S0GIRFY2GF40HAR7ZE"
                    ]
                }
            ]
        }

        return ex_response

    def test_cases_available(self, cc_response_with):
        try:
            cch = CommcareHandler(None, None, None, None, None)
            cases_available = cch.cases_available(cc_response_with)
            assert cases_available is True
        except ValueError:
            pass


    @pytest.fixture
    def cc_response_without(self):
        ex_response = {
            "meta": {
                'total_count': None
            },
            "cases": []
        }

        return ex_response

    def test_no_cases_available(self, cc_response_without):
        try:
            cch = CommcareHandler(None, None, None, None, None)
            cases_available = cch.cases_available(cc_response_without)
            assert cases_available is not True
        except ValueError:
            pass

    @pytest.fixture
    def cc_response_none(self):
        ex_response = None
        return ex_response

    def test_none_cases(self, cc_response_none):
        try:
            cch = CommcareHandler(None, None, None, None, None)
            cases_available = cch.cases_available(cc_response_none)
            assert cases_available is not True
        except ValueError:
            pass

    def test_commcare_without_credentials(self):
        with pytest.raises(ValueError) as e:
            CommcareHandler(None, None, None, None, None)

    def test_commcare_with_wrong_api_url(self):
        with pytest.raises(ValueError) as e:
            CommcareHandler(url="https://www.commcarehq.org/a/domain/api/v0.3/case", username="admin", password="password", case_type="some_case")
