import os
import sys
import time


def Date():  # function returns current date
   currentDateAndTime = time.asctime(time.localtime(time.time()))  # gives current date and time
   currentDateAndTime = currentDateAndTime.split()
   del currentDateAndTime[-2]  # removes time from list so the list now only contains the date
   s = " "
   # the date (including day of the week, day of the month, month, and year) is joined into one string
   currentDate = s.join(currentDateAndTime)
   return currentDate


def userLogin():
   print("\nLogin:\n-----\n")

   x = 0
   counter = 0
   while x == 0:
       userName = input("Username: ")
       password = input("Password: ")

       if userName == "sports" and password == "sports@123":
           print("Login successful! ")
           print("\n" * 50)  # clears screen by printing 50 lines
           x = 1
       else:
           print("Login unsuccessful. Please try again. \n") # Error handling

       counter = counter + 1
       if counter == 5:
           print("5 unsuccessful attempts. Program Closed.")
           sys.exit()  # closes program


def jerseyCondition():
   print("Condition of clothing: \n1. Excellent (New) \n2. Good (worn but in good condition) \n3. Okay (worn and shows minor damage/flaws) \n4. Poor(significant damage)")
   jerseyConditionNumber = int(input("Which number from above best describes the clothing's condition? "))

   if jerseyConditionNumber == 1:
       condition = "Excellent"
   elif jerseyConditionNumber == 2:
       condition = "Good"
   elif jerseyConditionNumber == 3:
       condition = "Okay"
   elif jerseyConditionNumber == 4:
       condition = "Poor"
   else:
       condition = "Error"
   return condition


def addJersey():
   inventory = open("inventory.csv", "a+")

   fileSize = os.stat("inventory.csv").st_size
   if fileSize == 0:  # if fileSize equals 0, this indicates that the file is empty
       inventory.write("Number , Team Name , Condition , Status , Location , Comments \n")

   infoList = []
   while True:  # error handling
       try:
           jerseyNumber = int(input("What is the number of the jersey? "))
       except ValueError:
           print("\n\nPlease enter an integer value!\n")
           continue
       else:
           break  # breaks out of loop if there is no error (ie. user enters an integer)

   infoList.append(str(jerseyNumber))
   infoList.append(",")
   # the "," is added as that will be used to split the row info bc/ info such as the team name can be 1+ words

   jerseyTeamName = input("Which team is it for? ")
   infoList.append(jerseyTeamName)
   infoList.append(",")

   condition = jerseyCondition()
   infoList.append(condition)
   infoList.append(",")

   infoList.append("In inventory")
   infoList.append(",")

   location = input("Location where clothing will be stored: ")
   infoList.append(location)
   infoList.append(",")

   additionalComments = input("If you want to add any additional comments, please enter them here "
                              "(note: when entering information, please do not use any commas. "
                              "If not press the 'enter' key. ")
   if len(additionalComments) != 0:
       infoList.append(additionalComments)
   else:
       infoList.append("N/A")

   s = "\t"
   infoList = s.join(infoList)

   inventory.writelines(infoList)
   inventory.write("\n")  # creates a new line for next time the text is appended

   inventory.close()
   print("------------------------------------------------------------")


def viewTeamInInventory():
   teamName = input("Please enter the name of the team whose jersey inventory you wish to see: ")
   header = teamName.capitalize() + " athletic wear: \n"
   print(header)

   inventory = open("inventory.csv", "r")
   specificTeam = open("specific_team_inventory.csv", "w+")

   numOfJerseys = 0
   for line in inventory:
       rowList = line.split(",")  #
       if len(rowList) > 1:  # to avoid the program from crashing because the last line in the file is always blank

           if teamName.lower() == rowList[1].strip().lower():  # rowList[1] is the team name
               #  .strip() removes the tab characters from both ends of th string
               # .lower() converts the string to lower case

               if numOfJerseys == 0:
                   specificTeam.write(header)
               specificTeam.write(line)
               print(line)
               numOfJerseys = numOfJerseys + 1
   if numOfJerseys == 0:
       print("None in inventory.")
   print("This information can also be viewed by opening the file 'specific_team_inventory.csv'")
   print("------------------------------------------------------------")


