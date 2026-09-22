"""User - the abstract base class for everyone in the system.

ABSTRACTION: User is an abstract class (it inherits from ABC and has
abstract methods), so it cannot be created directly. Only Student and
Mentor, which fill in the missing methods, can be created.
"""

from abc import ABC, abstractmethod


class User(ABC):
    """Base class shared by Student and Mentor."""

    # Class attributes - shared by the whole class, not by one object
    total_users = 0        # counts users of every kind
    created = 0            # counts users of one particular class
    id_prefix = "USR"

    def __init__(self, name, email):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address: " + str(email))

        User.total_users += 1          # shared counter
        type(self).created += 1        # Student and Mentor each count their own
        self.name = name
        self._user_id = self.id_prefix + "-" + str(type(self).created).zfill(3)

        # ENCAPSULATION: two underscores makes this attribute private.
        # It can only be read or changed through the email property below.
        self.__email = email.lower()

    # ------------------------------------------------------------------
    # Encapsulation: private data exposed through properties
    # ------------------------------------------------------------------
    @property
    def user_id(self):
        """Read-only ID. There is no setter, so it can never be changed."""
        return self._user_id

    @property
    def email(self):
        """Read the private email."""
        return self.__email

    @email.setter
    def email(self, new_email):
        """Change the email, but only if it is valid."""
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address: " + str(new_email))
        self.__email = new_email.lower()

    # ------------------------------------------------------------------
    # Abstraction: every subclass must write these two methods
    # ------------------------------------------------------------------
    @abstractmethod
    def role(self):
        """Return the role name, for example Student or Mentor."""

    @abstractmethod
    def describe(self):
        """Return one line describing this person."""

    # ------------------------------------------------------------------
    # Instance method - works on one object and uses its own data
    # ------------------------------------------------------------------
    def show_profile(self):
        """Return a profile line built from the data of this object."""
        return "[" + self.role() + "] " + self.user_id + " | " + self.name + " | " + self.email

    # ------------------------------------------------------------------
    # Static method - a helper that needs no object at all.
    # Can be called as User.is_valid_email("a@b.com")
    # ------------------------------------------------------------------
    @staticmethod
    def is_valid_email(email):
        """Return True if the email looks like name@domain.com."""
        if not isinstance(email, str) or email.count("@") != 1:
            return False
        name_part, domain_part = email.split("@")
        return len(name_part) > 0 and "." in domain_part

    # ------------------------------------------------------------------
    # Class method - receives the class (cls) instead of the object
    # ------------------------------------------------------------------
    @classmethod
    def count(cls):
        """Return how many users of all kinds have been created."""
        return User.total_users

    def __str__(self):
        """Called by print(user)."""
        return self.name + " (" + self.role() + ")"
