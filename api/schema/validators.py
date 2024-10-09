def validate_any_of(cls, v):
    if not any(v.values()):
        raise ValueError('At least one field must have a value.')
    return v