def editInventory():
   jerseyNumber = input("Please enter the number of the jersey you wish to edit: ")
   teamName = input("Please enter the team name of the jersey: ")

   inventory = open("inventory.csv", "r+")  # 'r' is used to read the file
   infoFile = inventory.readlines()

   lineNum = 0
   inventory = open("inventory.csv", "r+")  # 'r+' is used to read and write in the file

   for line in inventory:
       rowList = line.split(",")  # splits lineNum and creates list
       number = rowList[0]  # makes variable equal to 1st element in list (the jersey number)
       number = "".join(number)  # converts list into string
       number = number.strip()  # removes any spaces on either side of the number

       if str(jerseyNumber) == str(number):
           name = rowList[1]  # makes variable equal to 2nd element in list (the team name)
           name = "".join(name)  # converts list into string
           name = name.strip()  # removes any spaces on either side of the name

           if teamName.lower() == name.lower():
               infoList = []

               rowList[5] = rowList[5].rstrip("\n")
               # '\n' is stripped from the end of the list as new information needs to be added to the line

               infoList.append(jerseyNumber)
               infoList.append(",")
               # the "," is added as that will be used to split the row info bc/ info like team name might be 1+ word
               infoList.append(teamName)
               infoList.append(",")

               condition = jerseyCondition()
               infoList.append(condition)
               infoList.append(",")

               infoList.append("In inventory")
               infoList.append(",")
              
               location = input("Location where clothing will be stored: ")
               infoList.append(location)
               infoList.append(",")

               additionalComments = input("If you want to add any additional comments, please enter them here "
                                          "(note: when entering information, please do not use any commas. "
                                          "If not press the 'enter' key. ")
               if len(additionalComments) != 0:
                   infoList.append(additionalComments)
               else:
                   infoList.append("N/A")

               infoList.append("\n")
               s = "\t"
               infoList = s.join(infoList)
               # print(infoList) #for debugging

               infoFile[lineNum] = infoList

               inventory = open("inventory.csv", "w+")
               inventory.writelines(infoFile)

       lineNum = lineNum + 1
   inventory.close()
   print("------------------------------------------------------------")


def signOut():
   jerseyNumber = input("Please enter the number of the jersey being signed out: ")

   teamName = input("Please enter the name of the team: ")
   inventory = open("inventory.csv", "r+")  # 'r' is used to read the file
   infoFile = inventory.readlines()

   # print(infoFile)

   lineNum = 0
   inventory = open("inventory.csv", "r+")  # 'r+' is used to read and write in the file
   for line in inventory:
       rowList = line.split(",")  # splits line and creates list
       number = rowList[0]  # makes variable equal to list
       number = "".join(number)
       number = number.strip()

       if str(jerseyNumber) == str(number):  # rowlist[0] is the team number

           name = rowList[1]
           name = "".join(name)
           name = name.strip()
           name = name.lower()
           if teamName.lower() == name:  # rowList[1] is the team name
               infoList = []
               infoList.append(rowList[0])
               infoList.append(",")
               infoList.append(rowList[1])
               infoList.append(",")
               rowList[2] = rowList[2].rstrip("\n")
               infoList.append(rowList[2])
               infoList.append(",")

               name = input("Please enter the name of the athlete signing it out: ")
               infoList.append("Signed out by:")
               infoList.append(name)
               infoList.append("on")

               currentDate = Date()
               infoList.append(currentDate)
               infoList.append(",")

               infoList.append("N/A")
               infoList.append(",")

               additionalComments = input("If you want to add any additional comments, please enter them here "
                                          "(note: when entering information, please do not use any commas. "
                                          "If not press the 'enter' key. ")

               if len(additionalComments) != 0:

                   infoList.append(additionalComments)
               else:
                   infoList.append("N/A")

               infoList.append("\n")

               s = " "
               infoList = s.join(infoList)
               infoFile[lineNum] = infoList

               inventory = open("inventory.csv", "w+")
               inventory.writelines(infoFile)

       lineNum = lineNum + 1
   inventory.close()
   generateSignedOutFile()
   print("------------------------------------------------------------")


