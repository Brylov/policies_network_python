import json

import pytest
from stage3 import PolicyAPI


@pytest.fixture
def api():
    return PolicyAPI()

@pytest.fixture
def foo_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "foo",
                "description": "my foo policy",
                "type": "Arupa",
            }
        )
    )

@pytest.fixture
def bar_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "bar",
                "description": "my bar policy",
                "type": "Arupa",
            }
        )
    )
@pytest.fixture
def frisco_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "barfoo",
                "description": "my bar policy",
                "type": "Frisco",
            }
        )
    )

@pytest.fixture
def bar_rule_identifier(api, frisco_policy_identifier):
    first_bar_rule_json = api.create_rule(
        frisco_policy_identifier,
        json.dumps(
                {
                    "name": "bar",
                    "ip_proto": "TCP",
                    "source_port":"80",
                    "source_ip":"10.0.1.15",
                    "destination_ip":"0.0.0.0"
                }
        )
    )
    second_bar_rule_json = api.create_rule(
        frisco_policy_identifier,
        json.dumps(
                {
                    "name": "bar1",
                    "ip_proto": "TCP",
                    "source_port":"8080",
                    "source_ip":"10.0.1.16",
                    "destination_ip":"0.0.0.0"
                }
        )
    )
    return json.dumps({'policyID':frisco_policy_identifier,'ruleID':first_bar_rule_json})

@pytest.fixture
def foo_rule_identifier(api, foo_policy_identifier):
    first_foo_policy_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                    {
                        "name": "foo",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_subnet":"10.0.0.0/16"
                    }
            )
        )
    second_foo_policy_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                    {
                        "name": "foo1",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_subnet":"10.0.0.0/16"
                    }
            )
        )
    return json.dumps({'policyID':foo_policy_identifier,'ruleID':first_foo_policy_json})

    

class TestCreatePolicy:
    def test_type_validation(self, api):
        with pytest.raises(Exception):
            api.create_policy(
                json.dumps(
                    {
                        "name": "foo",
                        "description": "my foo policy",
                        "type": "invalid",
                    }
                )
            )

    def test_name_must_be_unique_for_arupa_policies(self, api, foo_policy_identifier):
        with pytest.raises(Exception):
            api.create_policy(
                json.dumps(
                    {
                        "name": "foo",
                        "description": "another foo policy",
                        "type": "Arupa",
                    }
                )
            )

    def test_name_can_be_duplicated_for_frisco_policies(self, api):
        first_foo_policy_json = api.create_policy(
            json.dumps(
                {
                    "name": "foo",
                    "description": "my foo policy",
                    "type": "Frisco",
                }
            )
        )
        another_foo_policy_json = api.create_policy(
            json.dumps(
                {
                    "name": "foo",
                    "description": "another foo policy",
                    "type": "Frisco",
                }
            )
        )
        first_foo_policy_identifier = json.loads(first_foo_policy_json)
        another_foo_policy_identifier = json.loads(another_foo_policy_json)
        assert first_foo_policy_identifier != another_foo_policy_identifier
        


class TestReadPolicy:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.read_policy(json.dumps("invalid"))

    def test_consistent_response_for_same_policy(self, api, foo_policy_identifier):
        assert api.read_policy(foo_policy_identifier) == api.read_policy(
            foo_policy_identifier
        )

    def test_different_response_for_different_policies(
        self, api, foo_policy_identifier, bar_policy_identifier
    ):
        assert api.read_policy(foo_policy_identifier) != api.read_policy(
            bar_policy_identifier
        )

    def test_returns_valid_json(self, api, foo_policy_identifier):
        json.loads(api.read_policy(foo_policy_identifier))

    def test_returns_dict_with_fields(self, api, foo_policy_identifier):
        policy = json.loads(api.read_policy(foo_policy_identifier))
        assert isinstance(policy, dict)
        assert policy["name"] == "foo"
        assert policy["description"] == "my foo policy"
        assert policy["type"] == "Arupa"


