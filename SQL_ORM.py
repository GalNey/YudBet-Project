__author__ = 'Gal Neystadt 2020'

import sqlite3
import datetime

import pickle
    # https://docs.python.org/2/library/sqlite3.html
    # https://www.youtube.com/watch?v=U7nfe4adDw8

log_path = "db_log.txt"

def log_data(data):
    global log_path

    with open(log_path, "a") as f:
        f.write("at: " + str(datetime.datetime.now()) + " | " + data + "\n")


class Identified_ObjectsORM():
    def __init__(self, path):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor
        self.path = path
    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.current=self.conn.cursor()
        
        
    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    #adds photo to db
    def add_photo(self, path, identification_time, camera_id, camera_name, bookmark, when_updated, free_text=""):
        self.open_DB()
        sql = "INSERT INTO identified_photos (path, identificitionTime, cameraId, cameraName, freeText, bookMark, whenUpdated) VALUES ('" + path + "','" + identification_time + "'," + str(camera_id) + ",'" + camera_name + "','" + free_text + "','" + str(bookmark) + "','" + when_updated + "')"
        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("New photo added")
        return ans

    #gets photo path by id
    def get_photo_path_by_id(self, id):
        self.open_DB()
        sql = "SELECT path FROM Identified_photos WHERE rowid IS " + id

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s path was withdrawn" % id)
        return ans

    # gets photo free text by id
    def get_photo_text_by_id(self, id):
        self.open_DB()
        sql = "SELECT freeText FROM Identified_photos WHERE rowid IS " + id

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s text was withdrawn" % id)
        return ans

    # gets photo with lowest id
    def get_photo_lowest_id(self):
        self.open_DB()
        sql = "SELECT MIN(rowid) FROM Identified_photos"
        #sql = "SELECT path FROM Identified_photos WHERE rowid = (SELECT MIN(rowid) FROM Identified_photos"

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("lowest id of current photos was withdrawn")
        return self.get_photo_path_by_id(ans.replace("(", "").replace(")", "").replace(",", ""))

    # deletes photo path by id
    def delete_photo_by_id(self, id):
        self.open_DB()
        sql = "DELETE FROM Identified_photos WHERE rowid IS " + id

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s was deleted" % id)
        return ans

    # bookmark photo path by id
    def bookmark_photo_by_id(self, id):
        self.open_DB()
        sql = "UPDATE Identified_photos SET bookmark = True WHERE rowid IS " + id
        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        reco_time = str(datetime.datetime.now())[:-3]

        sql = "UPDATE Identified_photos SET whenUpdated = '" + reco_time + "' WHERE rowid IS " + id
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s was bookmarked" % id)
        return ans

    # set free text of photo path by id
    def set_text_of_photo_by_id(self, id, text):
        self.open_DB()
        sql = "UPDATE Identified_photos SET freeText = '" + text + "' WHERE rowid IS " + id

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        reco_time = str(datetime.datetime.now())[:-3]

        sql = "UPDATE Identified_photos SET whenUpdated = '" + reco_time + "' WHERE rowid IS " + id
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s was set to '%s'" % (id, text))
        return ans

    # unbookmark photo path by id
    def unbookmark_photo_by_id(self, id):
        self.open_DB()
        sql = "UPDATE Identified_photos SET bookmark = False WHERE rowid IS " + id

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        reco_time = str(datetime.datetime.now())[:-3]

        sql = "UPDATE Identified_photos SET whenUpdated = '" + reco_time + "' WHERE rowid IS " + id
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

        log_data("Photo with id of %s was unbookmarked" % id)
        return ans

    # gets list of all photos
    def get_list_of_photos(self):
        self.open_DB()
        sql = "SELECT rowid, identificitionTime, cameraId, cameraName FROM Identified_photos"

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("list of all photos was withdrawn")
        return ans

    # gets list of all photos which are bookmarked
    def get_list_of_bookmark_photos(self):
        self.open_DB()
        sql = "SELECT rowid, identificitionTime, cameraId, cameraName FROM Identified_photos WHERE bookMark IS True"

        res = self.current.execute(sql)

        ans = ""
        for answer in res:
            ans += str(answer)

        self.commit()
        self.close_DB()

        log_data("list of all bookmarked photos was withdrawn")
        return ans

def main_test():

    db = Identified_ObjectsORM()

    #db.add_photo("ident_phts\\tests.jpg", "yesterday", 1, "yard", False, "yesterday", free_text="testing")
    #db.get_photo_path_by_id(1)
    #print(db.get_list_of_photos())
    #db.delete_photo_path_by_id(3)
    db.bookmark_photo_by_id("2")
    #db.unbookmark_photo_by_id(1)
    #db.get_list_of_bookmark_photos()
    #db.set_text_of_photo_by_id(5, "hello")



if __name__ == "__main__":
    main_test()


