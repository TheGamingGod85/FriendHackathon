from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_logic', methods=['POST'])
def run_python_logic():
    import webbrowser
    import csv
    from datetime import date   # import class date from module datetime
    from flask import request
    
    selected_car = request.form.get('car_model')
    selected_location = request.form.get('parking_location')


    def open_location_on_google_maps(latitude, longitude):
        maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"
        webbrowser.open(maps_url)


    def park_cost():   # function define
        const = 10
        weekend = ('Friday', 'Saturday', 'Sunday')
        additional = 20
        current_date = date.today()  # storing value of current date
        pricing = {'low': 10, 'med': 20, 'high': 40}  # charges according to demand
        # storing day part of date by converting string output to integer
        day = int(current_date.strftime("%d"))
        month = int(current_date.strftime("%m"))  # storing month part of date
        dname = current_date.strftime("%A")  # storing name of day
        f = open('./csv/festivals.csv', 'r')
        fread = csv.reader(f)
        for row in fread:
            if int(row[0]) == day and int(row[1]) == month:  # comparing with csv file records
                charges = const + pricing[row[2]]
                break
            elif dname in weekend:
                charges = const + additional
            else:
                charges = const
        return charges
        f.close()


    park_cost()  # function call
    car_len = 0
    car_wid = 0


    def car_details(cname):
        newcar = ""

        for char in cname:
            if char.isspace():
                continue
            else:
                newcar += char.lower()

        f = open("./csv/car.csv", 'r')
        car_data = csv.reader(f)
        for row in car_data:
            if row[0] == newcar:
                length = row[1]
                width = row[2]
                break
        return (length, width)


    # The car base dimensions have been assigned
    # street parking sl1,sl2,sl3,sw1,sw2,sw3 and parking lots pl1,pl2,pw1,pw2

    # length of street
    sl1 = 20
    sl2 = 16
    sl3 = 15

    #width of street
    sw1 = 9
    sw2 = 7
    sw3 = 6

    #length of parking lot
    pl1 = 100
    pl2 = 80

    #width of parking lot
    pw1 = 40
    pw2 = 50

    #fixed parking rates
    pAconst = 10
    pBconst = 20
    s1const = 8
    s2const = 5
    s3const = 10

    occupied_s1 = 0
    occupied_s2 = 0
    occupied_s3 = 0

    Occupied_area_A = 0
    Occupied_area_B = 0
    dimension = ()

    laneA1_wid = pw1  #initializing lane valiables for parking lot A
    laneA2_wid = pw1
    laneA3_wid = pw1
    laneA4_wid = pw1
    laneA5_wid = pw1

    laneB1_wid = pw2  #initializing lane valiables for parking lot B
    laneB2_wid = pw2
    laneB3_wid = pw2
    laneB4_wid = pw2

    f = open('./csv/variablenames.csv', 'r')   # taking value of variables stored in csv file
    fread = csv.reader(f)
    for row in fread:
        Occupied_area_A = float(row[0])
        Occupied_area_B = float(row[1])
        laneA1_wid = float(row[2])
        laneA2_wid = float(row[3])
        laneA3_wid = float(row[4])
        laneA4_wid = float(row[5])
        laneA5_wid = float(row[6])
        laneB1_wid = float(row[7])
        laneB2_wid = float(row[8])
        laneB3_wid = float(row[9])
        laneB4_wid = float(row[10])

    f.close()

    #the main program starts here


    cname = selected_car
    dimension = car_details(cname)
    car_len = float(dimension[0])
    car_wid = float(dimension[1])


    print(car_len)

    occupied_len = car_len + 1  #adding extra space for easy movement
    occupied_wid = car_wid + 2
    car_ar = occupied_len * occupied_wid

    Available_area_A = pl1 * pw1 - Occupied_area_A    #area after cars are parked
    Available_area_B = pl2 * pw2 - Occupied_area_B

    vacancyA = Available_area_A/(occupied_len * occupied_wid)   #number of cars that can be parked
    vacancyB = Available_area_B/(occupied_len * occupied_wid)


    print(""" Please use the following scheming to input your choice:
    1 = street parking 1
    2 = street parking 2
    3 = street parking 3
    4 = parking lot A
    5 = parking lot B""")
    print("Your parking options are as follows: ")
    if car_len < sl1 and car_wid < sw1 and occupied_s1 == 0:  #comparing car size with street size
        print("\n\nStreet parking 1")
        price = s1const + park_cost()
        print("The price is: ", price)
        latitude = 28.523
        longitude = 77.5734
    if car_len < sl2 and car_wid < sw2 and occupied_s2 == 0:  #comparing car size with street size
        print("\n\nStreet parking 2")
        price = s2const + park_cost()
        print("The price is: ", price)
        latitude = 28.523579
        longitude = 77.569016
    if car_len < sl3 and car_wid < sw3 and occupied_s3 == 0:   #comparing car size with street size
        print("\n\nStreet parking 3")
        price = s3const + park_cost()
        print("The price is: ", price)
        latitude = 28.523397
        longitude = 77.5696624
    if vacancyA != 0:
        print("\n\nParking lot A")
        price = pAconst + park_cost()
        print("The price is: ", price)
        print("The number of vacant spaces is: ", int(vacancyA))
        latitude = 28.524483
        longitude = 77.5744019
    if vacancyB != 0:
        print("\n\nParking lot B")
        price = pBconst + park_cost()
        print("The price is: ", price)
        print("The number of vacant spaces is: ", int(vacancyB))

        latitude = 28.527399
        longitude = 77.577824
    flag = 1
    choice = 0
    while flag != 0:
        choice = int(selected_location)
        if choice not in (1, 2, 3, 4, 5):
            print("Please enter valid option")
        else:
            flag = 0
            break

    pA_lanes = int(pl1 / 17)  #length of a big suv is around 17 feet
    pB_lanes = int(pl2 / 17)

  #saving parking lane in text file

    if choice == 4:
        for i in range(1, pA_lanes+1):
            if i == 1:

                if occupied_wid < laneA1_wid:
                    laneA1_wid -= car_wid
                    instruct = ("Park in lane 1")
                    occupied_s1 = 1
                    Occupied_area_A += car_ar
                    break
            if i == 2:

                if occupied_wid < laneA2_wid:
                    laneA2_wid -= occupied_wid
                    instruct = ("Park in lane 2")
                    occupied_s2 = 1
                    Occupied_area_A += car_ar
                    break

            if i == 3:

                if occupied_wid < laneA3_wid:
                    laneA3_wid -= occupied_wid
                    instruct = ("Park in lane 3")
                    occupied_s3 = 1
                    Occupied_area_A += car_ar
                    break
            if i == 4:

                if occupied_wid < laneA4_wid:
                    laneA4_wid -= occupied_wid
                    instruct = ("Park in lane 4")
                    Occupied_area_A += car_ar
                    break
            if i == 5:

                if occupied_wid < laneA5_wid:
                    laneA5_wid -= occupied_wid
                    instruct = ("Park in lane 5")
                    Occupied_area_A += car_ar
                    break


    if choice ==5:
        for i in range(1, pB_lanes + 1):
            if i == 1:

                if occupied_wid < laneB1_wid:
                    laneB1_wid -= car_wid
                    instruct = ("Park in lane 1")
                    Occupied_area_B += car_ar
                    break
            if i == 2:

                if occupied_wid < laneB2_wid:
                    laneB2_wid -= occupied_wid
                    instruct = ("Park in lane 2")
                    Occupied_area_B += car_ar
                    break

            if i == 3:

                if occupied_wid < laneB3_wid:
                    laneB3_wid -= occupied_wid
                    instruct = ("Park in lane 3")
                    Occupied_area_B += car_ar
                    break
            if i == 4:

                if occupied_wid < laneB4_wid:
                    laneB4_wid -= occupied_wid
                    instruct = ("Park in lane 4")
                    Occupied_area_B += car_ar
                    break

    #storing new variable values in csv file
    var = [Occupied_area_A,Occupied_area_B,laneA1_wid,laneA2_wid,laneA3_wid,laneA4_wid,laneA5_wid,laneB1_wid,laneB2_wid,laneB3_wid,laneB4_wid]
    f = open("./csv/variablenames.csv", 'w', newline = '')
    objwrite = csv.writer(f)
    objwrite.writerow(var)
    f.close()
    open_location_on_google_maps(latitude, longitude)  #redirect to google maps

    # The user has reached the parking lot successfully



    result = """Selected car: {}, Parking location: {}, 
                Parked At: Latitude: {}, Longitude: {}, Instruction: {}""".format(selected_car, selected_location, latitude, longitude, instruct)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
