from gurutracker.database.objects import Assignment, Tutor, Tag
from gurutracker.globals import controller

def list_to_objects(item):
    teac = Tutor(id=item[4],
                 name=item[5],
                 uidentifier=item[6],
                 subject=item[7],
                 level=item[8])
    ass = Assignment(id=int(item[0]),
                     name=item[1],
                     uidentifier=item[2],
                     type=item[3],
                     tutor=teac)
                     
    return ass

def taglist_to_objects(item):
    if isinstance(item[2], int):
        item[2] = "{:06d}".format(item[2])
    
    if isinstance(item[3], int):
        item[3] = "{:06d}".format(item[3])
    
    return Tag(id=int(item[0]),
               text=str(item[1]),
               fgcolor=item[2],
               bgcolor=item[3])
    
    
def get_cobject_tags(item, tags_y=None, tags_n=None):
    #GET Completed OBJECT TAGS
    if item.type == "test":
        if item:
            return tags_y
        else:
            return tags_n
            
def tv_tag_config(treeview):
    for tag in controller.list_tags():
        if tag.fgcolor or tag.bgcolor:
            treeview.tag_configure(f"tag_{tag.id}", foreground="#{}".format(tag.fgcolor) if tag.fgcolor else "#000000", background="#{}".format(tag.bgcolor) if tag.bgcolor else "#ffffff")
            
def color_treeview_item(item):
    tags = ()
    for tag in controller.assignment_tags(item):
        tags += (f"tag_{tag.id}",)
        
    return tags
    
def tagname_list(taglist):
    """Convert a list of Tag objects into a list with their names instead.

    Args:
        taglist (list): A list of Tag objects

    Returns:
        list[str]: A list of tag names.
    """
    lst = []
    for tag in taglist:
        lst.append(tag.text)
        
    return lst