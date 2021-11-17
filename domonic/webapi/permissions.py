"""
    domonic.webapi.permissions
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Permissions
"""


class PermissionStatus:
    """
    The PermissionStatus interface represents the current state of a permission.
    """
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return self.status

    def __repr__(self):
        return self.status

    @property
    def state(self):
        """
        The state of the permission.
        state replaces status
        """
        return self.status

    @state.setter
    def state(self, value):
        self.status = value


class Permissions:

    @staticmethod
    def query(PermissionDescriptor):
        """
        Returns a boolean value indicating whether the user agent has the
        specified permission.
        """
        pass

    @staticmethod
    def request(PermissionDescriptor):
        """
        Requests permission from the user agent.
        """
        pass

    # @staticmethod
    # def revoke(PermissionDescriptor):
    #     """
    #     Revokes the permission.
    #     """
    #     pass

    @staticmethod
    def requestAll():
        """
        Requests all permissions at once.
        """
        pass

    # @staticmethod
    # def revokeAll():
    #     """
    #     Revokes all permissions at once.
    #     """
    #     pass

