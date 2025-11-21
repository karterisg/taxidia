# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

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

    return [("cost_per_person","max_num_participants", "reservations", "driver", "guide", "trip_start", "trip_end"),]


def findRevenue(x):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    return [("travel_agency_branch_id", "total_num_reservations", "total_income", "total_num_employees", "total_salary"),]

def bestClient(x):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
    
    return [("first_name", "last_name", "total_countries_visited", "total_cities_visited", "list_of_attractions"),]
    

def giveAway(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    traveler_query = f"SELECT traveler_id, name, surname FROM traveler ORDER BY RANDOM() LIMIT {N}"
    selected_travelers = con.cursor(traveler_query)
    
   
    travel_package_query = "SELECT trip_package_id, cost_per_person, package_cost_category_id FROM trip_package"
    travel_packages = con.cursor(travel_package_query)
    
   
    for traveler in selected_travelers:
        traveler_id = traveler['traveler_id']
        name = traveler['name']
        surname = traveler['surname']
        
        
        past_booking_query = f"SELECT COUNT(*) AS booking_count FROM reservations WHERE customer_id = {traveler_id}"
        booking_count = con.cursor(past_booking_query)[0]['booking_count']
        
        
        filtered_packages = [package for package in travel_packages if package['trip_package_id'] not in past_bookings]
        
       
        selected_package = random.choice(filtered_packages)
        
       
        if booking_count > 1:
            cost = selected_package['cost_per_person'] * 0.75
            offer_info_category = 'group'
        else:
            cost = selected_package['cost_per_person']
            offer_info_category = 'full-price'
        
       
        offer_start = '2023-06-01'
        offer_end = '2023-06-30'
        
      
        insert_offer_query = f"INSERT INTO offers (offer_id, offer_start, offer_end, cost, description, trip_package_id, offer_info_category) VALUES ('{promo_code}', '{offer_start}', '{offer_end}', {cost}, '{selected_package['description']}', {selected_package['trip_package_id']}, '{offer_info_category}')"
        execute_query(insert_offer_query)
        
       
    
    

    return [("string"),]
    

