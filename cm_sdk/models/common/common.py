from json import JSONEncoder
import json
import logging
from enum import Enum
from cm_sdk.models.common.string_utils import to_camel_case, convert_dict_keys, Case

__author__ = 'e0d'


class CloudManagerJSONEncoder(JSONEncoder):
    """
    A custom JSON encoder to provide transparent conversion between
    CloudManager JSON format and the Python classes that represent API
    objects in the SDK.
    """

    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, CloudManagerEnum):
            return o.to_json()
        elif hasattr(o, "state"):
            # converts class parameter names from snake case to camel case expected
            # by the API and prunes nulls
            return dict((to_camel_case(k), v) for k, v in o.state.iteritems() if v is not None)
        else:
            return None


class CloudManagerBase(object):

    """
    Base class for python representations of CloudManager API objects that provides
    utility methods for static initialization, factors out common attributes and
    provides common API object equivalence checks.
    """
    # All API objects have these attributes
    COMMON_API_ATTRIBUTES = ['id', 'group_id', 'links', 'created']
    # The following attributes are ignored for determine whether instances are equivalent.
    # This is useful when determining if a non-persitant entity duplicates one that was
    # created previously.
    EQUIVALENCE_IGNORED_ATTRIBUTES = ['id', 'group_id', 'links', 'created', 'updated']

    def __init__(self, my_api_attributes):

        all_api_attributes = self.COMMON_API_ATTRIBUTES + my_api_attributes
        vars(self).update(all_api_attributes=all_api_attributes, state={})

    def equivalent(self, other):
        """
        Compares two API Objects, but ignoring specified attributes.
        This allows determining whether an object created locally
        is equivalent to one that was create previously.
        """

        _self = json.loads(self.to_json())
        _other = json.loads(other.to_json())
        filtered_self = self.remove_keys(_self, CloudManagerBase.EQUIVALENCE_IGNORED_ATTRIBUTES)
        filtered_other = self.remove_keys(_other, CloudManagerBase.EQUIVALENCE_IGNORED_ATTRIBUTES)

        return filtered_self == filtered_other

    @staticmethod
    def remove_keys(obj, to_remove):
        """
        Removes specified keys from a nested dict.  Used to determined the deep equivalence of API objects.  Keys, like
        ID, created, updated, that are set on the server side do not materially influence the equivalence of objects
        like AlertConfigs or Backups.
        """
        if isinstance(obj, dict):
            obj = {
                key: CloudManagerBase.remove_keys(value, to_remove)
                for key, value in obj.iteritems()
                if key not in to_remove}
        elif isinstance(obj, list):
            obj = [CloudManagerBase.remove_keys(item, to_remove)
                   for item in obj
                   if item not in to_remove]
        return obj

    @staticmethod
    def get_class_from_name(kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])

        try:
            m = __import__(module)
        except ImportError:
            raise CloudManagerException("Unable to import module {module} dynamically.".format(module=module))

        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    def __getattr__(self, name):
        if name in self.state:
            return self.state[name]
        else:
            raise AttributeError("No such attribute {name} for instance of class {klass}.".format(
                name=name,
                klass=type(self).__name__
            ))

    def __iter__(self):
        return self.state.keys().__iter__()

    def __setattr__(self, name, value):

        if name not in self.all_api_attributes:
            raise CloudManagerValidationException("Attribute {0} is not allowable for type {1}".
                                                  format(name, type(self).__name__))

        # Verify that the name in the JSON corresponds to list of children defined by each model.
        # If it is, we dispatch here to get an instance of the appropriate object or enum
        if name in self.children:

            if isinstance(value, list):
                value = self.get_children(name, value)
            else:
                value = self.get_child(name, value)

        # Do not store nil values
        if value is not None:
            self.state[name] = value

    def get_child(self, name, value):
        if isinstance(value, (CloudManagerEnum, CloudManagerBase)):
            return value
        else:
            if value is None:
                return value
            else:
                return self.get_child_from_value(name, value)

    def get_child_from_value(self, name, value):

        if hasattr(self, "children") \
                and name in self.children:
            try:
                klass = self.children[name]['class']

                if issubclass(klass, self.get_class_from_name('cm_sdk.models.common.common.CloudManagerEnum')):
                    try:
                        value = klass[value]
                    except KeyError:
                        logging.warn("Enum {0} has no key {1}".format(klass, value))
                elif issubclass(klass, self.get_class_from_name('cm_sdk.models.common.common.CloudManagerBase')):
                    value = klass.from_dict(value)
                else:
                    raise CloudManagerValidationException(
                        "Cannot marshall class {0} in deserializing from API JSON".format(klass.__class__))

            except AttributeError:
                print "Problem with {name}".format(name=name)

        return value

    def get_children(self, name, items):

        to_return = []

        for item in items:
            if isinstance(item, CloudManagerBase) or isinstance(item, CloudManagerEnum):
                to_return.append(item)
            else:
                to_return.append(self.get_child(name, item))

        return to_return

    @classmethod
    def from_json(cls, json_in):
        _dict = json.loads(json_in)
        return cls.from_dict(convert_dict_keys(_dict, Case.SNAKE))

    @classmethod
    def from_dict(cls, dict_in):
        instance = cls()
        converted = convert_dict_keys(dict_in, Case.SNAKE)

        for k, v in converted.items():
            setattr(instance, k, v)
        return instance

    def to_json(self):
        return json.dumps(self, cls=CloudManagerJSONEncoder)


class OrderedEnum(Enum):
    """
    Needed to provide implicit iteration for "in" checks for API related enums
    """
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ >= other._value_
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ > other._value_
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ <= other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ < other._value_
        return NotImplemented


class CloudManagerEnum(OrderedEnum):

    def to_json(self):
        """
        Return the value of the current instance of the Enum for JSON
        serialization.
        """
        return str(self.value)


class CloudManagerException(Exception):
    pass


class CloudManagerValidationException(CloudManagerException):
    pass