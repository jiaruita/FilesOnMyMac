import db_model

class FSModel(object):
    def __init__(self):
        try:
            self.db = db_model.SqliteModel()
        except Exception as e:
            print "got exception in FSModel init: " + str(e)
            exit(1)





