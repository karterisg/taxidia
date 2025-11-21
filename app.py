import settings
import sys, os, random
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' Use this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema,
        cursorclass=db.cursors.DictCursor  
    )
    return con

def findTrips(x, a, b):
    con = connection()
    cur = con.cursor()
    
    query = f"""
    SELECT tp.cost_per_person, tp.max_num_participants, COUNT(r.reservation_id) AS reservations,
           e1.name AS driver, e2.name AS guide, tp.trip_start, tp.trip_end
    FROM trip_package tp
    LEFT JOIN reservation r ON tp.trip_package_id = r.offer_trip_package_id
    LEFT JOIN employees e1 ON e1.employees_AM = tp.driver_employee_AM
    LEFT JOIN employees e2 ON e2.employees_AM = tp.travel_guide_employee_AM
    WHERE tp.cost_per_person BETWEEN {a} AND {b}
    GROUP BY tp.trip_package_id, e1.name, e2.name
    """
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return [(r['cost_per_person'], r['max_num_participants'], r['reservations'],
             r['driver'], r['guide'], r['trip_start'], r['trip_end']) for r in result]

def findRevenue(x):
    con = connection()
    cur = con.cursor()
    
    query = """
    SELECT e.travel_agency_branch_travel_agency_branch_id AS travel_agency_branch_id,
           COUNT(r.reservation_id) AS total_num_reservations,
           SUM(tp.cost_per_person) AS total_income,
           COUNT(DISTINCT e.employees_AM) AS total_num_employees,
           SUM(e.salary) AS total_salary
    FROM employees e
    LEFT JOIN trip_package tp ON e.employees_AM = tp.travel_guide_employee_AM
    LEFT JOIN reservation r ON tp.trip_package_id = r.offer_trip_package_id
    GROUP BY e.travel_agency_branch_travel_agency_branch_id
    """
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return [(r['travel_agency_branch_id'], r['total_num_reservations'], r['total_income'],
             r['total_num_employees'], r['total_salary']) for r in result]

def bestClient(x):
    con = connection()
    cur = con.cursor()
    
    query = """
    SELECT t.name AS first_name, t.surname AS last_name,
           COUNT(DISTINCT d.country) AS total_countries_visited,
           COUNT(DISTINCT d.name) AS total_cities_visited,
           GROUP_CONCAT(ta.name) AS list_of_attractions
    FROM traveler t
    JOIN reservation r ON t.traveler_id = r.customer_id
    JOIN trip_package tp ON r.offer_trip_package_id = tp.trip_package_id
    JOIN trip_package_has_destination tpd ON tp.trip_package_id = tpd.trip_package_trip_package_id
    JOIN destination d ON tpd.destination_destination_id = d.destination_id
    JOIN guided_tour gt ON tp.travel_guide_employee_AM = gt.travel_guide_employee_AM
    JOIN tourist_attraction ta ON gt.tourist_attraction_id = ta.tourist_attraction_id
    GROUP BY t.traveler_id
    ORDER BY total_countries_visited DESC, total_cities_visited DESC
    LIMIT 1
    """
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    if result:
        r = result[0]
        return [(r['first_name'], r['last_name'], r['total_countries_visited'],
                 r['total_cities_visited'], r['list_of_attractions'])]
    return []

def giveAway(N):
    con = connection()
    cur = con.cursor()
    
    
    cur.execute(f"SELECT traveler_id, name, surname FROM traveler ORDER BY RAND() LIMIT {N}")
    selected_travelers = cur.fetchall()
    
 
    cur.execute("SELECT trip_package_id, cost_per_person, description FROM trip_package")
    travel_packages = cur.fetchall()
    
    results = []
    
    for traveler in selected_travelers:
        traveler_id = traveler['traveler_id']
        
       
        cur.execute(f"SELECT offer_trip_package_id FROM reservation WHERE customer_id = {traveler_id}")
        past_bookings = {r['offer_trip_package_id'] for r in cur.fetchall()}
        
       
        filtered_packages = [p for p in travel_packages if p['trip_package_id'] not in past_bookings]
        if not filtered_packages:
            continue
        
        selected_package = random.choice(filtered_packages)
        
        results.append((traveler['name'], traveler['surname'], selected_package['trip_package_id'], selected_package['cost_per_person']))
    
    con.close()
    return results
