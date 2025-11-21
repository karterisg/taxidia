# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys, os
import random
import pymysql as db

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))

def connection():
    """Create a connection to the MySQL database"""
    con = db.connect(
        host=settings.mysql_host,
        user=settings.mysql_user,
        password=settings.mysql_passwd,
        database=settings.mysql_schema,
        cursorclass=db.cursors.DictCursor  # επιστρέφει αποτελέσματα ως dict
    )
    return con

def findTrips(x, a, b):
    con = connection()
    cur = con.cursor()
    query = "SELECT cost_per_person, max_num_participants, driver, guide, trip_start, trip_end FROM trip_package LIMIT 10"
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result

def findRevenue(x):
    con = connection()
    cur = con.cursor()
    query = """
    SELECT travel_agency_branch_id,
           SUM(num_reservations) AS total_num_reservations,
           SUM(total_income) AS total_income,
           COUNT(employee_id) AS total_num_employees,
           SUM(salary) AS total_salary
    FROM travel_agency
    GROUP BY travel_agency_branch_id
    """
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result

def bestClient(x):
    con = connection()
    cur = con.cursor()
    query = """
    SELECT t.first_name, t.last_name,
           COUNT(DISTINCT r.country_id) AS total_countries_visited,
           COUNT(DISTINCT r.city_id) AS total_cities_visited,
           GROUP_CONCAT(a.attraction_name) AS list_of_attractions
    FROM reservations r
    JOIN traveler t ON r.customer_id = t.traveler_id
    JOIN attractions a ON r.attraction_id = a.attraction_id
    GROUP BY t.traveler_id
    ORDER BY total_countries_visited DESC, total_cities_visited DESC
    LIMIT 1
    """
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result

def giveAway(N):
    con = connection()
    cur = con.cursor()

    # Επιλογή τυχαίων ταξιδιωτών
    cur.execute(f"SELECT traveler_id, name, surname FROM traveler ORDER BY RAND() LIMIT {N}")
    selected_travelers = cur.fetchall()

    # Λήψη όλων των ταξιδιωτικών πακέτων
    cur.execute("SELECT trip_package_id, cost_per_person, description FROM trip_package")
    travel_packages = cur.fetchall()

    for traveler in selected_travelers:
        traveler_id = traveler['traveler_id']

        # Πόσες κρατήσεις έχει κάνει ο πελάτης
        cur.execute(f"SELECT trip_package_id FROM reservations WHERE customer_id = {traveler_id}")
        past_bookings = [row['trip_package_id'] for row in cur.fetchall()]

        # Φιλτράρουμε πακέτα που δεν έχει ήδη κάνει κράτηση
        filtered_packages = [p for p in travel_packages if p['trip_package_id'] not in past_bookings]
        if not filtered_packages:
            continue

        selected_package = random.choice(filtered_packages)

        # Υπολογισμός κόστους
        cur.execute(f"SELECT COUNT(*) AS booking_count FROM reservations WHERE customer_id = {traveler_id}")
        booking_count = cur.fetchone()['booking_count']
        cost = selected_package['cost_per_person']
        offer_info_category = 'full-price'
        if booking_count > 1:
            cost *= 0.75
            offer_info_category = 'group'

        offer_start = '2023-06-01'
        offer_end = '2023-06-30'
        promo_code = f"OFFER{traveler_id}{selected_package['trip_package_id']}"

        insert_offer_query = f"""
        INSERT INTO offers (offer_id, offer_start, offer_end, cost, description, trip_package_id, offer_info_category)
        VALUES ('{promo_code}', '{offer_start}', '{offer_end}', {cost}, '{selected_package['description']}', {selected_package['trip_package_id']}, '{offer_info_category}')
        """
        cur.execute(insert_offer_query)
        con.commit()

    con.close()
    return [("Giveaway completed",)]

if __name__ == "__main__":
    print("Trips:", findTrips(None, None, None))
    print("Revenue:", findRevenue(None))
    print("Best Client:", bestClient(None))
    print("GiveAway:", giveAway(3))
