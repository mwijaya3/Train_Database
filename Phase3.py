#CS 4400 Phase III Source Code
#Members - Mario Wijaya, Masud Parvez, Ousmane Kaba, Wenlu Fu
#Demo date/time:  Tuesday 4/26/2016 2:15pm - 3:00pm
#Team #23
#We worked on this project only using stackoverflow.com and this semester's course materials.
from tkinter import *
import random
import csv
import re
import urllib.request
import time
import datetime
from operator import itemgetter
import copy
import statistics
import pymysql




class Phase3:

    def __init__(self, rootWin):
        self.ResDict={"Train ":["##","##"]," Time (Duration) ":["##", "##"]," Departs From ":[" ## "," ## "], " Arrives at ":["  ## "," ##  "], " Class ":[" ## "," ## "]," Price ":[" $$ "," $$ "]," #of Baggage ":[" ## "," ## "], " Passenger Name ":[" ## "," ## "]}
        ##self.ResDict will keep track of #of reservation made and all the other information regarding to the resevation like time, price etc:
        self.LoginPage()
        self.NumberOfReservation=1
        self.pricebagbag = 0
        self.totalCostCost = 0
        self.currentselection = []
        self.masud=0
        self.trackManFunc=0
        self.checkDupTrain=[]
    def LoginPage(self): #Login page
        rootWin.title("GTTrain.com")
        self.loginLab = Label(rootWin, text = "Login")
        self.loginLab.grid(row = 1, column = 4, columnspan = 4, sticky = EW)
        self.userLab = Label(rootWin, text = "Username")
        self.userLab.grid(row = 2, column = 0, sticky = E)
        self.userEntry = Entry(rootWin, width = 30)
        self.userEntry.grid(row = 2, column = 4, sticky = W)
        self.passLab = Label(rootWin, text = "Password")
        self.passLab.grid(row = 4, column = 0, sticky = E)
        self.passEntry = Entry(rootWin, width = 30)
        self.passEntry.grid(row = 4, column = 4, sticky = W)
        self.loginBut = Button(rootWin, text = "Login", padx = 10, command = self.LoginCheck) #command to be put in
        self.loginBut.grid(row = 6, column = 0, sticky = E)
        self.registerBut = Button(rootWin, text = "Register", padx = 10, command = self.RegisterPage) #command to be put in
        self.registerBut.grid(row = 6, column = 4, sticky = W)

    def Connect(self): #connect to database
        try:
            self.db = pymysql.connect(host = 'YOURHOST',
                                      passwd = 'PASSWORD', user = 'USERNAME', db='DATABASE')
            self.a1 = True

            return self.db
        except:
            messagebox.showerror("Error", "Check your internet connection")
            self.a1 = False

    def RegisterPage(self): #New User Registration Page
        rootWin.withdraw()
        self.register = Toplevel(rootWin)
        self.register.title("GTtrain.com Register Page")
        self.newUserLab = Label(self.register, text = "New User Registration")
        self.newUserLab.grid(row = 1, column = 4, columnspan = 6, sticky = W)
        self.usernameLab = Label(self.register, text = "Username")
        self.usernameLab.grid(row = 3, column = 1, sticky = E)
        self.usernameEntry = Entry(self.register, width = 30)
        self.usernameEntry.grid(row = 3, column = 3, sticky = E)
        self.emailLab = Label(self.register, text = "Email Address")
        self.emailLab.grid(row = 5, column = 1, sticky = E)
        self.emailEntry = Entry(self.register, width = 30)
        self.emailEntry.grid(row = 5, column = 3, sticky = E)
        self.newpassLab = Label(self.register, text = "Password")
        self.newpassLab.grid(row = 7, column = 1, sticky = E)
        self.newpassEntry = Entry(self.register, width = 30)
        self.newpassEntry.grid(row = 7, column = 3, sticky = E)
        self.conpassLab = Label(self.register, text = "Confirm Password")
        self.conpassLab.grid(row = 9, column = 1, sticky = E)
        self.conpassEntry = Entry(self.register, width = 30)
        self.conpassEntry.grid(row = 9, column = 3, sticky = E)
        self.createBut = Button(self.register, text = "Create", padx = 10, command = self.RegisterNew)
        self.createBut.grid(row = 11, column = 3, sticky = EW)

    def RegisterNew(self):
        self.Connect()
        self.usernameDB = []
        self.usernameDBlower = []
        self.listCheck = []
        self.emailDB = []
        self.emailDBlower = []
        self.Connect() #connect to database
        cursor2 = self.db.cursor()
        sql_custcust = '''SELECT C_Username, Email FROM Customer'''
        cursor2.execute(sql_custcust)

        for each in cursor2:
            self.usernameDB.append(each[0]) #Grab all the username from database
            self.emailDB.append(each[1]) #Grab all the email from database
        for i in range(len(self.emailDB)):
            self.emailDBlower.append(self.emailDB[i].lower()) #convert all email from database to lowercase
        for i in range(len(self.usernameDB)):
            self.usernameDBlower.append(self.usernameDB[i].lower()) #convert all Customer username from Database to lowercase
        if self.usernameEntry.get().lower() not in self.usernameDBlower: #check customer username to database
            self.listCheck.append(1)
        else:
            self.listCheck.append(2)
            messagebox.showerror("Error", "Username already exists")
        if self.newpassEntry.get() == self.conpassEntry.get(): #check if user input same password and confirm password
            self.listCheck.append(1)
        else:
            self.listCheck.append(2)
            messagebox.showerror("Error", "Password do not match, please try again")

        regexgex = re.findall('[^@]+@[^@]+\.[^@]+',self.emailEntry.get())


        if self.emailEntry.get() not in self.emailDBlower and len(regexgex) != 0: #Check email against database
            self.listCheck.append(1)
            if '.edu' in self.emailEntry.get(): #to check whether the email is student or not
                self.studentCheck = '1'
            else:
                self.studentCheck = '0'
        else:
            self.listCheck.append(2)
            messagebox.showerror("Error", "Email already exists in database or incorrect email input")
        if len(self.usernameEntry.get()) != 0 and len(self.newpassEntry.get()) != 0 and len(self.conpassEntry.get()) != 0 and len(self.emailEntry.get()) != 0: #check if any field is empty
            self.listCheck.append(1)
        else:
            self.listCheck.append(2)
            messagebox.showerror("Error", "Reinput any blank field")
        sql_insertEverything = '''INSERT INTO Customer(C_Username, C_Password, Email, Is_student) VALUES (%s, %s, %s, %s)''' #insert customer to table "Customer"
        if sum(self.listCheck) == 4: #check if information provided on gui is correct
            self.Connect()
            cursor = self.db.cursor()
            cursor.execute(sql_insertEverything, (self.usernameEntry.get(), self.newpassEntry.get(), self.emailEntry.get(), self.studentCheck)) #execute to database
            self.register.withdraw() #go back to login page from registration page
            rootWin.deiconify()



    def LoginCheck(self):
        #reserve for functionality
        self.Connect()
        if self.a1 == True:

            cursor = self.db.cursor()
            cursor1 = self.db.cursor()
            self.custUsername = []
            self.custPassword = []
            self.manUsername = []
            self.manPassword = []
            sql_custall = '''SELECT C_Username,C_Password FROM Customer''' #sql to get Customer Username and Password
            sql_manall = '''SELECT M_Username, M_Password FROM Manager'''  #sql to get Manager Username and Password
            cursor.execute(sql_custall)
            cursor1.execute(sql_manall)

            for each in cursor: #store Customer username and password
                self.custUsername.append(each[0])
                self.custPassword.append(each[1])
            for each in cursor1: #Store manager username and password
                self.manUsername.append(each[0])
                self.manPassword.append(each[1])

            self.userLog = self.userEntry.get() #to grab username that is typed on login entry
            self.passLog = self.passEntry.get() #to grab password that is typed on password entry
            if self.userLog in self.custUsername and self.passLog in self.custPassword:
                messagebox.showinfo(title = "Success", message = "You logged in successfully")
                rootWin.withdraw()
                self.custFunc()
            elif self.userLog in self.manUsername and self.passLog in self.manPassword:
                messagebox.showinfo(title = "Success", message = "You logged in successfully")
                rootWin.withdraw()
                self.ManagerFunc()
            else:
                messagebox.showerror("Error", "Unrecognizable Username/Password Combinations")







    def custFunc(self): #customer functionality
        self.chofunc = Toplevel(rootWin)
        self.cholab = Label(self.chofunc, text = "Choose Functionality")
        self.cholab.grid(row = 1, column = 1, columnspan = 8, sticky = E)
        self.viewtrain = Button(self.chofunc, text = "View Train Schedule", command=self.viewTrain) #proceed to view train
        self.viewtrain.grid(row = 2, column = 1, columnspan = 2, sticky = E)
        self.newreserve = Button(self.chofunc, text = "Make a new reservation", command = self.reservation) #proceed to reservation
        self.newreserve.grid(row = 3, column = 1, columnspan = 2, sticky = E)
        self.updateRev = Button(self.chofunc, text = "Update a reservation", command=self.UpdateReservation) #proceed to update
        self.updateRev.grid(row = 4, column = 1, columnspan = 2, sticky = E)
        self.cancelRev = Button(self.chofunc, text = "Cancel a reservation", command=self.CancelReservation) # proceed to cancel
        self.cancelRev.grid(row = 5, column = 1, columnspan = 2, sticky = E)
        self.giveRev = Button(self.chofunc, text = "Give review", command=self.GiveReview) #proceed to give review
        self.giveRev.grid(row = 6, column = 1, columnspan = 2, sticky = E)
        self.addSchool = Button(self.chofunc, text = "Add school Information(student discount)", command=self.addSchoolInfo) #proceed to add school info
        self.addSchool.grid(row = 7, column = 1, columnspan = 2, sticky = E)
        self.viewRev1 = Button(self.chofunc, text = "View Review", command = self.ViewReview)
        self.viewRev1.grid(row = 8, column = 1, columnspan = 2, sticky = E)
        self.logoutbut = Button(self.chofunc, text = "Log out", command=self.LogOutCust)
        self.logoutbut.grid(row = 10, column = 3, sticky = EW)

    def addSchoolInfo(self): #add school info window
        self.chofunc.withdraw()
        self.schoolInfo = Toplevel(rootWin)
        self.schoollab = Label(self.schoolInfo, text = "Add School Info")
        self.schoollab.grid(row = 1, column =1, sticky = W)
        self.schoolent = Entry(self.schoolInfo, width = 30)
        self.schoolent.grid(row = 1, column = 2, sticky = E)
        self.edulab = Label(self.schoolInfo, text = "Your school email address ends with .edu")
        self.edulab.grid(row = 2, column = 1, sticky = W)
        self.backChofunc = Button(self.schoolInfo, text = "Back", padx = 10, command = self.backSchool) #command to go back custFunc
        self.backChofunc.grid(row = 4, column = 1, sticky = E)
        self.subChofunc = Button(self.schoolInfo, text = "Submit", padx = 10, command = self.subSchool) #command back to custFunc
        self.subChofunc.grid(row = 4, column = 2, sticky = E)

    def backSchool(self): #back to customer functionality
        self.schoolInfo.withdraw()
        self.chofunc.deiconify()
    def subSchool(self): #submit school info
        self.schoolInfo.withdraw()
        if '.edu' in self.schoolent.get(): #to check whether the email is student or not
            self.studentCheck = '1'
        else:
            self.studentCheck = '0'
        self.Connect()
        cursor = self.db.cursor()
        sql_updateSchool = '''UPDATE Customer SET Is_student = %s WHERE C_Username= %s '''
        cursor.execute(sql_updateSchool,(self.studentCheck,self.userLog))
        self.chofunc.deiconify()




    def viewTrain(self): #View train schedule window
        self.chofunc.withdraw()
        self.trainSch = Toplevel(rootWin)
        self.viewtralab = Label(self.trainSch, text = "View Train Schedule")
        self.viewtralab.grid(row = 1, column = 1, columnspan = 2, sticky = EW)
        self.trainNum = Label(self.trainSch, text = "Train Number")
        self.trainNum.grid(row = 2, column = 1, sticky = E)
        self.trainEnt = Entry(self.trainSch, width = 50)
        self.trainEnt.grid(row = 2, column = 2, sticky = W)
        self.searchBut = Button(self.trainSch, text = "Search", padx = 10, command=self.viewTrain2) #command to view train schedule
        self.searchBut.grid(row = 5, column = 1, sticky = E)
        backchoho = Button(self.trainSch, text = "Back", padx = 10, command=self.backchohofunc)
        backchoho.grid(row = 5, column = 2, sticky = E)

    def backchohofunc(self):
        self.trainSch.withdraw()
        self.chofunc.deiconify()

    def viewTrain2(self):
        self.trainSch.withdraw()
        self.trainSch2 = Toplevel(rootWin)
        self.stationInfo = []
        self.totTrainNum = []
        self.stationInfo1 = []
        self.Connect()
        sql_getTrainSchedule = '''SELECT * FROM TrainStopStation WHERE TrainNumber = %s''' #sql to get train schedule
        sql_getTrainNumber = '''SELECT DISTINCT TrainNumber FROM TrainStopStation''' #to get all train number from database
        cursor1 = self.db.cursor()
        cursor1.execute(sql_getTrainNumber)
        for each in cursor1:
            self.totTrainNum.append(each[0])
        if int(self.trainEnt.get()) not in self.totTrainNum:
            messagebox.showerror("Error", "Train Number does not exist")
            self.trainSch2.withdraw()
            self.viewTrain()

        else:
            cursor = self.db.cursor()
            cursor.execute(sql_getTrainSchedule, (self.trainEnt.get())) #execute sql statement to get all train schedule info

            for each in cursor:
                self.stationInfo.append([each[1],each[2],each[3]]) #contain all info for view train schedule


            viewtralab = Label(self.trainSch2, text = "View Train Schedule")
            viewtralab.grid(row = 1, column = 1, columnspan=8, sticky = EW)
            aList=["Train","Arrival Time", "Departure Time", "Station"]
            for i in range(4):
                Lab=Label(self.trainSch2, text=aList[i])
                Lab.grid(row=2, column=1+i, sticky=W)

            self.trainlablab = Label(self.trainSch2, text = self.trainEnt.get())
            self.trainlablab.grid(row = 3, column = 1, sticky = W)
            for i in range(len(self.stationInfo)):
                stationlab = Label(self.trainSch2, text=self.stationInfo[i][0])
                stationlab.grid(row=3+i, column = 4, sticky=W)
                arrivallab = Label(self.trainSch2, text = self.stationInfo[i][1])
                arrivallab.grid(row=3+i, column = 2, sticky=W)
                departurelab = Label(self.trainSch2, text = self.stationInfo[i][2])
                departurelab.grid(row=3+i, column = 3, sticky=W)

            back = Button(self.trainSch2, text="Back", command=self.backtrainSch)
            back.grid(row=4+len(self.stationInfo), column = 1, sticky = W)

    def backtrainSch(self):
        self.trainSch2.withdraw()
        self.trainSch.deiconify()
        self.trainEnt.delete(0,'end')



    def reservation(self): #Make a reservation window
        self.chofunc.withdraw()
        self.newRev = Toplevel(rootWin)
        self.searchTrain = Label(self.newRev, text = "Search Train")
        self.searchTrain.grid(row = 1, column = 1, columnspan = 2, sticky = EW)
        self.depFrom = Label(self.newRev, text = "Departs From")
        self.depFrom.grid(row = 2, column = 1, sticky = W)
        self.nameLoc = []
        self.Connect()
        self.lst1 = []
        self.lsttemp1 = []
        self.lsttemp2 = []

        cursor = self.db.cursor()
        sql_getStation = '''SELECT Name, Location FROM Station''' #to grab all the departs from and arrives at
        cursor.execute(sql_getStation)
        for each in cursor:
            self.nameLoc.append([each[0],each[1]])
        for i in range(len(self.nameLoc)): #to put row of name location to self.lst1
            self.lsttemp1.append(self.nameLoc[i][0])
            self.lsttemp2.append(self.nameLoc[i][1])
        for i in range(len(self.lsttemp1)):
            self.lst1.append(self.lsttemp1[i] + "("+self.lsttemp2[i] + ")")

        self.var1 = StringVar()
        self.drop1 = OptionMenu(self.newRev, self.var1, *self.lst1)
        self.drop1.grid(row = 2, column = 2, sticky = E)

        self.lst2 = copy.deepcopy(self.lst1)
        self.arrAt = Label(self.newRev, text = "Arrives At")
        self.arrAt.grid(row = 3, column = 1, sticky = W)
        self.var2 = StringVar()
        self.drop2 = OptionMenu(self.newRev, self.var2, *self.lst2)
        self.drop2.grid(row = 3, column = 2, sticky = E)
        self.depDate = Label(self.newRev, text = "Departure Date")
        self.depDate.grid(row = 4, column = 1, sticky = W)
        self.depEntry = Entry(self.newRev)
        self.depEntry.grid(row = 4, column = 2, sticky = W)
        self.depLabel = Label(self.newRev, text = 'YYYY-MM-DD')
        self.depLabel.grid(row = 5, column = 2, sticky = W)
        self.findTrain = Button(self.newRev, text = "Find Trains", command = self.DepFromArr)
        self.findTrain.grid(row = 6, column = 1, sticky = W)

    def DepFromArr(self):
        self.departsneed = self.var1.get()
        a=self.departsneed.find("(")
        self.DepartsStationNam=self.departsneed[:a] #Departs from chosen

        self.Connect()
        cursor = self.db.cursor()
        self.trainDeparts = []
        self.finalSelectDeparts = []
        sql_trainSelect = '''SELECT * FROM TrainStopStation WHERE Name = %s'''
        sql_checkTrain = '''SELECT * FROM TrainStopStation WHERE Name = %s AND TrainNumber = %s'''
        cursor.execute(sql_trainSelect,(self.DepartsStationNam))
        for each in cursor: #train for departs chosen
            self.trainDeparts.append([each[0], each[1], each[2], each[3]]) #departure time
        cursor1 = self.db.cursor()
        self.arrivesneed = self.var2.get()
        b = self.arrivesneed.find("(")
        self.ArrivesStationNam = self.arrivesneed[:b] #arrives at chosen
        cursor1 = self.db.cursor()
        for i in range(len(self.trainDeparts)):

            cursor1.execute(sql_checkTrain,(self.ArrivesStationNam, self.trainDeparts[i][0]))
            for each in cursor1:
                self.finalSelectDeparts.append([each[0], each[1], each[2], each[3]]) #store the same departs from and arrives at but only arrivaltime

        self.selecttimeTrain = []
        for i in range(len(self.finalSelectDeparts)):
            for j in range(len(self.trainDeparts)):
                if self.finalSelectDeparts[i][0] == self.trainDeparts[j][0]:
                    self.selecttimeTrain.append([self.finalSelectDeparts[i][0], self.trainDeparts[j][3], self.finalSelectDeparts[i][2]]) #semi final show on select departure
        sql_price = '''SELECT * FROM TrainRoute'''
        cursor2 = self.db.cursor()
        cursor2.execute(sql_price)
        self.pricenumtrain = []
        for each in cursor2:
            self.pricenumtrain.append([each[0], each[1], each[2]])

        for i in range(len(self.selecttimeTrain)):
            for j in range(len(self.pricenumtrain)):
                if self.selecttimeTrain[i][0] == self.pricenumtrain[j][0]:
                    self.selecttimeTrain[i].append(self.pricenumtrain[j][1])
                    self.selecttimeTrain[i].append(self.pricenumtrain[j][2]) #final show on select departure



        self.depEntrycomp = self.depEntry.get()
        self.depEntrycomp1 = self.depEntrycomp.split('-')
        for i in range(len(self.depEntrycomp1)):
            self.depEntrycomp1[i] = int(self.depEntrycomp1[i])
        self.depEntrycomp2 = datetime.date(self.depEntrycomp1[0], self.depEntrycomp1[1], self.depEntrycomp1[2])
        if self.var1.get() == self.var2.get(): #to check departs from != arrives at
            messagebox.showerror("Error", "Departs From and Arrives At cannot be the same")
        elif self.depEntrycomp2 <= datetime.date.today():
            messagebox.showerror("Error", "Departure Date must be in future")
        elif len(self.selecttimeTrain) == 0:
            messagebox.showerror("Error", "No route exists")
        else:
            self.Select_Departure()
        #self.var1.get() & self.var2.get() & self.depEntry.get() works here!!





    def Select_Departure(self):
        self.newRev.withdraw()
        self.SelectDeparture=Toplevel(rootWin)
        selectDepartureLab=Label(self.SelectDeparture, text="Select Departure")
        selectDepartureLab.grid(row=1, column=1, columnspan=6, sticky=EW)
        aList=["Train Number   ", "Departure Time    ","Arrival Time", "Duration", "1st Class Price    ", "2nd Class Price   ", ]
        for i in range (len(aList)):
            TrainRow=Label(self.SelectDeparture, text=aList[i])
            TrainRow.grid(row=2, column=1+i, sticky=W)
        self.varvar1 = IntVar() #variable that has price selected
        for i in range(len(self.selecttimeTrain)):
            TrainRow=Label(self.SelectDeparture, text=self.selecttimeTrain[i][0]) #0 - > Train Number
            TrainRow.grid(row=3+i, column=1, sticky=W)
            TimeRow=Label(self.SelectDeparture, text=self.selecttimeTrain[i][1]) # 1 -> DepartureTime
            TimeRow.grid(row=3+i, column=2, sticky=W)
            TimeRow2=Label(self.SelectDeparture, text=self.selecttimeTrain[i][2]) # 2 - > Arrival Time
            TimeRow2.grid(row=3+i, column=3, sticky=W)
            firstPrice=Radiobutton(self.SelectDeparture, text=self.selecttimeTrain[i][3],variable=self.varvar1,value=int(self.selecttimeTrain[i][3]))
            firstPrice.grid(row=3+i, column=5, sticky=W)
            secondPrice=Radiobutton(self.SelectDeparture, text=self.selecttimeTrain[i][4], variable = self.varvar1, value = int(self.selecttimeTrain[i][4]))
            secondPrice.grid(row=3+i, column=6, sticky=W)
            Duration=abs((self.selecttimeTrain[i][2]-self.selecttimeTrain[i][1]).total_seconds()/3600)
            DurationHour=abs(int(Duration))
            DurationMinute=abs((int((Duration-DurationHour)*60)))
            DurationLabel=Label(self.SelectDeparture, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
            DurationLabel.grid(row=3+i, column=4,sticky=W)

        Next=Button(self.SelectDeparture,text="Next", command=self.CheckDupTr)
        Next.grid(row=3+len(self.selecttimeTrain), column=4, sticky=E)
        Back=Button(self.SelectDeparture, text="Back", command=self.backback)
        Back.grid(row=3+len(self.selecttimeTrain), column=1, sticky=W)
    def backback(self):
        self.SelectDeparture.withdraw()
        self.newRev.deiconify()

    def CheckDupTr(self):
        for i in range(len(self.selecttimeTrain)):
            if self.varvar1.get() == self.selecttimeTrain[i][3]:
                if self.selecttimeTrain[i][0] not in self.checkDupTrain:
                    self.checkDupTrain.append(self.selecttimeTrain[i][0])
                    self.Travel_Extras()
                elif self.selecttimeTrain[i][0] in self.checkDupTrain:
                    messagebox.showerror("Error","You have already choosen this train number. Please add a different train")
    def Travel_Extras(self):
        self.SelectDeparture.withdraw()
        self.TravelExtras=Toplevel(rootWin)
        self.TravelExtras1=Label(self.TravelExtras, text = "Travel Extras & Passenger Info")
        self.TravelExtras1.grid(row = 1, column = 1, columnspan = 8, sticky = EW)
        self.NumBag=Label(self.TravelExtras, text = "Number of Baggage")
        self.NumBag.grid(row = 2, column = 1, sticky = E)
        self.varvar2 = StringVar()
        self.varvar2.set("0") #initial value
        self.drop2 = OptionMenu(self.TravelExtras, self.varvar2, "0","1","2","3","4")
        self.drop2.grid(row = 2, column = 2, sticky = W)
        self.NumBagLimit=Label(self.TravelExtras, text = "(Every passenger can bring up to 4 baggage. 2 free of charge, 2 for $30 per bag)", width=70)
        self.NumBagLimit.grid(row = 3, column = 1, columnspan = 2, sticky = EW)
        ## we can use self.var2.get() to get the number of baggae to put into the database.
        self.PassengerName=Label(self.TravelExtras, text = "Passenger Name")
        self.PassengerName.grid(row = 4, column = 1, sticky = EW)
        self.PassengerNameEntry=Entry(self.TravelExtras, width=30)
        self.PassengerNameEntry.grid(row = 4, column = 2, sticky = W)
        self.backSelDep = Button(self.TravelExtras, text = "Back", padx = 10, command=self.backbackback) #command to go back to Select Departure custFunc
        self.backSelDep.grid(row = 6, column = 1, sticky = W)
        self.nextMakeRes1 = Button(self.TravelExtras, text = "Next", padx = 10, command=self.Make_Reservation) #command to go to next window twhich is Make Reservation
        self.nextMakeRes1.grid(row = 6, column = 2, sticky = E)

    def backbackback(self):
        self.TravelExtras.withdraw()
        self.SelectDeparture.deiconify()

    def Make_Reservation(self):
        if self.PassengerNameEntry.get() == '':
            messagebox.showerror("Error", "Passenger name field is empty")

        else:
            self.TravelExtras.withdraw()

            self.MakeReservation=Toplevel(rootWin)
            self.MakeReservation1=Label(self.MakeReservation, text = "Make Reservation")
            self.MakeReservation1.grid(row = 1, column = 1, columnspan = 8, sticky = EW)
            currentlySelected=Label(self.MakeReservation, text = "Currently Selected")
            currentlySelected.grid(row = 2, column = 1, sticky = W)

            self.pricefirstsecond = self.varvar1.get()
            aList=["Train Number"," Depart Time ","Arrival Time","Duration", "Depart Date ", " Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "," Remove "]
            for i in range (len(aList)):
                Lab=Label(self.MakeReservation, text=aList[i])
                Lab.grid(row=3, column=1+i, sticky=W)
            self.currentselection.append([self.varvar2.get(),self.PassengerNameEntry.get(),self.var1.get(),self.var2.get(),self.depEntry.get()])
            ##for j in range(self.NumberOfReservation):
            for i in range(len(self.selecttimeTrain)):
                if self.pricefirstsecond == self.selecttimeTrain[i][3]:
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][0])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][1])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][2])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][3])
                    self.currentselection[self.NumberOfReservation-1].append('FirstClass')
                elif self.pricefirstsecond == self.selecttimeTrain[i][4]:
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][0])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][1])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][2])
                    self.currentselection[self.NumberOfReservation-1].append(self.selecttimeTrain[i][4])
                    self.currentselection[self.NumberOfReservation-1].append('SecondClass')


            for  j in range (self.NumberOfReservation):
                for i in range(len(self.currentselection)):
                    self.var6=IntVar() ##to keep track of which resrvation we want to remove.
                    lab=Label(self.MakeReservation, text=self.currentselection[i][5])
                    lab.grid(row=4+i, column=1, sticky=W)
                    lab2=Label(self.MakeReservation, text=self.currentselection[i][6])
                    lab2.grid(row=4+i, column=2, sticky=W)
                    lab3=Label(self.MakeReservation, text=self.currentselection[i][7])
                    lab3.grid(row=4+i, column=3, sticky=W)
                    lab4=Label(self.MakeReservation, text=self.currentselection[i][4])
                    lab4.grid(row=4+i, column=5, sticky=W)
                    lab5=Label(self.MakeReservation, text=self.currentselection[i][2])
                    lab5.grid(row=4+i, column=6, sticky=W)
                    lab6=Label(self.MakeReservation, text=self.currentselection[i][3])
                    lab6.grid(row=4+i, column=7, sticky=W)
                    lab7=Label(self.MakeReservation, text=self.currentselection[i][9])
                    lab7.grid(row=4+i, column=8, sticky=W)
                    lab8=Label(self.MakeReservation, text=self.currentselection[i][8])
                    lab8.grid(row=4+i, column=9, sticky=W)
                    lab9=Label(self.MakeReservation, text=self.currentselection[i][0])
                    lab9.grid(row=4+i, column=10, sticky=W)
                    lab10=Label(self.MakeReservation, text=self.currentselection[i][1])
                    lab10.grid(row=4+i, column=11, sticky=W)
                    lab11=Radiobutton(self.MakeReservation,variable=self.var6,text="Remove", value=int(i))
                    lab11.grid(row=4+i, column=12, sticky=W)
                    Duration=abs((self.currentselection[i][7]-self.currentselection[i][6]).total_seconds()/3600)
                    DurationHour=abs(int(Duration))
                    DurationMinute=abs((int((Duration-DurationHour)*60)))
                    DurationLabel=Label(self.MakeReservation, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
                    DurationLabel.grid(row=4+i, column=4,sticky=W)
            self.Connect()
            sql_getUsernamestatus = '''SELECT Is_student FROM Customer WHERE C_Username = %s'''
            cursor = self.db.cursor()
            cursor.execute(sql_getUsernamestatus, (self.userLog))
            for each in cursor:
                self.tempUser = each[0]

            if self.tempUser == 1: #label for student discount
                stuDisLab=Label(self.MakeReservation, text="Student Discount Applied.")
                stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
            else:
                stuDisLab=Label(self.MakeReservation, text="Student Discount Not Applied.")
                stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
            self.totCostLab=Label(self.MakeReservation, text="Total Cost")
            self.totCostLab.grid(row=6+len(self.currentselection), column=1, sticky=W)
            self.calculation = []
            self.Connect()

            for i in range(self.NumberOfReservation): #price for bag
                #self.calculation.append([self.currentselection[i][3], self.currentselection[i][5]]) #row that contain [price, numbag]
                if int(self.currentselection[i][0]) < 3:
                    pricebag = 0
                    ##self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)
                else:
                    pricebag = (int(self.currentselection[i][0]) - 2) * 30
                    self.priceIndex=i
                self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)

            if self.tempUser == 1:
                self.totalCostCost = self.totalCostCost * 0.8
            self.totalCostCost = "{0:.2f}".format(self.totalCostCost)
            self.totCost=Label(self.MakeReservation, text="$"+str(self.totalCostCost)) #total cost
            self.totCost.grid(row=6+self.NumberOfReservation, column=2, sticky=W)
            self.Connect()
            cursor = self.db.cursor()
            sql_getCard = '''SELECT RIGHT(CardNumber,4),CardNumber FROM PaymentInfo WHERE C_Username = %s'''
            cursor.execute(sql_getCard, (self.userLog))
            self.cardNumnum = []
            self.cardNumberFullDigit=[]
            for each in cursor: #get cardnumber of the user from database
                self.cardNumnum.append(each[0])
                self.cardNumberFullDigit.append(each[1])



            self.var3x = StringVar()
            self.var3x.set(self.cardNumnum[0]) #initial value
            self.useCardLab=OptionMenu(self.MakeReservation, self.var3x, *self.cardNumnum) ## here options are all the cards in the database for that customer, we need to get these from database
            self.useCardLab.grid(row=7+self.NumberOfReservation, column=2, sticky=W)
            useCardLabel=Label(self.MakeReservation, text="Use Card")
            useCardLabel.grid(row=7+self.NumberOfReservation, column=1, sticky=W)
            self.addCard=Button(self.MakeReservation, text="Add Card", command=self.Payment_Information)
            self.addCard.grid(row=7+self.NumberOfReservation, column=3, sticky=W)

            ConAddTrain=Button(self.MakeReservation, text="Continue adding a train", command=self.continueAddTrain)
            ConAddTrain.grid(row=8+self.NumberOfReservation, column=1, sticky=W)
            self.backToTravelExtra = Button(self.MakeReservation, text = "Back", padx = 10, command=self.back10)
            self.backToTravelExtra.grid(row = 9+self.NumberOfReservation, column = 2, sticky = W)
            self.submitMakeRes = Button(self.MakeReservation, text = "Submit", padx = 10, command=self.Confirmation)
            self.submitMakeRes.grid(row=9+self.NumberOfReservation, column = 4, sticky = E)
            self.RemoveSubmit=Button(self.MakeReservation, text="Remove Selected", command=self.RemoveSubmitButton)
            self.RemoveSubmit.grid(row=5+len(self.currentselection), column=11, sticky=E)

    def RemoveSubmitButton(self):
        self.currentselection.remove(self.currentselection[self.var6.get()])
        self.NumberOfReservation=self.NumberOfReservation-1
        self.totalCostCost = 0
        self.MakeReservation.withdraw()
        self.MakeReservation=Toplevel(rootWin)
        aList=["Train Number"," Depart Time ","Arrival Time","Duration", "Depart Date ", " Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "," Remove "]
        for i in range (len(aList)):
            Lab=Label(self.MakeReservation, text=aList[i])
            Lab.grid(row=3, column=1+i, sticky=W)
        for  j in range (self.NumberOfReservation):
            for i in range(len(self.currentselection)):
                self.var6=IntVar() ##to keep track of which resrvation we want to remove.
                lab=Label(self.MakeReservation, text=self.currentselection[i][5])
                lab.grid(row=4+i, column=1, sticky=W)
                lab2=Label(self.MakeReservation, text=self.currentselection[i][6])
                lab2.grid(row=4+i, column=2, sticky=W)
                lab3=Label(self.MakeReservation, text=self.currentselection[i][7])
                lab3.grid(row=4+i, column=3, sticky=W)
                lab4=Label(self.MakeReservation, text=self.currentselection[i][4])
                lab4.grid(row=4+i, column=5, sticky=W)
                lab5=Label(self.MakeReservation, text=self.currentselection[i][2])
                lab5.grid(row=4+i, column=6, sticky=W)
                lab6=Label(self.MakeReservation, text=self.currentselection[i][3])
                lab6.grid(row=4+i, column=7, sticky=W)
                lab7=Label(self.MakeReservation, text=self.currentselection[i][9])
                lab7.grid(row=4+i, column=8, sticky=W)
                lab8=Label(self.MakeReservation, text=self.currentselection[i][8])
                lab8.grid(row=4+i, column=9, sticky=W)
                lab9=Label(self.MakeReservation, text=self.currentselection[i][0])
                lab9.grid(row=4+i, column=10, sticky=W)
                lab10=Label(self.MakeReservation, text=self.currentselection[i][1])
                lab10.grid(row=4+i, column=11, sticky=W)
                lab11=Radiobutton(self.MakeReservation,variable=self.var6,text="Remove", value=int(i))
                lab11.grid(row=4+i, column=12, sticky=W)
                Duration=abs((self.currentselection[i][7]-self.currentselection[i][6]).total_seconds()/3600)
                DurationHour=abs(int(Duration))
                DurationMinute=abs((int((Duration-DurationHour)*60)))
                DurationLabel=Label(self.MakeReservation, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
                DurationLabel.grid(row=4+i, column=4,sticky=W)
        self.Connect()
        sql_getUsernamestatus = '''SELECT Is_student FROM Customer WHERE C_Username = %s'''
        cursor = self.db.cursor()
        cursor.execute(sql_getUsernamestatus, (self.userLog))
        for each in cursor:
            self.tempUser = each[0]

        if self.tempUser == 1: #label for student discount
            stuDisLab=Label(self.MakeReservation, text="Student Discount Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        else:
            stuDisLab=Label(self.MakeReservation, text="Student Discount Not Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        self.totCostLab=Label(self.MakeReservation, text="Total Cost")
        self.totCostLab.grid(row=6+len(self.currentselection), column=1, sticky=W)
        self.calculation = []
        self.Connect()

        for i in range(self.NumberOfReservation): #price for bag
            #self.calculation.append([self.currentselection[i][3], self.currentselection[i][5]]) #row that contain [price, numbag]
            if int(self.currentselection[i][0]) < 3:
                pricebag = 0
                ##self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)
            else:
                pricebag = (int(self.currentselection[i][0]) - 2) * 30
                self.priceIndex=i
            self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)


        if self.tempUser == 1:
            self.totalCostCost = self.totalCostCost * 0.8
        self.totalCostCost = "{0:.2f}".format(self.totalCostCost)
        self.totCost=Label(self.MakeReservation, text="$"+str(self.totalCostCost)) #total cost
        self.totCost.grid(row=6+self.NumberOfReservation, column=2, sticky=W)
        self.Connect()
        cursor = self.db.cursor()
        sql_getCard = '''SELECT RIGHT(CardNumber,4) FROM PaymentInfo WHERE C_Username = %s'''
        cursor.execute(sql_getCard, (self.userLog))
        self.cardNumnum = []
        for each in cursor: #get cardnumber of the user from database
            self.cardNumnum.append(each[0])



        self.var3x = StringVar()
        self.var3x.set(self.cardNumnum[0]) #initial value
        self.useCardLab=OptionMenu(self.MakeReservation, self.var3x, *self.cardNumnum) ## here options are all the cards in the database for that customer, we need to get these from database
        self.useCardLab.grid(row=7+self.NumberOfReservation, column=2, sticky=W)
        useCardLabel=Label(self.MakeReservation, text="Use Card")
        useCardLabel.grid(row=7+self.NumberOfReservation, column=1, sticky=W)
        self.addCard=Button(self.MakeReservation, text="Add Card", command=self.Payment_Information)
        self.addCard.grid(row=7+self.NumberOfReservation, column=3, sticky=W)

        ConAddTrain=Button(self.MakeReservation, text="Continue adding a train", command=self.continueAddTrain)
        ConAddTrain.grid(row=8+self.NumberOfReservation, column=1, sticky=W)
        self.backToTravelExtra = Button(self.MakeReservation, text = "Back", padx = 10, command=self.back10)
        self.backToTravelExtra.grid(row = 9+self.NumberOfReservation, column = 2, sticky = W)
        self.submitMakeRes = Button(self.MakeReservation, text = "Submit", padx = 10, command=self.Confirmation)
        self.submitMakeRes.grid(row=9+self.NumberOfReservation, column = 4, sticky = E)
        self.RemoveSubmit=Button(self.MakeReservation, text="Remove Selected", command=self.RemoveSubmitButton)
        self.RemoveSubmit.grid(row=5+len(self.currentselection), column=11, sticky=E)

    def continueAddTrain(self):
        self.MakeReservation.withdraw()
        self.NumberOfReservation=self.NumberOfReservation+1
        self.totalCostCost= 0
        self.reservation()

    def back10(self):
        self.MakeReservation.withdraw()
        self.custFunc()


    def Payment_Information(self):
        self.MakeReservation.withdraw()
        self.PaymentInformation=Toplevel(rootWin)
        paymentInform=Label(self.PaymentInformation, text="Payment Information")
        paymentInform.grid(row=1, column=1, columnspan = 8, sticky=EW)
        addDelCardList=["Add Card:","Name On Card", "Card Number", "CVV", "Expiration Date", " Delete Card:", "   Card Number"]
        for i in range(7):
            if i==5 or i==6:
                deleteCard=Label(self.PaymentInformation, text=addDelCardList[i])
                deleteCard.grid(row=2+(i-5), column=4, sticky=E)
            else:
                addCard=Label(self.PaymentInformation, text=addDelCardList[i])
                addCard.grid(row=2+i, column=1, sticky=W)
        self.NamOnCardEntry=Entry(self.PaymentInformation, width=30)
        self.NamOnCardEntry.grid(row=3, column=2, sticky=EW)
        self.CardNumberEntry=Entry(self.PaymentInformation, width=30)
        self.CardNumberEntry.grid(row=4, column=2, sticky=EW)
        self.CvvEntry=Entry(self.PaymentInformation, width=10)
        self.CvvEntry.grid(row=5, column=2, sticky=W)
        self.ExpirationDateEntry=Entry(self.PaymentInformation, width=20)
        self.ExpirationDateEntry.grid(row=6, column=2, sticky=W)
        self.ExpDateEntry=Label(self.PaymentInformation, text="YYYY-MM-DD")
        self.ExpDateEntry.grid(row=7, column=2, sticky=W)
        self.var4x = StringVar()
        self.var4x.set(self.cardNumnum[0]) #initial value
        self.delCardNumber=OptionMenu(self.PaymentInformation, self.var4x, *self.cardNumnum)
        self.delCardNumber.grid(row=3, column=5, sticky=EW)
        self.addCardSubmit=Button(self.PaymentInformation, text="Submit", padx=10, command=self.Confirmationadd)
        self.addCardSubmit.grid(row=8, column=1, sticky=W)
        self.delCardSubmit=Button(self.PaymentInformation, text="Submit", padx=10, command=self.Confirmationdel) ##Note: A customer cannot delete a card that is being used in the transaction
        self.delCardSubmit.grid(row=4, column=5, sticky=W)

    def Confirmationdel(self):  ###I fixed everything here except we need to check if the datetime works
        self.Connect()
        cursor = self.db.cursor()
        sql_getResID = '''SELECT ReservationID, RIGHT(CardNumber,4), CardNumber FROM Reservation WHERE C_Username = %s AND Is_cancelled = %s'''
        self.tempResget = []
        cursor.execute(sql_getResID, (self.userLog,'0'))
        for each in cursor:
            self.tempResget.append([each[0], each[1],each[2]])
        cardList=[]
        for i in range (len(self.tempResget)):
            cursor5 = self.db.cursor()
            sql_getResDate='''SELECT DepartureDate FROM ReserveTrain WHERE ReservationID= %s'''
            cursor5.execute(sql_getResDate,(self.tempResget[i][0]))
            for each in cursor5:
                if each[0]>datetime.date.today():
                   cardList.append(self.tempResget[i][1])
        if self.var4x.get() in cardList:
            messagebox.showerror("Error", "You cannot delete this card since it's being used in a transaction.")
            self.PaymentInformation.withdraw()
        else:
            cursor2 = self.db.cursor()
            sql_getCardNumb='''SELECT RIGHT(CardNumber,4), CardNumber FROM PaymentInfo WHERE C_Username = %s '''
            cursor2.execute(sql_getCardNumb,(self.userLog))
            cardNumberList=[]
            cardNumberList2=[]
            for each in cursor2:
                cardNumberList.append(each[0])
                cardNumberList2.append(each[1])
            for i in range (len(cardNumberList)):
                if self.var4x.get()==cardNumberList[i]:
                    self.b=i
            cursor3 = self.db.cursor()
            sql_getDelCard='''DELETE FROM PaymentInfo WHERE CardNumber= %s'''
            cursor3.execute(sql_getDelCard,(cardNumberList2[self.b]))
            try:
                cursor4 = self.db.cursor()
                sql_deleteReserv = '''DELETE FROM Reservation WHERE CardNumber = %s'''
                cursor4.execute(sql_deleteReserv,(cardNumberList2[self.b]))
                messagebox.showinfo("Success", "Your card is deleted successfully.")
                self.PaymentInformation.withdraw()
            except:
                self.PaymentInformation.withdraw()
        self.totalCostCost = 0
        self.MakeReservation.withdraw()
        self.MakeReservation=Toplevel(rootWin)
        aList=["Train Number"," Depart Time ","Arrival Time","Duration", "Depart Date ", " Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "," Remove "]
        for i in range (len(aList)):
            Lab=Label(self.MakeReservation, text=aList[i])
            Lab.grid(row=3, column=1+i, sticky=W)
        for  j in range (self.NumberOfReservation):
            for i in range(len(self.currentselection)):
                self.var6=IntVar() ##to keep track of which resrvation we want to remove.
                lab=Label(self.MakeReservation, text=self.currentselection[i][5])
                lab.grid(row=4+i, column=1, sticky=W)
                lab2=Label(self.MakeReservation, text=self.currentselection[i][6])
                lab2.grid(row=4+i, column=2, sticky=W)
                lab3=Label(self.MakeReservation, text=self.currentselection[i][7])
                lab3.grid(row=4+i, column=3, sticky=W)
                lab4=Label(self.MakeReservation, text=self.currentselection[i][4])
                lab4.grid(row=4+i, column=5, sticky=W)
                lab5=Label(self.MakeReservation, text=self.currentselection[i][2])
                lab5.grid(row=4+i, column=6, sticky=W)
                lab6=Label(self.MakeReservation, text=self.currentselection[i][3])
                lab6.grid(row=4+i, column=7, sticky=W)
                lab7=Label(self.MakeReservation, text=self.currentselection[i][9])
                lab7.grid(row=4+i, column=8, sticky=W)
                lab8=Label(self.MakeReservation, text=self.currentselection[i][8])
                lab8.grid(row=4+i, column=9, sticky=W)
                lab9=Label(self.MakeReservation, text=self.currentselection[i][0])
                lab9.grid(row=4+i, column=10, sticky=W)
                lab10=Label(self.MakeReservation, text=self.currentselection[i][1])
                lab10.grid(row=4+i, column=11, sticky=W)
                lab11=Radiobutton(self.MakeReservation,variable=self.var6,text="Remove", value=int(i))
                lab11.grid(row=4+i, column=12, sticky=W)
                Duration=abs((self.currentselection[i][7]-self.currentselection[i][6]).total_seconds()/3600)
                DurationHour=abs(int(Duration))
                DurationMinute=abs((int((Duration-DurationHour)*60)))
                DurationLabel=Label(self.MakeReservation, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
                DurationLabel.grid(row=4+i, column=4,sticky=W)
        self.Connect()
        sql_getUsernamestatus = '''SELECT Is_student FROM Customer WHERE C_Username = %s'''
        cursor = self.db.cursor()
        cursor.execute(sql_getUsernamestatus, (self.userLog))
        for each in cursor:
            self.tempUser = each[0]

        if self.tempUser == 1: #label for student discount
            stuDisLab=Label(self.MakeReservation, text="Student Discount Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        else:
            stuDisLab=Label(self.MakeReservation, text="Student Discount Not Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        self.totCostLab=Label(self.MakeReservation, text="Total Cost")
        self.totCostLab.grid(row=6+len(self.currentselection), column=1, sticky=W)
        self.calculation = []
        self.Connect()

        for i in range(self.NumberOfReservation): #price for bag
            #self.calculation.append([self.currentselection[i][3], self.currentselection[i][5]]) #row that contain [price, numbag]
            if int(self.currentselection[i][0]) < 3:
                pricebag = 0
                ##self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)
            else:
                pricebag = (int(self.currentselection[i][0]) - 2) * 30
                self.priceIndex=i
            self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)


        if self.tempUser == 1:
            self.totalCostCost = self.totalCostCost * 0.8
        self.totalCostCost = "{0:.2f}".format(self.totalCostCost)
        self.totCost=Label(self.MakeReservation, text="$"+str(self.totalCostCost)) #total cost
        self.totCost.grid(row=6+self.NumberOfReservation, column=2, sticky=W)
        self.Connect()
        cursor = self.db.cursor()
        sql_getCard = '''SELECT RIGHT(CardNumber,4) FROM PaymentInfo WHERE C_Username = %s'''
        cursor.execute(sql_getCard, (self.userLog))
        self.cardNumnum = []
        for each in cursor: #get cardnumber of the user from database
            self.cardNumnum.append(each[0])



        self.var3x = StringVar()
        self.var3x.set(self.cardNumnum[0]) #initial value
        self.useCardLab=OptionMenu(self.MakeReservation, self.var3x, *self.cardNumnum) ## here options are all the cards in the database for that customer, we need to get these from database
        self.useCardLab.grid(row=7+self.NumberOfReservation, column=2, sticky=W)
        useCardLabel=Label(self.MakeReservation, text="Use Card")
        useCardLabel.grid(row=7+self.NumberOfReservation, column=1, sticky=W)
        self.addCard=Button(self.MakeReservation, text="Add Card", command=self.Payment_Information)
        self.addCard.grid(row=7+self.NumberOfReservation, column=3, sticky=W)

        ConAddTrain=Button(self.MakeReservation, text="Continue adding a train", command=self.continueAddTrain)
        ConAddTrain.grid(row=8+self.NumberOfReservation, column=1, sticky=W)
        self.backToTravelExtra = Button(self.MakeReservation, text = "Back", padx = 10, command=self.back10)
        self.backToTravelExtra.grid(row = 9+self.NumberOfReservation, column = 2, sticky = W)
        self.submitMakeRes = Button(self.MakeReservation, text = "Submit", padx = 10, command=self.Confirmation)
        self.submitMakeRes.grid(row=9+self.NumberOfReservation, column = 4, sticky = E)
        self.RemoveSubmit=Button(self.MakeReservation, text="Remove Selected", command=self.RemoveSubmitButton)
        self.RemoveSubmit.grid(row=5+len(self.currentselection), column=11, sticky=E)



    def Confirmationadd(self):
        self.Connect()
        sql_getcard = '''SELECT CardNumber FROM PaymentInfo'''

        cursor = self.db.cursor()
        cursor.execute(sql_getcard)
        cursorNum = self.db.cursor()
        cardList = []
        for each in cursor:
            cardList.append(each[0])

        if self.CardNumberEntry.get() in cardList:
            messagebox.showerror("Fail", "Card number exists on database")
            self.PaymentInformation.withdraw()
            self.Payment_Information()

        elif datetime.datetime.strptime(str(self.ExpirationDateEntry.get()), "%Y-%m-%d") < datetime.datetime.now():
            messagebox.showerror("Fail", "Expiration date of the card has passed")
            self.PaymentInformation.withdraw()
            self.Payment_Information()
        else:

            sql_addcardcardcard = '''INSERT INTO PaymentInfo(`CardNumber`,`CVV`,`ExpDate`,`NameOnCard`,`C_Username`) VALUES(%s, %s, %s, %s, %s)'''
            cursorNum.execute(sql_addcardcardcard, (self.CardNumberEntry.get(), self.CvvEntry.get(), self.ExpirationDateEntry.get(), self.NamOnCardEntry.get(),self.userLog))
            messagebox.showinfo("Success", "Card added successfully")
            self.PaymentInformation.withdraw()
            self.GoBackToMakeReservation10()

    def  GoBackToMakeReservation10(self):
        self.totalCostCost = 0
        self.MakeReservation.withdraw()
        self.MakeReservation=Toplevel(rootWin)
        aList=["Train Number"," Depart Time ","Arrival Time","Duration", "Depart Date ", " Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "," Remove "]
        for i in range (len(aList)):
            Lab=Label(self.MakeReservation, text=aList[i])
            Lab.grid(row=3, column=1+i, sticky=W)
        for  j in range (self.NumberOfReservation):
            for i in range(len(self.currentselection)):
                self.var6=IntVar() ##to keep track of which resrvation we want to remove.
                lab=Label(self.MakeReservation, text=self.currentselection[i][5])
                lab.grid(row=4+i, column=1, sticky=W)
                lab2=Label(self.MakeReservation, text=self.currentselection[i][6])
                lab2.grid(row=4+i, column=2, sticky=W)
                lab3=Label(self.MakeReservation, text=self.currentselection[i][7])
                lab3.grid(row=4+i, column=3, sticky=W)
                lab4=Label(self.MakeReservation, text=self.currentselection[i][4])
                lab4.grid(row=4+i, column=5, sticky=W)
                lab5=Label(self.MakeReservation, text=self.currentselection[i][2])
                lab5.grid(row=4+i, column=6, sticky=W)
                lab6=Label(self.MakeReservation, text=self.currentselection[i][3])
                lab6.grid(row=4+i, column=7, sticky=W)
                lab7=Label(self.MakeReservation, text=self.currentselection[i][9])
                lab7.grid(row=4+i, column=8, sticky=W)
                lab8=Label(self.MakeReservation, text=self.currentselection[i][8])
                lab8.grid(row=4+i, column=9, sticky=W)
                lab9=Label(self.MakeReservation, text=self.currentselection[i][0])
                lab9.grid(row=4+i, column=10, sticky=W)
                lab10=Label(self.MakeReservation, text=self.currentselection[i][1])
                lab10.grid(row=4+i, column=11, sticky=W)
                lab11=Radiobutton(self.MakeReservation,variable=self.var6,text="Remove", value=int(i))
                lab11.grid(row=4+i, column=12, sticky=W)
                Duration=abs((self.currentselection[i][7]-self.currentselection[i][6]).total_seconds()/3600)
                DurationHour=abs(int(Duration))
                DurationMinute=abs((int((Duration-DurationHour)*60)))
                DurationLabel=Label(self.MakeReservation, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
                DurationLabel.grid(row=4+i, column=4,sticky=W)
        self.Connect()
        sql_getUsernamestatus = '''SELECT Is_student FROM Customer WHERE C_Username = %s'''
        cursor = self.db.cursor()
        cursor.execute(sql_getUsernamestatus, (self.userLog))
        for each in cursor:
            self.tempUser = each[0]

        if self.tempUser == 1: #label for student discount
            stuDisLab=Label(self.MakeReservation, text="Student Discount Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        else:
            stuDisLab=Label(self.MakeReservation, text="Student Discount Not Applied.")
            stuDisLab.grid(row=5+len(self.currentselection), column=1, sticky=EW)
        self.totCostLab=Label(self.MakeReservation, text="Total Cost")
        self.totCostLab.grid(row=6+len(self.currentselection), column=1, sticky=W)
        self.calculation = []
        self.Connect()

        for i in range(self.NumberOfReservation): #price for bag
            #self.calculation.append([self.currentselection[i][3], self.currentselection[i][5]]) #row that contain [price, numbag]
            if int(self.currentselection[i][0]) < 3:
                pricebag = 0
                ##self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)
            else:
                pricebag = (int(self.currentselection[i][0]) - 2) * 30
                self.priceIndex=i
            self.totalCostCost=float(self.totalCostCost)+float(self.currentselection[i][8])+float(pricebag)


        if self.tempUser == 1:
            self.totalCostCost = self.totalCostCost * 0.8
        self.totalCostCost = "{0:.2f}".format(self.totalCostCost)
        self.totCost=Label(self.MakeReservation, text="$"+str(self.totalCostCost)) #total cost
        self.totCost.grid(row=6+self.NumberOfReservation, column=2, sticky=W)
        self.Connect()
        cursor = self.db.cursor()
        sql_getCard = '''SELECT RIGHT(CardNumber,4) FROM PaymentInfo WHERE C_Username = %s'''
        cursor.execute(sql_getCard, (self.userLog))
        self.cardNumnum = []
        for each in cursor: #get cardnumber of the user from database
            self.cardNumnum.append(each[0])



        self.var3x = StringVar()
        self.var3x.set(self.cardNumnum[0]) #initial value
        self.useCardLab=OptionMenu(self.MakeReservation, self.var3x, *self.cardNumnum) ## here options are all the cards in the database for that customer, we need to get these from database
        self.useCardLab.grid(row=7+self.NumberOfReservation, column=2, sticky=W)
        useCardLabel=Label(self.MakeReservation, text="Use Card")
        useCardLabel.grid(row=7+self.NumberOfReservation, column=1, sticky=W)
        self.addCard=Button(self.MakeReservation, text="Add Card", command=self.Payment_Information)
        self.addCard.grid(row=7+self.NumberOfReservation, column=3, sticky=W)

        ConAddTrain=Button(self.MakeReservation, text="Continue adding a train", command=self.continueAddTrain)
        ConAddTrain.grid(row=8+self.NumberOfReservation, column=1, sticky=W)
        self.backToTravelExtra = Button(self.MakeReservation, text = "Back", padx = 10, command=self.back10)
        self.backToTravelExtra.grid(row = 9+self.NumberOfReservation, column = 2, sticky = W)
        self.submitMakeRes = Button(self.MakeReservation, text = "Submit", padx = 10, command=self.Confirmation)
        self.submitMakeRes.grid(row=9+self.NumberOfReservation, column = 4, sticky = E)
        self.RemoveSubmit=Button(self.MakeReservation, text="Remove Selected", command=self.RemoveSubmitButton)
        self.RemoveSubmit.grid(row=5+len(self.currentselection), column=11, sticky=E)

    def Confirmation(self):

        self.ReservationIdList=[]
        for i in range (len(self.cardNumberFullDigit)):
            if str(self.var3x.get()) in (str(self.cardNumberFullDigit[i])[4:]):
                self.cardNumberFullDigit2=self.cardNumberFullDigit[i]
        self.Connect()
        cursor6=self.db.cursor()
        sql_getMaxReservationID='''SELECT ReservationID FROM Reservation'''
        cursor6.execute(sql_getMaxReservationID)
        self.ReservationIdList10=[]
        for each in cursor6:
            self.ReservationIdList.append(int(each[0]))
        self.ReservationID=max(self.ReservationIdList)

        self.ReservationIdList10.append(self.ReservationID+1+i)
        self.Connect()
        cursor3=self.db.cursor()
        sql_PutIntoReservation='''INSERT INTO Reservation(ReservationID,CardNumber, C_Username, Is_cancelled, Total) VALUES(%s,%s,%s,%s,%s)'''
        cursor3.execute(sql_PutIntoReservation,(str(self.ReservationID+1),str(self.cardNumberFullDigit2), self.userLog, "0", str(self.totalCostCost)))
        for i in range (len(self.currentselection)):
            DepartsFromIndex=self.currentselection[i][2].find("(")
            DepartsFrom=self.currentselection[i][2][:DepartsFromIndex]
            ArrivesAtIndex=self.currentselection[i][3].find("(")
            ArrivesAt=self.currentselection[i][3][:ArrivesAtIndex]
            sql_PutIntoReserveTrain='''INSERT INTO ReserveTrain(ReservationID, TrainNumber,Class,DepartureDate, PassengerName, NumBags, DepartsFrom, ArrivesAt, Price, Is_cancelled) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor=self.db.cursor()
            cursor.execute(sql_PutIntoReserveTrain,(str(self.ReservationID+1),str(self.currentselection[i][5]), self.currentselection[i][9], self.currentselection[i][4], self.currentselection[i][1],
                                                    str(self.currentselection[i][0]),DepartsFrom, ArrivesAt, str(self.currentselection[i][8]),"0"))

        self.MakeReservation.withdraw()
        self.Confirm=Toplevel(rootWin)
        conLabel=Label(self.Confirm, text="Confirmation")
        conLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)
        ReseIdLab=Label(self.Confirm, text="Reservation ID   "+str(self.ReservationID+1))
        ReseIdLab.grid(row=2, column=1, sticky=W)
        thankLab=Label(self.Confirm, text="Thank you for your purchase. Please save Reservation ID for your Records.", width=55)
        thankLab.grid(row=3, column=1, sticky=W)
        GoBackToChoFunc=Button(self.Confirm, text="Go Back to choose functionality", width=25, command=self.back101)
        GoBackToChoFunc.grid(row=4, column=1, sticky=W)

    def back101(self):
        self.Confirm.withdraw()
        self.currentselection = []
        self.NumberOfReservation = 1
        self.totalCostCost = 0
        self.custFunc()
    def UpdateReservation(self):
        self.chofunc.withdraw()
        self.UpReservation=Toplevel(rootWin)
        UpdateLabel=Label(self.UpReservation, text="Update Reservation")
        UpdateLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)
        ReseIdLab=Label(self.UpReservation, text="Reservation ID    ")
        ReseIdLab.grid(row=2, column=1, sticky=W)
        self.ReservationIdEntry=Entry(self.UpReservation, width=15)
        self.ReservationIdEntry.grid(row=2, column=2, sticky=EW)
        self.ResIdSearch=Button(self.UpReservation,text="Search", command=self.UpdateReservation2)
        self.ResIdSearch.grid(row=2, column=3, sticky=EW)
        GoBackToChoFunc=Button(self.UpReservation, text="Back", width=10, command=self.updaterevback)
        GoBackToChoFunc.grid(row=4, column=1, sticky=W)
    def updaterevback(self): #back menu functionality for update reservation
        self.UpReservation.withdraw()
        self.chofunc.deiconify()
    def UpdateReservation2(self):
        self.UpReservation.withdraw()
        self.UpReservation2=Toplevel(rootWin)
        ##Note:Error message should pop up if we cant find the reservation ID or it wasn't made by that customer
        self.Connect()
        sql_reservationID = '''SELECT ReservationID FROM Reservation WHERE C_Username = %s'''
        res_idget = []
        cursor = self.db.cursor()
        cursor.execute(sql_reservationID, self.userLog)
        for each in cursor:
            res_idget.append(each[0])
        for i in range(len(res_idget)):
            res_idget[i] = str(res_idget[i])
        sql_allreserv = '''SELECT ReservationID FROM ReserveTrain'''
        cursor1 = self.db.cursor()
        cursor1.execute(sql_allreserv)
        allrevid = []
        for each in cursor1:
            allrevid.append(each[0])
        for i in range(len(allrevid)):
            allrevid[i] = str(allrevid[i])
        if str(self.ReservationIdEntry.get()) not in res_idget or str(self.ReservationIdEntry.get()) not in allrevid:
            self.UpReservation2.withdraw()
            messagebox.showerror("Error", "Reservation ID cannot be found or not made by the customer")

            self.UpdateReservation()

        else:

            UpdateLabel=Label(self.UpReservation2, text="Update Reservation")

            self.Connect()
            self.getlist = []
            sql_getinfoinfo = '''SELECT ReserveTrain.TrainNumber, ReserveTrain.DepartureDate, ReserveTrain.DepartsFrom, ReserveTrain.ArrivesAt, ReserveTrain.Class, ReserveTrain.NumBags, ReserveTrain.PassengerName  FROM ReserveTrain INNER JOIN Reservation ON Reservation.ReservationID = ReserveTrain.ReservationID WHERE Reservation.ReservationID = %s'''
            cursor = self.db.cursor()
            cursor.execute(sql_getinfoinfo, self.ReservationIdEntry.get())
            cursor1 = self.db.cursor()
            sql_getPriceprice = '''SELECT FirstClassPrice, SecondClassPrice FROM TrainRoute WHERE TrainNumber = %s'''
            cursor2 = self.db.cursor()
            sql_getArrDep = '''SELECT ArrivalTime, DepartureTime FROM TrainStopStation WHERE TrainNumber = %s AND Name = %s'''
            pricelist1 = []
            getlist1 = []
            getprice1 = []
            getlist2 = []
            for each in cursor:
                self.getlist.append([each[0],each[1],each[2],each[3],each[4],each[5],each[6]]) #[TrainNumber, DepartureDate, DepartsFrom, ArrivesAt, Class, NumBags, PassengerName]

                cursor1.execute(sql_getPriceprice, each[0])
                for eacheach in cursor1:
                    getlist1.append([eacheach[0], eacheach[1]]) #FirstClassPrice, SecondClassPrice
            for i in range(len(self.getlist)):
                self.Connect()
                cursor2.execute(sql_getArrDep, (str(self.getlist[i][0]), self.getlist[i][2]))
                for eacheacheach in cursor2:

                    getlist2.append([eacheacheach[0], eacheacheach[1]]) #ArrivalTime, DepartureTime
            for i in range(len(self.getlist)):
                if self.getlist[i][4] == "FirstClass":
                    getprice1.append(getlist1[i][0])
                elif self.getlist[i][4] == "SecondClass":
                    getprice1.append(getlist1[i][1])

            for i in range(len(self.getlist)):
                self.getlist[i].append(getlist2[i][0])
                self.getlist[i].append(getlist2[i][1])
                self.getlist[i].append(getprice1[i]) #TrainNumber, DepartureDate, DepartsFrom, ArrivesAt, Class, NumBags, PassengerName,  ArrivalTime, DepartureTime, Price

            UpdateLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)

            titleList=["Select", "Train ","Departure Time", "Arrival Time","Duration","Departure Date"," Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "]
            for i in range(len(titleList)):
                title=Label(self.UpReservation2, text=titleList[i])
                title.grid(row=2, column=i+1, sticky=EW)

            self.varxD = IntVar()
            for i in range(len(self.getlist)):
                radioselect = Radiobutton(self.UpReservation2, variable = self.varxD, value = int(i))
                radioselect.grid(row=3+i, column = 1, sticky=W)
                trainxD = Label(self.UpReservation2, text= str(self.getlist[i][0]))
                trainxD.grid(row=3+i, column = 2, sticky=W)
                departxD = Label(self.UpReservation2, text= str(self.getlist[i][8]))
                departxD.grid(row=3+i, column = 3, sticky=W)
                arrivalxD = Label(self.UpReservation2, text= str(self.getlist[i][7]))
                arrivalxD.grid(row=3+i, column = 4, sticky=W)
                depdatexD = Label(self.UpReservation2, text= str(self.getlist[i][1]))
                depdatexD.grid(row=3+i, column = 6, sticky=W)
                departfrxD = Label(self.UpReservation2, text= str(self.getlist[i][2]))
                departfrxD.grid(row=3+i, column = 7, sticky=W)
                arrivesatxD = Label(self.UpReservation2, text= str(self.getlist[i][3]))
                arrivesatxD.grid(row=3+i, column = 8, sticky=W)
                classxD = Label(self.UpReservation2, text= str(self.getlist[i][4]))
                classxD.grid(row=3+i, column = 9, sticky=W)
                pricexD = Label(self.UpReservation2, text= str(self.getlist[i][9]))
                pricexD.grid(row=3+i, column = 10, sticky=W)
                numbagxD = Label(self.UpReservation2, text= str(self.getlist[i][5]))
                numbagxD.grid(row=3+i, column = 11, sticky=EW)
                passnamexD = Label(self.UpReservation2, text= str(self.getlist[i][6]))
                passnamexD.grid(row=3+i, column = 12, sticky=W)
                Duration=abs((self.getlist[i][7]-self.getlist[i][8]).total_seconds()/3600)
                DurationHour=abs(int(Duration))
                DurationMinute=abs((int((Duration-DurationHour)*60)))
                DurationLabel=Label(self.UpReservation2, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
                DurationLabel.grid(row=3+i, column=5,sticky=W)
            Next=Button(self.UpReservation2,text="Next", command=self.DepartDateCheck)
            Next.grid(row=4+len(self.getlist), column=3, sticky=E)
            Back=Button(self.UpReservation2, text="Back", command=self.backupdaterev)
            Back.grid(row=4+len(self.getlist), column=1, sticky=W)
    def backupdaterev(self):
        self.UpReservation2.withdraw()
        self.UpdateReservation()
    def DepartDateCheck(self):  ##checing whether you are allowed to update the reservation now since rervation update cant be made one day earlier than departure date.
        if int((self.getlist[self.varxD.get()][1]-datetime.date.today()).days)<2:
            messagebox.showerror("Error","An Update Should be made One day Earlier than the departure date.")
        elif int((self.getlist[self.varxD.get()][1]-datetime.date.today()).days)>1:
            self.UpdateReservation3()

    def UpdateReservation3(self):
        self.UpReservation2.withdraw()
        self.UpdateRe3 = Toplevel(rootWin)
        self.updatesel=self.varxD.get()
        UpdateLabel=Label(self.UpdateRe3, text="Update Reservation")
        UpdateLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)
        CurrentTic=Label(self.UpdateRe3, text="Current Train Ticket")
        CurrentTic.grid(row=2, column=1, sticky=W)
        titleList=["Train ","Departure Time","Arrival Time", "Duration","Departure Date"," Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "]
        for i in range(len(titleList)):
            title=Label(self.UpdateRe3, text=titleList[i])
            title.grid(row=3, column=i+1, sticky=EW)
        train1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][0]))
        train1xS.grid(row=4, column = 1, sticky=EW)
        depart1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][8]))
        depart1xS.grid(row=4, column = 2, sticky=EW)
        arrival1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][7]))
        arrival1xS.grid(row=4, column = 3, sticky=EW)
        depdate1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][1]))
        depdate1xS.grid(row=4, column = 5, sticky=EW)
        departfr1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][2]))
        departfr1xS.grid(row=4, column = 6, sticky=EW)
        arrivesat1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][3]))
        arrivesat1xS.grid(row=4, column = 7, sticky=EW)
        class1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][4]))
        class1xS.grid(row=4, column = 8, sticky=EW)
        price1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][9]))
        price1xS.grid(row=4, column = 9, sticky=EW)
        numbag1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][5]))
        numbag1xS.grid(row=4, column = 10, sticky=EW)
        passname1xS = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][6]))
        passname1xS.grid(row=4, column = 11, sticky=EW)
        Duration=abs((self.getlist[0][7]-self.getlist[0][8]).total_seconds()/3600)
        DurationHour=abs(int(Duration))
        DurationMinute=abs((int((Duration-DurationHour)*60)))
        DurationLabel=Label(self.UpdateRe3, text=str(DurationHour)+"hr"+str(DurationMinute)+"min")
        DurationLabel.grid(row=4, column=4,sticky=W)

        NewDepDatLab=Label(self.UpdateRe3, text="New Departure Date")
        NewDepDatLab.grid(row=5, column=1, sticky=W)
        self.NewDepDat=Entry(self.UpdateRe3, width=15)
        self.NewDepDat.grid(row=5, column=2, sticky=W)
        datedateput = Label(self.UpdateRe3, text = "YYYY-MM-DD")
        datedateput.grid(row=6, column = 2, sticky=W)
        self.searchAvail=Button(self.UpdateRe3, text="Search Availability", command=self.SearchAvailability)
        self.searchAvail.grid(row=5, column=3, sticky=E)


    def SearchAvailability(self):
        self.comparedep = self.NewDepDat.get()
        self.comparedep1 = self.comparedep.split('-')
        for i in range(len(self.comparedep1)):
            self.comparedep1[i] = int(self.comparedep1[i])
        self.comparedep2 = datetime.date(self.comparedep1[0], self.comparedep1[1], self.comparedep1[2]) #change to date XXXX-YY-ZZ
        if self.comparedep2 > datetime.date.today():
            updatetrainxD1 = Label(self.UpdateRe3, text = "Updated Train Ticket")
            updatetrainxD1.grid(row=7, column = 1, sticky =W)
            titleList=["Train ","Departure Time","Arrival Time", "Duration","Departure Date"," Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "]
            for i in range(len(titleList)):
                title1=Label(self.UpdateRe3, text=titleList[i])
                title1.grid(row=8, column=i+1, sticky=EW)
            train1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][0]))
            train1xS1.grid(row=9, column = 1, sticky=EW)
            depart1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][8]))
            depart1xS1.grid(row=9, column = 2, sticky=EW)
            arrival1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][7]))
            arrival1xS1.grid(row=9, column = 3, sticky=EW)
            depdate1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][1]))
            depdate1xS1.grid(row=9, column = 5, sticky=EW)
            departfr1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][2]))
            departfr1xS1.grid(row=9, column = 6, sticky=EW)
            arrivesat1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][3]))
            arrivesat1xS1.grid(row=9, column = 7, sticky=EW)
            class1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][4]))
            class1xS1.grid(row=9, column = 8, sticky=EW)
            price1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][9]))
            price1xS1.grid(row=9, column = 9, sticky=EW)
            numbag1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][5]))
            numbag1xS1.grid(row=9, column = 10, sticky=EW)
            passname1xS1 = Label(self.UpdateRe3, text= str(self.getlist[self.updatesel][6]))
            passname1xS1.grid(row=9, column = 11, sticky=EW)
            Duration1=abs((self.getlist[0][7]-self.getlist[0][8]).total_seconds()/3600)
            DurationHour1=abs(int(Duration1))
            DurationMinute1=abs((int((Duration1-DurationHour1)*60)))
            DurationLabel1=Label(self.UpdateRe3, text=str(DurationHour1)+"hr"+str(DurationMinute1)+"min")
            DurationLabel1.grid(row=9, column=4,sticky=W)
            changeFeeLabel1=Label(self.UpdateRe3, text="Change Fee       $50")
            changeFeeLabel1.grid(row=10,column=1,sticky=W)
            self.Connect()
            cursor21=self.db.cursor()
            sql_getPrice='''SELECT Total FROM Reservation WHERE ReservationID=%s'''
            cursor21.execute(sql_getPrice,(self.ReservationIdEntry.get()))
            for each in cursor21:
                self.UpdatedTotalCost=float(each[0])
            self.UpdatedTotalCost=self.UpdatedTotalCost+50
            UpTotCostLab=Label(self.UpdateRe3, text="Updated Total Cost     $ "+str(self.UpdatedTotalCost))
            UpTotCostLab.grid(row=11,column=1,sticky=W)
            self.backxD = Button(self.UpdateRe3, text = "Back",command=self.back24)
            self.backxD.grid(row = 12, column = 1, sticky = W)
            self.submitxD = Button(self.UpdateRe3, text = "Submit", command=self.UpResSubmit)
            self.submitxD.grid(row = 12, column = 3, sticky = W)
        else:
            messagebox.showerror("Error", "This date has been passed, Choose a date in the future.")
            self.UpdateRe3.withdraw()
            self.UpdateReservation3()


    def back24(self):
        self.UpdateRe3.withdraw()
        self.UpReservation2.deiconify()

    def UpResSubmit(self):
##        print(str(self.UpdatedTotalCost),self.NewDepDat.get(),str(self.ReservationIdEntry.get()))
        self.Connect()
        cursor=self.db.cursor()
        sql_depDateUpdate='''UPDATE ReserveTrain SET DepartureDate=%s WHERE ReservationID=%s AND TrainNumber=%s AND DepartureDate=%s AND Class=%s AND PassengerName=%s AND DepartsFrom=%s AND ArrivesAt=%s '''
        cursor.execute(sql_depDateUpdate,(str(self.NewDepDat.get()),str(self.ReservationIdEntry.get()), str(self.getlist[self.varxD.get()][0]),str(self.getlist[self.varxD.get()][1]),str(self.getlist[self.varxD.get()][4]),str(self.getlist[self.varxD.get()][6]),
                                          str(self.getlist[self.varxD.get()][2]), str(self.getlist[self.varxD.get()][3])))

        self.Connect()
        cursor2=self.db.cursor()
        sql_TotalCostUpdate='''UPDATE Reservation SET Total=%s WHERE ReservationID=%s'''
        cursor2.execute(sql_TotalCostUpdate,(str(self.UpdatedTotalCost),str(self.ReservationIdEntry.get())))
        messagebox.showinfo("Success","Reservation was updated successfully")
        self.UpdateRe3.withdraw()
        self.custFunc()
    def CancelReservation(self):
        self.chofunc.withdraw()
        self.CaRev = Toplevel(rootWin)
        CanLabel=Label(self.CaRev, text="Cancel Reservation")
        CanLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)
        ReseIdLab=Label(self.CaRev, text="Reservation ID    ")
        ReseIdLab.grid(row=2, column=1, sticky=W)
        self.CanReservationIdEntry=Entry(self.CaRev, width=15)
        self.CanReservationIdEntry.grid(row=2, column=2, sticky=EW)
        self.CanResIdSearch=Button(self.CaRev,text="Search", command=self.CancelReservationSearch)
        self.CanResIdSearch.grid(row=2, column=3, sticky=EW)
        GoBackToChoFunc=Button(self.CaRev, text="Back", width=10, command=self.back12)
        GoBackToChoFunc.grid(row=4, column=1, sticky=W)

    def back12(self):
        self.CaRev.withdraw()
        self.custFunc()

    def CancelReservationSearch(self):
        self.CancelReservationId=self.CanReservationIdEntry.get()
        self.Connect()
        cursor=self.db.cursor()
        sql_getFromReserveTrain='''SELECT ReservationID FROM ReserveTrain'''
        cursor.execute(sql_getFromReserveTrain)
        cancelReservationList=[]
        for each in cursor:
            cancelReservationList.append(int(each[0]))
        if int(self.CanReservationIdEntry.get()) not in cancelReservationList:
            messagebox.showerror("Error","Reservation ID does not exist")
        elif int(self.CanReservationIdEntry.get()) in cancelReservationList:
            self.CancelReservation2()

    def CancelReservation2(self):
        self.CaRev.withdraw()
        self.CanReservation2 = Toplevel(rootWin)
        CanLabel=Label(self.CanReservation2, text="Cancel Reservation")
        CanLabel.grid(row=1, column=1, columnspan = 8, sticky=EW)
        titleList=["Train Number"," Depart Time ","Arrival Time ","Duration","Departure Date "," Departs From "," Arrives at "," Class "," Price "," #of Baggage "," Passenger Name "]
        for i in range(len(titleList)):
            title=Label(self.CanReservation2, text=titleList[i])
            title.grid(row=2, column=i+1, sticky=EW)
        self.CancelReservationId=self.CanReservationIdEntry.get()
        self.Connect()
        cursor=self.db.cursor()
        sql_getFromReserveTrain='''SELECT * FROM ReserveTrain WHERE ReservationID=%s'''
        cursor.execute(sql_getFromReserveTrain,(self.CancelReservationId))
        cancelReservationList=[]
        for each in cursor:
            cancelReservationList.append([each[1],each[2],each[3],each[4],each[5],each[6],each[7]])
        for i in range(len(cancelReservationList)):
            self.Connect()
            cursor2=self.db.cursor()
            if cancelReservationList[i][1]=="FirstClass":
                sql_getPrice='''SELECT FirstClassPrice FROM TrainRoute WHERE TrainNumber=%s'''
                cursor2.execute(sql_getPrice,(cancelReservationList[i][0]))
                for each in cursor2:
                    cancelReservationList[i].append(each[0])
            elif cancelReservationList[i][1]=="SecondClass":
                sql_getPrice='''SELECT SecondClassPrice FROM TrainRoute WHERE TrainNumber=%s'''
                cursor2.execute(sql_getPrice,(cancelReservationList[i][0]))
                for each in cursor2:
                    cancelReservationList[i].append(each[0])
            self.Connect()
            cursor3=self.db.cursor()
            sql_getArrivalDeparture='''SELECT DepartureTime FROM TrainStopStation WHERE TrainNumber=%s AND Name=%s'''
            cursor3.execute(sql_getArrivalDeparture,(cancelReservationList[i][0],cancelReservationList[i][5]))
            for each in cursor3:
                cancelReservationList[i].append(each[0])

            self.Connect()
            cursor4=self.db.cursor()
            sql_getArrivalDeparture='''SELECT DepartureTime FROM TrainStopStation WHERE TrainNumber=%s AND Name=%s'''
            cursor4.execute(sql_getArrivalDeparture,(cancelReservationList[i][0],cancelReservationList[i][6]))
            for each in cursor4:
                cancelReservationList[i].append(each[0])


        for i in range (len(cancelReservationList)):
            trainNumber=Label(self.CanReservation2, text=cancelReservationList[i][0])
            trainNumber.grid(row=3+i, column=1, sticky=EW)
            departTime=Label(self.CanReservation2, text=cancelReservationList[i][8])
            departTime.grid(row=3+i, column=2, sticky=EW)
            arrivalTime=Label(self.CanReservation2, text=cancelReservationList[i][9])
            arrivalTime.grid(row=3+i, column=3, sticky=EW)
            departDate=Label(self.CanReservation2, text=cancelReservationList[i][2])
            departDate.grid(row=3+i, column=5, sticky=EW)
            departFrom=Label(self.CanReservation2, text=cancelReservationList[i][5])
            departFrom.grid(row=3+i, column=6, sticky=EW)
            arrivesAt=Label(self.CanReservation2, text=cancelReservationList[i][6])
            arrivesAt.grid(row=3+i, column=7, sticky=EW)
            classLabel=Label(self.CanReservation2, text=cancelReservationList[i][1])
            classLabel.grid(row=3+i, column=8, sticky=EW)
            priceLabel=Label(self.CanReservation2, text=cancelReservationList[i][7])
            priceLabel.grid(row=3+i, column=9, sticky=EW)
            NumBag=Label(self.CanReservation2, text=cancelReservationList[i][4])
            NumBag.grid(row=3+i, column=10, sticky=EW)
            PassengerName=Label(self.CanReservation2, text=cancelReservationList[i][3])
            PassengerName.grid(row=3+i, column=11, sticky=EW)
            Duration1=abs((cancelReservationList[i][9]-cancelReservationList[i][8]).total_seconds()/3600)
            DurationHour1=abs(int(Duration1))
            DurationMinute1=abs((int((Duration1-DurationHour1)*60)))
            DurationLabel1=Label(self.CanReservation2, text=str(DurationHour1)+"hr"+str(DurationMinute1)+"min")
            DurationLabel1.grid(row=3+i, column=4,sticky=W)
        DepartureDateList=[]
        DateOfCancellation=datetime.date.today()
        self.Connect()
        cursor21=self.db.cursor()
        sql_getPrice='''SELECT Total FROM Reservation WHERE ReservationID=%s'''
        cursor21.execute(sql_getPrice,(self.CancelReservationId))
        for each in cursor21:
            CancelTotalCost=float(each[0])
        for i in range(len(cancelReservationList)):
            d1 =cancelReservationList[i][2]
            difference=(d1 - DateOfCancellation)
            DepartureDateList.append(difference.days)
        if min(DepartureDateList)>7:
            AmountToBeRefunded=(CancelTotalCost*0.8)-50
            if AmountToBeRefunded<0:
                AmountToBeRefunded=0
        elif min(DepartureDateList)<7 and min(DepartureDateList)>1:
            AmountToBeRefunded=(CancelTotalCost*0.5)-50
            if AmountToBeRefunded<0:
                AmountToBeRefunded=0
        elif min(DepartureDateList)<1:
            messagebox.showerror("Error","Cancellation is not allowed since Departure Date has passesd.")
        self.Connect()
        cursor7=self.db.cursor()
        sql_checkStudent='''SELECT Is_student FROM Customer WHERE C_Username=%s'''
        cursor7.execute(sql_checkStudent,(self.userLog))
        for each in cursor7:
            studentCheck=each[0]

        if int(studentCheck)==1:
            studentDiscLab=Label(self.CanReservation2, text="(Student Discount was applied)")
            studentDiscLab.grid(row=4+len(cancelReservationList), column=2, sticky=E)
        CancelTotalCost="{0:.2f}".format(CancelTotalCost)
        AmountToBeRefunded = "{0:.2f}".format(AmountToBeRefunded)
        totalCostResLabel=Label(self.CanReservation2, text="Total Cost Of reservation      "+ str(CancelTotalCost))
        totalCostResLabel.grid(row=4+len(cancelReservationList), column=1, sticky=W)
        dateCanLabel=Label(self.CanReservation2, text="Date of Cancellation      "+str(DateOfCancellation))
        dateCanLabel.grid(row=5+len(cancelReservationList), column=1, sticky=W)
        AmtRefund=Label(self.CanReservation2, text="Amount to be Refunded       "+ str(AmountToBeRefunded))
        AmtRefund.grid(row=6+len(cancelReservationList), column=1, sticky=W)

        Submit=Button(self.CanReservation2,text="Submit", command=self.cancelResrvationSubmit)
        Submit.grid(row=8+len(cancelReservationList), column=3, sticky=E)
        Back=Button(self.CanReservation2, text="Back", command=self.goBackToCanRes)
        Back.grid(row=8+len(cancelReservationList), column=1, sticky=W)

    def cancelResrvationSubmit(self):
        self.Connect()
        cursor=self.db.cursor()
        sql_deleteReservation='''DELETE FROM ReserveTrain WHERE ReservationID=%s'''
        cursor.execute(sql_deleteReservation,(str(self.CancelReservationId)))
        self.Connect()
        cursor2=self.db.cursor()
        sql_UpdateIsCan='''UPDATE Reservation SET Is_cancelled=%s WHERE ReservationID=%s'''
        cursor2.execute(sql_UpdateIsCan,("1",str(self.CancelReservationId)))
        messagebox.showinfo("Sucess", "Your Reservation was deleted successfully")
        self.CanReservation2.withdraw()
        self.custFunc()

    def goBackToCanRes(self):
        self.CanReservation2.withdraw()
        self.CancelReservation()


    def ViewReview(self):
        self.chofunc.withdraw()
        self.ViewRev1 = Toplevel(rootWin)
        ViewRev=Label(self.ViewRev1, text="View Review")
        ViewRev.grid(row=1, column=1, columnspan = 8, sticky=EW)
        TrainNumLab=Label(self.ViewRev1, text="Train Number    ")
        TrainNumLab.grid(row=2, column=1, sticky=W)
        self.TrainNumEntry=Entry(self.ViewRev1, width=25)
        self.TrainNumEntry.grid(row=2, column=2, sticky=E)  ##Need to find the train from Database.
        Next=Button(self.ViewRev1,text="Next", command=self.ViewReview2)
        Next.grid(row=3, column=2, sticky=E)
        Back=Button(self.ViewRev1, text="Back", command=self.reviewbackback)
        Back.grid(row=3, column=1, sticky=W)
    def reviewbackback(self):
        self.ViewRev1.withdraw()
        self.custFunc()
    def ViewReview2(self):
        self.Connect()
        sql_getTraintosee = '''Select TrainNumber FROM Review'''
        cursor1 = self.db.cursor()
        cursor1.execute(sql_getTraintosee)
        traintrack = []
        for each in cursor1:
            traintrack.append(str(each[0]))

        if str(self.TrainNumEntry.get()) in traintrack:

            self.ViewRev1.withdraw()
            self.ViewRev2 = Toplevel(rootWin)
            ViewRev=Label(self.ViewRev2, text="View Review")
            ViewRev.grid(row=1, column=1, columnspan = 8, sticky=EW)
            self.Connect()
            sql_getreview = '''SELECT Rating, Comment FROM Review WHERE TrainNumber = %s'''
            cursor = self.db.cursor()
            cursor.execute(sql_getreview,(self.TrainNumEntry.get()))
            self.ratco = []
            aDict = {}
            for each in cursor:
                self.ratco.append([each[0],each[1]])



            for i in range(len(self.ratco)): #to create dictionary to store [Rating] -> [comment]
                try:
                    aDict[self.ratco[i][0]].append(", "+self.ratco[i][1])
                except:
                    aDict[self.ratco[i][0]] = [self.ratco[i][1]]
            aList = []
            aList = list(aDict)



            ratingshowLab = Label(self.ViewRev2, text = "Rating")
            ratingshowLab.grid(row=2, column = 1, sticky = W)
            commentshowLab = Label(self.ViewRev2, text = "Comment")
            commentshowLab.grid(row=2, column = 2, sticky = E)
            for i in range(len(aList)):

                ratingLab=Label(self.ViewRev2, text=aList[i])
                ratingLab.grid(row=3+i, column=1, sticky=W)
                commentLab = Label(self.ViewRev2, text = aDict[aList[i]])
                commentLab.grid(row=3+i, column = 2, sticky = E)
            Back=Button(self.ViewRev2, text="Back To Choose Functionality", command=self.viewrevback)
            Back.grid(row=3+len(aList), column=1, columnspan = 8, sticky=EW)
        else:
            messagebox.showerror("Error","No Comment/Rating for this Train or Train Number does not exist")
            self.TrainNumEntry.delete(0,'end')


    def viewrevback(self): #back to chofunc
        self.ViewRev2.withdraw()
        self.chofunc.deiconify()

    def GiveReview(self):
        self.chofunc.withdraw()
        self.GivRev = Toplevel(rootWin)
        GiveRev=Label(self.GivRev, text="Give Review")
        GiveRev.grid(row=1, column=1, columnspan = 8, sticky=EW)
        TrainNumLab=Label(self.GivRev, text="Train Number    ")
        TrainNumLab.grid(row=2, column=1, sticky=W)
        self.TrainNumEntry2=Entry(self.GivRev, width=25)
        self.TrainNumEntry2.grid(row=2, column=2, sticky=W)
        RatingLab=Label(self.GivRev, text="Rating     ")
        RatingLab.grid(row=3, column=1, sticky=W)
        self.Rating=StringVar()
        self.RatingList=["very good", "good", "bad", "very bad"]
        self.Rating.set("very good") #initial value
        Rating=OptionMenu(self.GivRev, self.Rating, *self.RatingList)   ##We need to put the rating into the Database
        Rating.grid(row=3, column=2, sticky=W)
        CommentLab=Label(self.GivRev, text="Comment     ")
        CommentLab.grid(row=4, column=1, sticky=W)
        self.CommentEntry=Entry(self.GivRev, width=50)   ##We need to put the comment into the Database
        self.CommentEntry.grid(row=4, column=2, sticky=W)
        Submit=Button(self.GivRev,text="Submit", command=self.submitRev)
        Submit.grid(row=5, column=2, sticky=EW)

    def submitRev(self):
        self.Connect()
        sql_insertReview = '''INSERT INTO Review(C_Username, TrainNumber, Rating, Comment) VALUES (%s, %s, %s, %s)'''
        cursor = self.db.cursor()
        sql_getTrainNumberber = '''SELECT TrainNumber FROM TrainRoute'''
        traintrainnumNum = []
        cursor.execute(sql_getTrainNumberber)
        cursor1 = self.db.cursor()
        for each in cursor:
            traintrainnumNum.append(each[0])
        for i in range(len(traintrainnumNum)):
            traintrainnumNum[i] = str(traintrainnumNum[i])
        if self.TrainNumEntry2.get() != '' and self.Rating.get() != '' and str(self.TrainNumEntry2.get()) in traintrainnumNum: #check if any field is empty
            cursor1.execute(sql_insertReview, (self.userLog, self.TrainNumEntry2.get(), self.Rating.get(), self.CommentEntry.get()))
            messagebox.showinfo("Success", "Review has been added successfully")
            self.GivRev.withdraw()
            self.chofunc.deiconify()
        else:
            messagebox.showerror("Error", "Reinput Train Number and Rating fields")

    def ManagerFunc(self):
        rootWin.withdraw()
        self.ManFunctionality = Toplevel(rootWin)
        ManFunc=Label(self.ManFunctionality, text="Choose Functionality")
        ManFunc.grid(row=1, column=1, columnspan = 8, sticky=EW)
        ViewRevRep=Button(self.ManFunctionality, text="View Revenue Report", command=self.ViewRevenueReport)
        ViewRevRep.grid(row=2, column=1, sticky=EW)
        ViewPopRouRep=Button(self.ManFunctionality, text="View Popular Route Report", command=self.ViewPopularRouteReport)
        ViewPopRouRep.grid(row=3, column=1, sticky=EW)
        LogOut=Button(self.ManFunctionality, text="Log Out", command=self.LogOutMan)
        LogOut.grid(row=4, column=1, sticky=EW)

    def ViewRevenueReport(self):

        if self.trackManFunc==1:
            self.ViewPopularRouteRep.withdraw()
            self.ManFunctionality.withdraw()
        else:
            self.ManFunctionality.withdraw()
        self.ViewRevenueRep = Toplevel(rootWin)
        ViewREvLab=Label(self.ViewRevenueRep, text="View Revenue Report")
        ViewREvLab.grid(row=1, column=1, columnspan = 8, sticky=EW)
        MonLab=Label(self.ViewRevenueRep, text="Month           ")
        MonLab.grid(row=2, column=1, sticky=W)
        RevLab=Label(self.ViewRevenueRep, text="Revenue           ")
        RevLab.grid(row=2, column=2, sticky=W)
        self.Connect()
        cursor = self.db.cursor()
        sql_getReport = '''SELECT *
                            FROM (

                            SELECT MONTH , SUM( Price ) AS TotalRevenue
                            FROM revenuetable
                            WHERE MONTH = EXTRACT(
                            MONTH FROM CURDATE( ) ) -3
                            GROUP BY MONTH
                            )DummyName1
                            UNION
                            SELECT *
                            FROM (

                            SELECT MONTH , SUM( Price ) AS TotalRevenue
                            FROM revenuetable
                            WHERE MONTH = EXTRACT(
                            MONTH FROM CURDATE( ) ) -2
                            GROUP BY MONTH
                            )DummyName2
                            UNION
                            SELECT *
                            FROM (

                            SELECT MONTH , SUM( Price ) AS TotalRevenue
                            FROM revenuetable
                            WHERE MONTH = EXTRACT(
                            MONTH FROM CURDATE( ) ) -1
                            GROUP BY MONTH
                            )DummyName3'''

        cursor.execute(sql_getReport)
        monthrev = []
        for each in cursor:
            monthrev.append([each[0], each[1]])
        for i in range(len(monthrev)):
            if monthrev[i][0] == 1:
                monthrev[i][0] = "January"
            elif monthrev[i][0] == 2:
                monthrev[i][0] = "February"
            elif monthrev[i][0] == 3:
                monthrev[i][0] = "March"
        for i in range(len(monthrev)):
            monthrev[i][1] = "$"+ str(monthrev[i][1])
        for i in range(len(monthrev)):
            monthport = Label(self.ViewRevenueRep, text = monthrev[i][0])
            monthport.grid(row=3+i, column = 1, sticky = W)
            revport = Label(self.ViewRevenueRep, text = monthrev[i][1])
            revport.grid(row=3+i, column = 2, sticky = W)
        Back=Button(self.ViewRevenueRep, text="Back", command=self.backmanager)
        Back.grid(row=3+len(monthrev), column=1, columnspan = 8, sticky=EW)
    def backmanager(self):
        self.ViewRevenueRep.withdraw()
        self.trackManFunc=1
        self.ManagerFunc()
    def ViewPopularRouteReport(self):
        if self.trackManFunc==1:
            self.ViewRevenueRep.withdraw()
            self.ManFunctionality.withdraw()
        else:
            self.ManFunctionality.withdraw()
        self.ViewPopularRouteRep = Toplevel(rootWin)
        self.Connect()
        cursor = self.db.cursor()

        sql_getpopRoute = '''SELECT *
                            FROM (

                            SELECT EXTRACT(
                            MONTH FROM DepartureDate) AS
                            MONTH , TrainNumber, COUNT( ReservationID ) AS NumRes
                            FROM ReserveTrain
                            WHERE EXTRACT(
                            MONTH FROM DepartureDate ) = EXTRACT( MONTH FROM CURDATE() )-3
                            GROUP BY MONTH , TrainNumber
                            ORDER BY NumRes DESC
                            LIMIT 3
                            )DUMMY_ALIAS1
                            UNION
                            SELECT *
                            FROM (

                            SELECT EXTRACT(
                            MONTH FROM DepartureDate ) AS
                            MONTH , TrainNumber, COUNT( ReservationID ) AS NumRes
                            FROM ReserveTrain
                            WHERE EXTRACT(
                            MONTH FROM DepartureDate ) = EXTRACT( MONTH FROM CURDATE() )-2

                            GROUP BY MONTH , TrainNumber
                            ORDER BY NumRes DESC
                            LIMIT 3
                            )DUMMY_ALIAS2
                            UNION
                            SELECT *
                            FROM (

                            SELECT EXTRACT(
                            MONTH FROM DepartureDate ) AS
                            MONTH , TrainNumber, COUNT( ReservationID ) AS NumRes
                            FROM ReserveTrain
                            WHERE EXTRACT(
                            MONTH FROM DepartureDate ) = EXTRACT( MONTH FROM CURDATE() )-1

                            GROUP BY MONTH , TrainNumber
                            ORDER BY NumRes DESC
                            LIMIT 3
                            )DUMMY_ALIAS3'''
        routerep = []
        cursor.execute(sql_getpopRoute)
        for each in cursor:
            routerep.append([each[0], each[1], each[2]]) # Month, TrainNumber, # Reservation
        viewpop = Label(self.ViewPopularRouteRep, text = "View Popular Route Report")
        viewpop.grid(row = 1, columnspan = 8, sticky = EW)
        monthlablab = Label(self.ViewPopularRouteRep, text = "Month")
        monthlablab.grid(row = 2, column = 1, sticky = W)
        trainnumlab = Label(self.ViewPopularRouteRep, text = "Train number")
        trainnumlab.grid(row = 2, column = 2, sticky = W)
        numres = Label(self.ViewPopularRouteRep, text = "# of Reservations")
        numres.grid(row = 2, column = 3, sticky = W)
        monthneed = []
        for i in range(len(routerep)):
            if routerep[i][0] not in monthneed:
                if routerep[i][0] == 1:
                    monthneed.append(1)
                elif routerep[i][0] == 2:
                    monthneed.append(2)
                elif routerep[i][0] == 3:
                    monthneed.append(3)
        monthtext = []
        for i in range(len(monthneed)):
            if monthneed[i] == 1:
                monthtext.append("January")
            elif monthneed[i] == 2:
                monthtext.append("February")
            elif monthneed[i] == 3:
                monthtext.append("March")
        janmonthlab = Label(self.ViewPopularRouteRep,text = monthtext[0])
        janmonthlab.grid(row = 3, column = 1, sticky = W)
        febmonthlab = Label(self.ViewPopularRouteRep,text = monthtext[1])
        febmonthlab.grid(row=6, column = 1, sticky = W)
        marmonthlab = Label(self.ViewPopularRouteRep,text = monthtext[2])
        marmonthlab.grid(row = 9, column = 1, sticky = W)
        for i in range(len(routerep)):
            trainnumlabs = Label(self.ViewPopularRouteRep,text = routerep[i][1])
            trainnumlabs.grid(row=i+3, column = 2, sticky = EW)
            revnumlab = Label(self.ViewPopularRouteRep,text = routerep[i][2])
            revnumlab.grid(row=i+3, column = 3, sticky = EW)
        back = Button(self.ViewPopularRouteRep,text = "Back", command = self.backpoproute)
        back.grid(row = len(routerep) + 8, column = 2, sticky = W)
    def backpoproute(self):
        self.ViewPopularRouteRep.withdraw()
        self.trackManFunc=1
        self.ManagerFunc()
    def LogOutMan(self):
        self.ManFunctionality.withdraw()
        rootWin.deiconify()
        self.userEntry.delete(0,'end')
        self.passEntry.delete(0,'end')
    def LogOutCust(self):
        self.chofunc.withdraw()
        rootWin.deiconify()
        self.userEntry.delete(0,'end')
        self.passEntry.delete(0,'end')
rootWin = Tk()
app = Phase3(rootWin)
rootWin.mainloop()

