from app import db

class Snapshot(db.Model):
    api_key = db.Column(db.String(128), primary_key=True)
    inventory = db.Column(db.String(20000))
    materials = db.Column(db.String(20000))

    def __init__(self, api_key, inventory, materials):
        self.api_key = api_key
        self.inventory = inventory
        self.materials = materials

    def __repr__(self):
        return '<API Key %r>' % self.api_key
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name
