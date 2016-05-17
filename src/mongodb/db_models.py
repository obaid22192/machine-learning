from __future__ import absolute_import


class User(dict):
    """Data model for User, DynamicDocument allows to add fields dynamically"""
    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.itemlist = super(User, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(User, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)


class ProjectData(dict):
    """
        Data model for Project data, DynamicDocument allows to add fields
        dynamically
    """
    def __init__(self, *args, **kw):
        super(ProjectData, self).__init__(*args, **kw)
        self.itemlist = super(ProjectData, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(ProjectData, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)


class Project(dict):
    """
        Data model for Project, DynamicDocument allows to add fields
        dynamically
    """
    # user_id is string field because this id is autogenrated by mongodb.
    def __init__(self, *args, **kw):
        super(Project, self).__init__(*args, **kw)
        self.itemlist = super(Project, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(Project, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)


class DatasetInfo(dict):
    """
        Data model for Dataset information.
    """
    # user_id is string field because this id is autogenrated by mongodb.
    def __init__(self, *args, **kw):
        super(DatasetInfo, self).__init__(*args, **kw)
        self.itemlist = super(DatasetInfo, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(DatasetInfo, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)


class ProjectInfoData(dict):
    """
        Data model for Dataset information.
    """
    # user_id is string field because this id is autogenrated by mongodb.
    def __init__(self, *args, **kw):
        super(ProjectInfoData, self).__init__(*args, **kw)
        self.itemlist = super(ProjectInfoData, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(ProjectInfoData, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)
    # user_id = None
    # project_name = None
    # project_creation_date = None


class Results(dict):
    """
    Data model for Experiments results.
    """
    # user_id is string field because this id is autogenrated by mongodb.
    def __init__(self, *args, **kw):
        super(Results, self).__init__(*args, **kw)
        self.itemlist = super(Results, self).keys()

    def __setitem__(self, key, value):
        # TODO: what should happen to the order if
        #       the key is already in the dict
        # self.itemlist.append(key)
        super(Results, self).__setitem__(key, value)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)
