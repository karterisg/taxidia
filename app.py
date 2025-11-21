# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import lib.pymysql as db
import random 
from datetime import datetime ,timedelta


def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)

    return con

def  findTrips(x,a,b):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
    query1 = """
    SELECT  r.offer_trip_package_id,tp.cost_per_person, tp.max_num_participants, COUNT(*) AS reservation_count, (tp.max_num_participants - Count(*))as empty_seats , tp.trip_start , tp.trip_end 
    FROM reservation r , trip_package tp , travel_agency_branch tab
    WHERE r.offer_trip_package_id = tp.trip_package_id
    AND tab.travel_agency_branch_id = r.travel_agency_branch_id
    AND tab.travel_agency_branch_id = '%s'
    AND (tp.trip_start >= '%s' AND tp.trip_start <= '%s')
    GROUP BY offer_trip_package_id , tp.trip_start , tp.trip_end , tp.max_num_participants, tp.cost_per_person;""" % (x,a,b)

    cur.execute(query1)        

    results = [("Package ID","Cost per person","Max number of participants", "Reservations", "Empty_seats", "Trip start", "Trip end","Guides")]
    query_results = cur.fetchall()
    for row in query_results:    
        id = row[0]
        query2 = """
        SELECT e.surname, e.name AS guide
        FROM employees e
        WHERE e.employees_AM IN
            (SELECT gt.travel_guide_employee_AM
            FROM reservation r , trip_package tp , travel_agency_branch tab, guided_tour gt
            WHERE r.offer_trip_package_id = tp.trip_package_id
            AND tab.travel_agency_branch_id = r.travel_agency_branch_id
            AND gt.trip_package_id = tp.trip_package_id
            AND tp.trip_package_id = '%s'
            AND tab.travel_agency_branch_id = '%s'
            AND tp.trip_start >= '%s' AND tp.trip_start<= '%s');""" % (id,x,a,b)
        cur.execute(query2)
        query2_results = cur.fetchall()
        guides = ', '.join([str(element[0] + ' ' + element[1]) for element in query2_results])
        row = row + (guides,)
        
        results.append(row)
    return results

def findRevenue(x): 

   # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    results = [("Branch ID", "Total Reservations", "Total Income", "Total Employees", "Total Salary"),]
    if x == 'ASC' or x == 'DESC' or 'asc' or 'desc':
        query1 = """
        SELECT r.travel_agency_branch_id as BranchID, COUNT(*) AS Reservations , sum(o.cost) AS Revenue
        FROM reservation r, offer o
        WHERE r.offer_id = o.offer_id
        GROUP BY r.travel_agency_branch_id
        ORDER BY sum(o.cost) %s;""" % (x)

        cur.execute(query1)
        query_results = cur.fetchall()

        for row in query_results:
            branchid = row[0]
            query2 = """
            SELECT  count(*) as Employees_number , sum(salary) AS Salary_expenses
            FROM employees e
            WHERE e.travel_agency_branch_travel_agency_branch_id = '%s'
            GROUP BY e.travel_agency_branch_travel_agency_branch_id;""" % (branchid)

            cur.execute(query2)
            query2_results = cur.fetchall()
            for row2 in query2_results:
                row += row2
            results.append(row)
    return results

def bestClient(x):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    results = [("First Name", "Last Name", "Total Countries Visited", "Total Cities Visited", "List of Attractions"),]
    if x == 'Best' or x == 'Best' or x == 'BEST' or 'best':
        query = """
        SELECT tr.name, tr.surname, COUNT(DISTINCT d.country) AS num_countries, COUNT(DISTINCT d.name) AS num_cities
        FROM reservation r, trip_package_has_destination thd, destination d , traveler tr , tourist_attraction ta
        WHERE
            r.offer_trip_package_id = thd.trip_package_trip_package_id
            AND thd.destination_destination_id = d.destination_id
            AND r.Customer_id = tr.traveler_id
            AND ta.destination_destination_id = d.destination_id
            AND r.Customer_id =
                (SELECT r.Customer_id
                FROM reservation r , offer o
                WHERE r.offer_id = o.offer_id
                GROUP BY r.Customer_id
                HAVING sum(o.cost) >= ALL 
                    (SELECT sum(o.cost)
                    FROM reservation r, offer o
                    WHERE r.offer_id = o.offer_id
                    GROUP BY r.Customer_id
                    ORDER BY sum(o.cost) desc
                    )
                )
        GROUP BY tr.traveler_id;"""
        
        query2 = """
        SELECT distinct ta.name
        FROM reservation r  , trip_package_has_destination thd, destination d , tourist_attraction ta , guided_tour gt
        WHERE
            r.offer_trip_package_id = thd.trip_package_trip_package_id
            AND thd.destination_destination_id = d.destination_id
            AND ta.tourist_attraction_id = gt.tourist_attraction_id
            AND gt.trip_package_id = r.offer_trip_package_id
            AND r.Customer_id =
                (SELECT r.Customer_id
                FROM reservation r , offer o
                WHERE r.offer_id = o.offer_id
                GROUP BY r.Customer_id
                HAVING sum(o.cost) >= ALL 
                    (SELECT sum(o.cost)
                    FROM reservation r, offer o
                    WHERE r.offer_id = o.offer_id
                    GROUP BY r.Customer_id
                    ORDER BY sum(o.cost) desc));"""
        cur.execute(query)

        query_results = cur.fetchall()
        for row in query_results:
            cur.execute(query2)
            query2_results = cur.fetchall()
            attractions = ' , '.join([str(element[0]) for element in query2_results])
            row += (attractions,)
            results.append(row)
        return results

