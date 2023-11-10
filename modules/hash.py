import hashlib

class Hash(object):
    def __init__(self):
        pass
    
    def hashPassword(self, password):
        self.password = password.encode('utf-8')
        
        hash_object = hashlib.sha256(self.password)
        hashed_pw = hash_object.hexdigest()
        return hashed_pw
        
    def checkHash(self, entered_password):
        self.entered_password = entered_password
        
        
        
        
        