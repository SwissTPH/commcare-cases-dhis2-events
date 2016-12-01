import json

from six import iteritems

class Case:
    """ Class for converting Commcare cases into processable Case objects"""

    def __init__(self, obj):

        # only get CLOSED cases because editing them with this connector is not supported
        case_date = obj.get('date_closed', None)
        if not case_date:
            raise ValueError(
                "Commcare cases must be closed. Set Commcare request headers accordingly (Closed=True)")
        else:
            self.case_date = case_date[:10]

        self.case_id = obj['case_id']

        # get the properties of the Commcare case
        properties = obj['properties']

        # case must have orgunit property
        self.orgunit = obj['properties'].get('userLocationOrgUnitID', None)
        if self.orgunit is None:
            raise ValueError("No orgunit ID provided for case_id {}".format(self.case_id))
        else:
            properties.pop('userLocationOrgUnitID')

        # standardize Boolean properties
        true_values = ['1', 1, True, 'yes', 'Yes', 'YES']
        false_values = ['0', 0, False, 'no', 'No', 'NO']
        for k, v in iteritems(properties):
            # standardize TRUE values
            if v in true_values:
                properties[k] = True
            # standardize FALSE values
            elif v in false_values:
                properties[k] = False
            # keep String values (e.g. for category options in DHIS2)
            elif isinstance(v, str):
                continue

        # remove NULL values
        filtered = {k: v for k, v in iteritems(properties) if v != None}

        # set Case instance attribute for each property
        for k, v in iteritems(filtered):
            setattr(self, k, v)

    def __iter__(self):
        return self

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
