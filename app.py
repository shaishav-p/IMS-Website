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
        jerseyNumber = request.form["Jersey number"]
        teamName = str(request.form["Team name"]).strip()
        athleteName = str(request.form["Athlete name"])
        additionalComments = str(request.form["Additional comments"])
        print("num: "+ jerseyNumber+ " team name: "+ teamName)

        inventory = open("inventory.csv", "r+")  # 'r' is used to read the file
        infoFile = inventory.readlines()
        lineNum = 0
        inventory = open("inventory.csv", "r+")  # 'r+' is used to read and write in the file

        for line in inventory:
            rowList = line.split(",")  # splits line and creates list
            number = rowList[0]  # makes variable equal to list
            number = "".join(number)
            number = number.strip()
            print("current loop num:" + number +"."+ str(jerseyNumber == number))
            if str(jerseyNumber) == str(number):  # rowlist[0] is the team number
                name = rowList[1]
                name = "".join(name)
                name = name.strip()
                name = name.lower()
                print("current loop name:" + name +"." + "team name:" + teamName.lower() +"."+ str(teamName.lower() == name))

                if teamName.lower() == name:  # rowList[1] is the team name
                    print("----> full match")
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

                    return render_template('success.html', title="Sign Out Jersey", successMsg="successfully signed out jersey to {}".format(athleteName))

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