class TestUpdatePolicy:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.update_policy(
                json.dumps("invalid"),
                json.dumps(
                    {
                        "name": "foo",
                        "description": "my foo policy",
                        "type": "Arupa",
                    }
                ),
            )

    def test_invalid_fields(self, api, foo_policy_identifier):
        with pytest.raises(Exception):
            api.update_policy(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "bar",
                        "description": "my foo policy",
                        "type": "invalid",
                    }
                ),
            )

    def test_update_description(self, api, foo_policy_identifier):
        api.update_policy(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "foo",
                    "description": "my bar policy",
                    "type": "Arupa",
                }
            ),
        )
        updated_policy = json.loads(api.read_policy(foo_policy_identifier))
        assert updated_policy["name"] == "foo"
        assert updated_policy["description"] == "my bar policy"
        assert updated_policy["type"] == "Arupa"

    def test_failed_update_is_idempotent(self, api, foo_policy_identifier):
        foo_policy = api.read_policy(foo_policy_identifier)
        with pytest.raises(Exception):
            api.update_policy(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "foo",
                        "description": "my foo policy",
                        "type": "invalid",
                    }
                ),
            )
        assert api.read_policy(foo_policy_identifier) == foo_policy


class TestDeletePolicy:
    def test_no_read_or_update_after_delete(self, api, foo_policy_identifier):
        api.read_policy(foo_policy_identifier)
        api.delete_policy(foo_policy_identifier)
        with pytest.raises(Exception):
            api.read_policy(foo_policy_identifier)
        with pytest.raises(Exception):
            api.update_policy(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "bar",
                        "description": "my foo policy",
                        "type": "Arupa",
                    }
                ),
            )


class TestListPolicies:
    def test_list_one(self, api, foo_policy_identifier):
        policies = json.loads(api.list_policies())
        assert len(policies) == 1
        [policy] = policies
        assert isinstance(policy, dict)
        assert policy["name"] == "foo"
        assert policy["description"] == "my foo policy"
        assert policy["type"] == "Arupa"

    def test_list_multiple(self, api, foo_policy_identifier, bar_policy_identifier):
        assert len(json.loads(api.list_policies())) == 2

class TestCreateRule:
    def test_create_rule_frisco(self, frisco_policy_identifier, api):
        first_bar_policy_json = api.create_rule(
            frisco_policy_identifier,
            json.dumps(
                    {
                        "name": "foo",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_ip":"10.0.1.15",
                        "destination_ip":"0.0.0.0"
                    }
            )
        )
    def test_create_rule_arupa(self, foo_policy_identifier, api):
        first_foo_policy_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                    {
                        "name": "foo",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_subnet":"10.0.0.0/16"
                    }
            )
        )
    def test_create_rule_frisco_duplicate(self, frisco_policy_identifier, api):
        first_foo_policy_json = api.create_rule(
            frisco_policy_identifier,
            json.dumps(
                    {
                        "name": "bar",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_ip":"10.0.1.15",
                        "destination_ip":"0.0.0.0"
                    }
            )
        )
        first_foo_policy_json = api.create_rule(
            frisco_policy_identifier,
            json.dumps(
                    {
                        "name": "bar1",
                        "ip_proto": "TCP",
                        "source_port":"8080",
                        "source_ip":"10.0.1.16",
                        "destination_ip":"0.0.0.0"
                    }
            )
        )
        with pytest.raises(Exception):
            first_foo_policy_json = api.create_rule(
                frisco_policy_identifier,
                json.dumps(
                        {
                            "name": "bar",
                            "ip_proto": "TCP",
                            "source_port":"80",
                            "source_ip":"10.0.1.15",
                            "destination_ip":"0.0.0.0"
                        }
                )
            )
    def test_create_rule_arupa_duplicate(self, foo_policy_identifier, api):
        first_foo_policy_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                    {
                        "name": "foo",
                        "ip_proto": "TCP",
                        "source_port":"80",
                        "source_subnet":"10.0.0.0/16"
                    }
            )
        )
        first_foo_policy_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                    {
                        "name": "foo1",
                        "ip_proto": "TCP",
                        "source_port":"81",
                        "source_subnet":"10.0.1.0/24"
                    }
            )
        )
        with pytest.raises(Exception):
            first_foo_policy_json = api.create_rule(
                foo_policy_identifier,
                json.dumps(
                        {
                            "name": "foo",
                            "ip_proto": "TCP",
                            "source_port":"80",
                            "source_subnet":"101.0.0.0/16"
                        }
                )
            )

