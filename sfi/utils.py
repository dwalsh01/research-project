from pathlib import PurePath

def get_project_root():
    ''' Returns the path of the project root.'''
    
    root =  PurePath(__file__).parent.parent
    return root 