def generateSignedOutFile():
   inventory = open("inventory.csv", "r")
   # 'r' is used to read the file
   signOutFile = open("signOut.csv","w+")
   # 'w+' is used so the contents of the old file are overwritten

   numberOfClothesSignedOut = 0
   for line in inventory:
       infoLine = line.split(",")
       if len(infoLine) > 1:
           status = infoLine[3]
           status = "".join(status)  # makes list into string
           status = status.strip()

           if status != "In inventory" and status != "Status":
               numberOfClothesSignedOut = numberOfClothesSignedOut + 1
               if numberOfClothesSignedOut == 1:
                   # prints header on first line on file with labels for columns
                   signOutFile.write("Number , Team Name , Condition , Status , Location, Comments \n")

               signOutFile.write(line)

   if numberOfClothesSignedOut == 0:
       signOutFile.write("Currently, no athletic wear is signed out.")


def viewTeamInSignOutFile():
   generateSignedOutFile()
   signOutFile = open("signOut.csv", "r+")
   specificTeamFile = open("specific_team_signOut.csv", "w+")

   teamChoice = input("Would you like to view the sign outs for a particular team? "
                      "If yes, please enter the name of the team. If not, please press the enter key. ")
   for line in signOutFile:
       rowList = line.split(",")

       # to stop the program from crashing as the last line is blank and thus it does not have multiple elements
       if len(rowList) > 1:
           name = rowList[1]  # makes variable equal to 2nd element in list (the team name)
           name = "".join(name)  # converts list into string
           name = name.strip()  # removes any spaces on either side of the name
           if teamChoice.lower() == name.lower():
               print(line)
               specificTeamFile.write(line)
   print("This information can also be viewed by opening the file 'specific_team_signOut.csv'")
   print("------------------------------------------------------------")
   signOutFile.close()
   specificTeamFile.close()


def signIn():
   jerseyNumber = input("Please enter the number of the jersey being signed in: ")
   teamName = input("Please enter the name of the team: ")

   inventory = open("inventory.csv", "r+")  # 'r' is used to read the file
   infoFile = inventory.readlines()

   lineNum = 0
   inventory = open("inventory.csv", "r+")  # 'r+' is used to read and write in the file

   for line in inventory:
       rowList = line.split(",")  # splits line and creates list
       number = rowList[0]  # makes variable equal to 1st element in list (the jersey number)
       number = "".join(number)  # converts list into string
       number = number.strip()  # removes any spaces on either side of the number

       if str(jerseyNumber) == str(number):
           name = rowList[1]  # makes variable equal to 2nd element in list (the team name)
           name = "".join(name)  # converts list into string
           name = name.strip()  # removes any spaces on either side of the name

           if teamName.lower() == name.lower():
               infoList = []

               rowList[5] = rowList[5].rstrip(
                   "\n")  # '\n' is stripped from the end of the list as new information needs to be added to the list

               historyList = rowList

               del historyList[4]  # removes 'N/A' for the stoarage location

               infoList.append(jerseyNumber)
               infoList.append(
                   ",")  # the "," is added as that will be used to split the row information bc/ information such as the team name might be more than one word so blank spaces cannot be used to split when required

               infoList.append(teamName)
               infoList.append(",")

               priorCondition = historyList[2]
               priorCondition = "".join(priorCondition)
               priorCondition = priorCondition.strip()
               priorCondition = "Condition prior to return: " + priorCondition + ", "

               condition = jerseyCondition()
               infoList.append(condition)
               historyList[2] = priorCondition + "Condition upon return:" + condition + "\t"

               infoList.append(",")

               infoList.append("In inventory")
               infoList.append(",")

               location = input("Location where clothing will be stored: ")
               infoList.append(location)
               infoList.append(",")

               additionalComments = input("If you want to add any additional comments, please enter them here "
                                          "(note: when entering information, please do not use any commas. "
                                          "If not press the 'enter' key. ")
               if len(additionalComments) != 0:
                   infoList.append(additionalComments)
               else:
                   infoList.append("N/A")
               infoList.append("\n")

               s = "\t"
               infoList = s.join(infoList)

               # replaces the line in the list with the new updated info for the jersey being signed in
               infoFile[lineNum] = infoList

               inventory = open("inventory.csv", "w+")
               inventory.writelines(infoFile)  # writes all lines to file

               s = ",\t"
               currentDate = Date()
               currentDate = " Signed in on: " + currentDate
               historyList.append(currentDate)
               historyList = s.join(historyList)

               historyFile = open("history.csv", "a+")

               historyFile.writelines(historyList)  # writes line to at the end of the file

               # creates a new line so that the next time info. is added to the file it is on a new line
               historyFile.write("\n")

               historyFile.close()

       lineNum = lineNum + 1
   inventory.close()
   generateSignedOutFile()
   print("------------------------------------------------------------")


