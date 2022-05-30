import uuid

def gen_uuid(name:str, len:int=8) -> str:
    """
    Generate uuid for each application
    """
    return str(uuid.uuid4())[:len]