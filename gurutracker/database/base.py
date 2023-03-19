from abc import ABC, abstractmethod


class Base(ABC):
    """Base

    Use this as a base for all database classes. All methods except
    `sql_query` are mandatory to implement. For a full working example,
    see `mysql.py`.
    """
    
    @abstractmethod
    def list_all_subjects(self):
        pass
    
    @abstractmethod
    def get_subject_by_uid(self):
        pass
    
    @abstractmethod
    def add_subject(self, subject):
        pass
    
    @abstractmethod
    def edit_subject(self, subject):
        pass
    
    @abstractmethod
    def delete_subject(self, subject):
        pass

    @abstractmethod
    def list_all_assignments(self):
        pass
    
    @abstractmethod
    def get_assignment_by_id(self, id):
        pass
    
    @abstractmethod
    def get_assignment_by_uid(self, uid):
        pass
    
    @abstractmethod
    def search_assignment_by_name_instr(self, name):
        pass

    @abstractmethod
    def search_uid_by_name_instr(self, name):
        pass
    
    @abstractmethod
    def search_assignment_by_tags(self, tags):
        pass

    @abstractmethod
    def add_assignment(self, assignment):
        pass

    @abstractmethod
    def edit_assignment(self, assignment):
        pass

    @abstractmethod
    def del_assignment(self, assignment):
        pass

    @abstractmethod
    def list_tutors(self):
        pass
        
    @abstractmethod
    def get_tutor_by_uid(self, uid):
        pass

    @abstractmethod
    def add_tutor(self, tutor):
        pass

    @abstractmethod
    def edit_tutor(self, tutor):
        pass

    @abstractmethod
    def delete_tutor(self, tutor):
        pass

    @abstractmethod
    def list_tags(self):
        pass
        
    @abstractmethod
    def search_tag_by_text_instr(self, text):
        pass
        
    @abstractmethod
    def get_tag(self, text):
        pass

    @abstractmethod
    def add_tag(self, tag):
        pass

    @abstractmethod
    def edit_tag(self, tag):
        pass

    @abstractmethod
    def delete_tag(self, tag):
        pass

    @abstractmethod
    def tag_assignment(self, assignment, tag):
        pass

    @abstractmethod
    def untag_assignment(self, assignment, tag):
        pass
        
    @abstractmethod
    def assignment_tags(self, assignment):
        pass
        
    @abstractmethod
    def tagged_assignments(self, assignment):
        pass

    def sql_query(self):
        pass