def repairList():
   inventory = open("inventory.csv", "r")
   repairFile = open("repairList.csv", "w+")


   # lineList = []
   numberOfRepairs = 0
   for line in inventory:
       lineList = line.split(",")

       if len(lineList) > 1:  # to avoid the program from crashing because the last line in the file is always blank
           condition = lineList[2]
           condition = "".join(condition) # converts to string
           condition = condition.strip()  # removes blank spaces from ends of string

           if condition == "Poor":
               numberOfRepairs = numberOfRepairs + 1
               if numberOfRepairs == 1:
                   repairFile.write("Number , Team Name , Condition , Status , Location, Comments \n")
                   # prints header on first line on file with labels for columns

               s = ","
               lineList = s.join(lineList)
               repairFile.write(lineList)
   if numberOfRepairs == 0:
       repairFile.write("Currently, no athletic wear is in need of repairs.")

   inventory.close()
   repairFile.close()

# function will be used to help the user narrow their search as the file "history.csv" can be very long after some use
def historyFileSearch():
   jerseyNumber = input("Please enter the number of the jersey whose sigin in/out history you wish to see: ")
   teamName = input("Please enter the name of the team to which the jersey belongs: ")

   historyFile = open("history.csv", "r")

   for line in historyFile:
       rowList = line.split(",")  # splits line at ',' and adds the contents to the list

       if str(jerseyNumber) == str(rowList[0].strip()):  # rowlist[0] is the team number

           if teamName.lower() == rowList[1].strip().lower():  # rowList[1] is the team name
               # .strip() removes the tab characters from both ends of string # .lower() converts string to lower case
               print(line)
   print("------------------------------------------------------------")
   historyFile.close()


def mainMain():
   rerun = ""
   while rerun.lower() != "no":

       print ("1 - Add Jersey"
              "\n2 - Sign Out Jersey"
              "\n3 - Sign In Jersey"
              "\n4 - Edit Information of Jersey in Inventory"
              "\n5 - View Inventory for Specific Team"
              "\n6 - View Sign Outs for Specific Team"
              "\n7 - View history of sign ins/out for a jersey")

       action = int(input("Enter the number of the action you wish to do: "))
       if action == 1 or action == 2 or action == 3 or action == 4:
           repeat = int(input("\nHow many times would you like to repeat the chosen action? "
                              "\nPlease enter a numeric value: "))
       else:
           repeat = 1
       print("\n")

       for i in range(repeat):
           if action == 1:
               addJersey()
           elif action == 2:
               signOut()
           elif action == 3:
               signIn()
           elif action == 4:
               editInventory()
           elif action == 5:
               viewTeamInInventory()
           elif action == 6:
               viewTeamInSignOutFile()
           elif action == 7:
               historyFileSearch()
           else:   # invalid number or string entered
               print("\nPlease enter a valid number:")
               mainMain()

           print("-----------------------")

       rerun = input("If you would like to perform another action, press the enter key. "
                     "If you do not wish to do so, type 'no': ")

   generateSignedOutFile()  # function creates signOut.csv
   repairList()  # function creates repairList.csv
   print("\n\nHave a great day!")


# code runs here:
userLogin()
mainMain()