class TestListRules:
    def test_list_one(self, api, foo_rule_identifier):
        ids = json.loads(foo_rule_identifier)
        rules = json.loads(api.list_rules(ids['policyID']))
        assert len(rules) == 2
        for rule in rules:
            assert isinstance(rule, dict)
            assert "name" in rule
            assert "ip_proto" in rule
            assert "source_port" in rule
            assert "source_subnet" in rule
            
            # Perform specific assertions for each rule
            if rule["name"] == "foo":
                assert rule["ip_proto"] == "TCP"
                assert rule["source_port"] == "80"
                assert rule["source_subnet"] == "10.0.0.0/16"

class TestReadRule:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.read_rule(json.dumps({"policyID":"0","ruleID":"invalid"}))

    def test_consistent_response_for_same_rule(self, api, foo_rule_identifier):
        assert api.read_rule(foo_rule_identifier) == api.read_rule(
            foo_rule_identifier
        )

    def test_different_response_for_different_rules(
        self, api, foo_rule_identifier, bar_rule_identifier
    ):
        assert api.read_rule(foo_rule_identifier) != api.read_rule(
            bar_rule_identifier
        )

    def test_returns_valid_json(self, api, foo_rule_identifier):
        json.loads(api.read_rule(foo_rule_identifier))

    def test_returns_dict_with_fields(self, api, foo_rule_identifier):
        rule = json.loads(api.read_rule(foo_rule_identifier))
        assert isinstance(rule, dict)
        assert rule["name"] == "foo"
        assert rule["ip_proto"] == "TCP"
        assert rule["source_port"] == "80"
        assert rule["source_subnet"] == "10.0.0.0/16"

class TestDeleteRule:
    def test_no_read_or_update_after_delete(self, api, foo_rule_identifier):
        api.read_rule(foo_rule_identifier)
        api.delete_rule(foo_rule_identifier)
        with pytest.raises(Exception):
            api.read_rule(foo_rule_identifier)
        with pytest.raises(Exception):
            api.update_rule(
                foo_rule_identifier,
                json.dumps(
                    {
                        "name": "foochanged",
                        "ip_proto": "UDP",
                        "source_port": "8080",
                        "source_subnet": "10.0.1.0/16"
                    }
                ),
            )

class TestUpdateRule:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.update_rule(
                json.dumps({"policyID": {"id": 0}, "ruleID": {"id": 999}}),
                json.dumps({"name": "foo", "ip_proto": "tcp", "source_port": 80})
            )

    def test_invalid_fields(self, api, foo_policy_identifier, foo_rule_identifier):
        with pytest.raises(Exception):
            api.update_rule(
                foo_rule_identifier,
                json.dumps(
                    {
                        "name": "foo",
                        "ip_proto": "http",
                        "source_port": '80',
                        "source_subnet": "10.0.1.0/16"
                    }
                ),
            )

    def test_update_rule(self, api, foo_policy_identifier, foo_rule_identifier):
        api.update_rule(
            foo_rule_identifier,
            json.dumps(
                {
                    "name": "fooUpdate",  # Corrected the name here
                    "ip_proto": "TCP",
                    "source_port": '80',
                    "source_subnet": "10.0.1.0/16"
                }
            ),
        )
        updated_rule = json.loads(api.read_rule(foo_rule_identifier))
        assert updated_rule["name"] == "fooUpdate"  # Corrected the expected name here
        assert updated_rule["ip_proto"] == "TCP"
        assert updated_rule["source_port"] == '80'
        assert updated_rule["source_subnet"] == "10.0.1.0/16"

    def test_failed_update_is_idempotent(self, api, foo_policy_identifier, foo_rule_identifier):
        foo_rule = api.read_rule(foo_rule_identifier)
        with pytest.raises(Exception):
            api.update_rule(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "bar",
                        "ip_proto": "invalid",
                        "source_port": '80'
                    }
                ),
            )
        assert api.read_rule(foo_rule_identifier) == foo_rule



    