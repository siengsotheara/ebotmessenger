import requests
import json

class FacebookUtil(object):
    """
    Handle common handle facebook event
    """

    _uri = "https://graph.facebook.com/v2.6/"

    def __init__(self):
        pass


    def handle_webhook(self, json_data):
        pass

    def _user_profile(self, id, access_token):
        _uri = _uri + id + "?fields=first_name,last_name,gender,locale,timezone,profile_pic&access_token=" + access_token
        data = requests.get(url=_uri)
        return json.dumps(data)

class UserProfile(object):

    def __init__(self, results=None, **option):
        if results is None:
            results = {}
        self.results = results

    @property
    def first_name(self):
        return self.results.get("first_name", None)

    @property
    def last_name(self):
        return self.results.get("last_name", None)

    @property
    def profile_pic(self):
        return self.results.get("profile_pc", None)

    @property
    def id(self):
        return self.results.get("id", None)

    @property
    def locale(self):
        return self.results.get("locale", None)

    @property
    def gender(self):
        return self.results.get("gender", None)
    
    @property
    def timezone(self):
        return self.results.get("timezone", None)

