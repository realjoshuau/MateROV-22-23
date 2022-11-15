class Database:
    def __init__(self, checklist):
        self.checklist = checklist

    def deleteTask(self):
        for i in self.checklist:
            if(self.checklist[i] == "undone"):
                self.checklist[i] = "done"
                break
        print(self.checklist)
        return
    
    def getTasks(self):
        return self.checklist