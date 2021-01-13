from flask import Flask, render_template, request
import time
import sys
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-jersey', methods = ["GET", "POST"])
def addJersey():
    errors = ""
    if request.method == "POST":
        infoList = []
        jerseyNumber = None
        try:
            jerseyNumber = int(request.form["Jersey number"])
        except: 
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["Jersey number"])
        
        if jerseyNumber is not None:
            infoList.append("\n")  # creates a new line for next time the text is appended
            infoList.append(str(jerseyNumber))
            # the "," is added as that will be used to split the row info bc/ info such as the team name can be 1+ words
            infoList.append(",")

            jerseyTeamName = str(request.form["Team name"])
            infoList.append(jerseyTeamName)
            infoList.append(",")

            condition = str(request.form["Condition"])
            infoList.append(condition)
            infoList.append(",")

            infoList.append("In inventory")
            infoList.append(",")

            location = str(request.form["Location"])
            infoList.append(location)
            infoList.append(",")

            additionalComments = str(request.form["Additional Comments"])

            if len(additionalComments) != 0:
                infoList.append(additionalComments)
            else:
                infoList.append("N/A")

            s = "\t"
            infoList = s.join(infoList)

            inventory = open("inventory.csv", "a+")

            fileSize = os.stat("inventory.csv").st_size
            if fileSize == 0:  # if fileSize equals 0, this indicates that the file is empty
                inventory.write("Number , Team Name , Condition , Status , Location , Comments")

            inventory.writelines(infoList)
            #inventory.write("\n")  # creates a new line for next time the text is appended

            inventory.close()

            return render_template('success.html', title="Add Jersey", successMsg="added jersey to inventory!")


    return render_template('add-jersey.html', errors=errors)


@app.route('/sign-out-jersey', methods = ["GET", "POST"])
def signOutJersey():
    errors = ""
    if request.method == "POST":
        #verify that a jersey with the given jersey number and team exists in inventory
        jerseyNumber = str(request.form["Jersey number"]).strip()
        teamName = str(request.form["Team name"]).strip()
        athleteName = str(request.form["Athlete name"])
        additionalComments = str(request.form["Additional comments"])
        #print("num: "+ jerseyNumber+ " team name: "+ teamName)

        inventory = open("inventory.csv", "r+")  # 'r' is used to read the file
        infoFile = inventory.readlines()
        lineNum = 0
        inventory = open("inventory.csv", "r+")  # 'r+' is used to read and write in the file

        for line in inventory:
            rowList = line.split(",")  # splits line and creates list
            number = rowList[0]  # makes variable equal to list
            number = "".join(number)
            number = number.strip()
            #print("current loop num:" + number +"."+ str(jerseyNumber == number))
            if str(jerseyNumber) == str(number):  # rowlist[0] is the team number
                name = rowList[1]
                name = "".join(name)
                name = name.strip()
                name = name.lower()
                #print("current loop name:" + name +"." + "team name:" + teamName.lower() +"."+ str(teamName.lower() == name))

                if teamName.lower() == name:  # rowList[1] is the team name
                    #print("----> full match")
                    infoList = []
                    infoList.append(rowList[0])
                    infoList.append(",")
                    infoList.append(rowList[1])
                    infoList.append(",")
                    rowList[2] = rowList[2].rstrip("\n")
                    infoList.append(rowList[2])
                    infoList.append(",")

                    infoList.append("Signed out by:")
                    infoList.append(athleteName)
                    infoList.append("on")

                    currentDate = Date()
                    infoList.append(currentDate)
                    infoList.append(",")

                    infoList.append("N/A")
                    infoList.append(",")

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

                    return render_template('success.html', title="Sign Out Jersey", successMsg=" signed out jersey to {}".format(athleteName))

            lineNum = lineNum + 1 
        
        #if reach end of for loop that means that jersey with the given jersey number and team DNE in inventory
        errors += "A jersey with number {!r} and team name {!r} does not exist; check the inventory to make sure the jersey in the inventory.\nPlease enter valid jersey information.\n".format(jerseyNumber, teamName)
        

    return render_template('sign-out-jersey.html', errors=errors)