def giveAway(N):
    
# Create a new connection
    con = connection()

# Create a cursor on the connection
    cur = con.cursor()
    results = [("Give-Away winners",)] # Output Message list
    ids_list = []  # All winners
    selectedTrips = [] # All trips gifted to avoid same trips

    query1 = """SELECT traveler_id FROM traveler;"""
    cur.execute(query1)
    traveler_ids = cur.fetchall()
    
    for id in traveler_ids:
        ids_list.append(id[0])

# For each choosen traveler 
    for i in range(int(N)):
        traveler = random.choice(ids_list)

    # Find winners name and surname 
        query_name = "SELECT name , surname FROM traveler WHERE traveler_id = %d" % (traveler)
        cur.execute(query_name)
        row = cur.fetchone()
        traveler_name = row[0]
        traveler_surname = row[1]

    # Find how many reservations winner has in order to form the cost of the offer
        query2 = "SELECT COUNT(distinct Reservation_id) FROM reservation WHERE Customer_id = %d;" % (traveler)
        cur.execute(query2)
        reservations = cur.fetchone()
        discount = False
        if (int(reservations[0]) > 1):
            discount = True

    # Find the trip_package_id
        query3 = """SELECT trip_package_id
        FROM trip_package
        WHERE trip_package_id NOT IN (
            SELECT offer_trip_package_id
            FROM reservation
            WHERE Customer_id = %d)
        AND trip_package_id IN (SELECT trip_package_trip_package_id FROM trip_package_has_destination);
        """ % (traveler)

        cur.execute(query3)
        packages = cur.fetchall()

        while True: # Make sure each random selection is unique
            trips = []
            for row in packages:
                trips.append(row[0])
            rand_package = random.choice(trips)
            if rand_package not in selectedTrips:
                selectedTrips.append(rand_package)
                break


    #Find all destinations that the trip_package provides
        query_dest = """SELECT d.name
        FROM destination d
        WHERE d.destination_id IN(SELECT DISTINCT destination_destination_id FROM trip_package_has_destination WHERE trip_package_trip_package_id = %d);""" % (int(selectedTrips[i]))
        cur.execute(query_dest)
        query_result = cur.fetchall()
        destinations = ', '.join([str(element[0]) for element in query_result])


    #Find offer cost based on the trip_package_id    
        query4 = "SELECT cost_per_person FROM trip_package WHERE trip_package_id = %d;" % (selectedTrips[i])
        cur.execute(query4)
        cost = cur.fetchone()
        if discount:
            trip_cost = int(cost[0]) - (int(cost[0]) * 25/100)
            category = 'group-discount'
        else:
            trip_cost = int(cost[0])
            category = 'full-price'

    #Find current date and end date (All offers last 90 days)
        cur_date = datetime.now().strftime("%Y-%m-%d")
        date_object = datetime.strptime(cur_date, "%Y-%m-%d")
        new_date = date_object + timedelta(days= 90)
        end_date = new_date.strftime("%Y-%m-%d")

    # Find offer_id number
        cur.execute("SELECT offer_id + 1 FROM offer GROUP BY offer_id HAVING offer_id >= ALL (SELECT offer_id FROM offer)")
        row = cur.fetchone()
        offer_id = row[0]
        offer_description = "Happy travel tour"

    # Insert new offer
        insert_query = """INSERT INTO offer (offer_id, offer_start, offer_end, cost, description, trip_package_id, offer_info_category) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (offer_id,cur_date, end_date, trip_cost, offer_description, int(selectedTrips[i]), category)
        cur.execute(insert_query)
        con.commit()
        
    # Final Message Output
        message = ("""Congratulations %s %s!
        Pack your bags and get ready to enjoy the %s! At ART TOUR travel we
        acknowledge you as a valued customer and we’ve selected the most incredible
        tailor-made travel package for you. We offer you the chance to travel to ( %s )
        at the incredible price of %d $. Our offer ends on %s. Use code
        OFFER%d to book your trip. Enjoy these holidays that you deserve so much!""" % (traveler_name, traveler_surname, offer_description, destinations, trip_cost, end_date, offer_id),)
        results.append(message)
    return results
