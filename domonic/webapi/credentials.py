"""
    domonic.webapi.credentials
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Credential_Management_API
"""


class CredentialsContainer:

    @staticmethod
    def create(self):
        """ Returns a Promise that resolves with a new Credential instance based on the provided options,
        or null if no Credential object can be created. In exceptional circumstances, the Promise may reject."""
        raise NotImplementedError

    @staticmethod
    def get(self):
        """ Returns a Promise that resolves with the Credential instance that matches the provided parameters."""
        raise NotImplementedError

    @staticmethod
    def preventSilentAccess(self):
        """ Sets a flag that specifies whether automatic log in is allowed for future visits to the current origin,
        then returns an empty Promise. For example, you might call this, after a user signs out of a website to ensure that they aren't automatically signed in on the next site visit. Earlier versions of the spec called this method requireUserMediation(). See Browser compatibility for support details."""
        raise NotImplementedError

    @staticmethod
    def store(self):
        """ Stores a set of credentials for a user, inside a provided Credential instance and returns that instance in a Promise."""
        raise NotImplementedError