def Date():  # function returns current date
   currentDateAndTime = time.asctime(time.localtime(time.time()))  # gives current date and time
   currentDateAndTime = currentDateAndTime.split()
   del currentDateAndTime[-2]  # removes time from list so the list now only contains the date
   s = " "
   # the date (including day of the week, day of the month, month, and year) is joined into one string
   currentDate = s.join(currentDateAndTime)
   return currentDate


@app.route('/sign-in-jersey', methods = ["GET", "POST"])
def signInJersey():
    errors = ""
    if request.method == "POST":
        jerseyNumber = str(request.form["Jersey number"]).strip()
        teamName = str(request.form["Team name"]).strip()
        condition = str(request.form["Condition"])
        location = str(request.form["Location"])
        additionalComments = str(request.form["Additional comments"])

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

                    rowList[5] = rowList[5].rstrip("\n")  # '\n' is stripped from the end of the list as new information needs to be added to the list

                    historyList = rowList

                    del historyList[4]  # removes 'N/A' for the stoarage location

                    infoList.append(jerseyNumber)
                    infoList.append(",")  # the "," is added as that will be used to split the row information bc/ information such as the team name might be more than one word so blank spaces cannot be used to split when required

                    infoList.append(teamName)
                    infoList.append(",")

                    priorCondition = historyList[2]
                    priorCondition = "".join(priorCondition)
                    priorCondition = priorCondition.strip()
                    priorCondition = "Condition prior to return: " + priorCondition + ", "

                    infoList.append(condition)
                    historyList[2] = priorCondition + "Condition upon return:" + condition + "\t"

                    infoList.append(",")

                    infoList.append("In inventory")
                    infoList.append(",")

                    infoList.append(location)
                    infoList.append(",")


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
                    
                    return render_template('success.html', title="Sign In Jersey", successMsg=" signed in jersey.")


            lineNum = lineNum + 1
        
        #if reach end of for loop that means that jersey with the given jersey number and team DNE in inventory
        errors += "A jersey with number {!r} and team name {!r} does not exist; check the inventory to make sure the jersey in the inventory.\nPlease enter valid jersey information.\n".format(jerseyNumber, teamName)
         

    return render_template('sign-in-jersey.html', errors=errors)


@app.route('/edit-jersey', methods = ["GET", "POST"])
def editJersey():
    errors = ""
    if request.method == "POST":
        jerseyNumber = str(request.form["Jersey number"]).strip()
        teamName = str(request.form["Team name"]).strip()
        condition = str(request.form["Condition"])
        location = str(request.form["Location"])
        additionalComments = str(request.form["Additional comments"])

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

                    infoList.append(condition)
                    infoList.append(",")

                    infoList.append("In inventory")
                    infoList.append(",")
                    
                    infoList.append(location)
                    infoList.append(",")

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

                    return render_template('success.html', title="Edit Jersey", successMsg=" editted jersey number {} from the {} team".format(jerseyNumber, teamName))

            lineNum = lineNum + 1

        #if reach end of for loop that means that jersey with the given jersey number and team DNE in inventory
        errors += "A jersey with number {!r} and team name {!r} does not exist; check the inventory to make sure the jersey in the inventory.\nPlease enter valid jersey information.\n".format(jerseyNumber, teamName)

    
    return render_template('edit-jersey.html', errors=errors)


@app.route('/view-inventory')
def viewInventory():

    return render_template('view-inventory.html')



@app.route('/inventory.csv')
def inventoryFile():
    inventory = open("inventory.csv", "r")
    contents = inventory.read()
    inventory.close()

    return contents






#app.run(host='0.0.0.0', port=81)

if __name__ == '__main__':
    app.run(debug=True)
