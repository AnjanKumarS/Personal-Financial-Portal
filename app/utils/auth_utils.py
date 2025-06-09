def validate_password(password):
    """
    Validate password meets minimum requirements
    - At least 8 characters
    - Contains at least one letter and one number
    """
    if len(password) < 8:
        return False
    
    has_letter = False
    has_number = False
    
    for char in password:
        if char.isalpha():
            has_letter = True
        if char.isdigit():
            has_number = True
    
    return has_letter and has_number
