class UserEntity:
    """
    KAVRAM #43: Entity - PostgreSQL'deki 'users' tablosunun Python nesnesidir.
    """
    def __init__(self, user_id: str, email: str, hashed_password: str, role: str):
        self.user_id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
