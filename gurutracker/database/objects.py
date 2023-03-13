class Subject(object):
    def __init__(self, id=None, name=None, desc=None, uidentifier=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.uidentifier = uidentifier
    
    def __repr__(self):
        return "<Tutor {}, name={}, desc={}, uidentifier={}>".format(
            self.id, self.name, self.desc, self.uidentifier
        )

class Tutor(object):
    def __init__(self, id=None, name=None, uidentifier=None, subject=None):
        """__init__

        The Tutor object represent a single tutor.

        Args:
            id (int, optional):
                The ID in the database. Defaults to None.
            name (str, optional):
                Name of the tutor. Defaults to None.
            uid (str, optional): Tutor UID. Defaults to None.
            subject (str, optional): Subject object. Defaults to None.
        """
        self.id = id
        self.name = name
        self.uidentifier = uidentifier
        self.subject = subject
    
    def __repr__(self):
        return "<Tutor {}, name={}, uidentifier={}, subject={}>".format(
            self.id, self.name, self.uidentifier, self.subject
        )


class Assignment(object):
    def __init__(self, id=None, name=None, uidentifier=None, type=None, tutor=None, completed=None):
        """__init__

        Refers to an Assignment.

        Args:
            id (int, optional): ID. Defaults to None.
            name (str, optional): Name. Defaults to None.
            uidentifier (str, optional): UID. Defaults to None.
            type (str, optional): Type. Defaults to None.
            tutor (Tutor, optional):
                A `Tutor` object representing the tutor. Must have the
                ID attribute populated. Defaults to None.
        """
        self.id = id
        self.name = name
        self.uidentifier = uidentifier
        self.type = type
        self.tutor = tutor
    
    def __repr__(self):
        return "<Assignment {}, name={}, uidentifier={}, type={}, tutor={}>".format(
            self.id, self.name, self.uidentifier, self.type, self.tutor
        )


class Tag(object):
    def __init__(self, id=None, text=None, fgcolor=None, bgcolor=None):
        self.id = id
        self.text = text
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        
    def __repr__(self):
        return "<Tag {}, text={}, fgcolor={}, bgcolor={}>".format(
            self.id, self.text, self.fgcolor, self.bgcolor
        )
