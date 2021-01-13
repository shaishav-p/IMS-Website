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
