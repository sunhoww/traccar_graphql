import unittest

from traccar_graphql.utils import camelify_keys

class TestUtilsCamelifyKeys:
    def test_flat_dict(self):
        assert camelify_keys({ 'first_name': "Tony", 'last_name': "Stark" }) == \
            { 'firstName': "Tony", 'lastName': "Stark" }
    def test_nested_dict(self):
        assert camelify_keys({ 'org_name': "S.H.I.E.L.D.", 'contact': { 'first_name': "Maria" } }) == \
            { 'orgName': "S.H.I.E.L.D.", 'contact': { 'firstName': "Maria" } }
    def test_list_of_dicts(self):
        assert camelify_keys({ 'assets': [{ 'unique_id': 'MK_VIII', 'status': 'active' }, { 'unique_id': 'MK_XIIc', 'status': 'unknown' }] }) == \
            { 'assets': [{ 'uniqueId': 'MK_VIII', 'status': 'active' }, { 'uniqueId': 'MK_XIIc', 'status': 'unknown' }] }
    def test_complex(self):
        assert camelify_keys({
            'first_name': "Tony",
            'affliated_to': { 'org_name': "Stark Industries", 'affliations': [{ 'org_name': "Avengers" }, { 'org_name': "S.H.I.E.L.D.", 'contact': { 'first_name': "Maria" } }] },
            'likes': ["Shawarma", { 'id': "MK_I", "top_speed": 300 }],
            'keys': [[{ 'primary_key': 23, 'access': "Parker Residence"}, { 'secondary_key': 1 }], [{ 'primary_key': 12, 'access': "Avenger Tower"}]] }) == \
            {
            'firstName': "Tony",
            'affliatedTo': { 'orgName': "Stark Industries", 'affliations': [{ 'orgName': "Avengers" }, { 'orgName': "S.H.I.E.L.D.", 'contact': { 'firstName': "Maria" } }] },
            'likes': ["Shawarma", { 'id': "MK_I", "topSpeed": 300 }],
            'keys': [[{ 'primaryKey': 23, 'access': "Parker Residence"}, { 'secondaryKey': 1 }], [{ 'primaryKey': 12, 'access': "Avenger Tower"}]] }
