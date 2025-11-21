Καρτερης Γιωργος
Κολοκουρας Αποστολος


#1
SELECT distinct e.name , e.surname
FROM employees e, travel_guide tg,travel_guide_has_languages tghl, guided_tour gt, tourist_attraction ta, destination d
WHERE e.employees_AM = tg.travel_guide_employee_AM
AND tg.travel_guide_employee_AM = tghl.travel_guide_employee_AM
AND tghl.travel_guide_employee_AM = gt.travel_guide_employee_AM
AND ta.tourist_attraction_id = gt.tourist_attraction_id
AND d.destination_id = ta.destination_destination_id
AND d.country = "GERMANY"
ORDER BY e.name;


------------------------------------------------

#2
SELECT distinct travel_guide_employee_AM  AS travel_guide_id, count(*) AS number_of_guided_tours
FROM guided_tour gt , trip_package tp
WHERE tp.trip_package_id = gt.trip_package_id
AND (tp.trip_start >= '2019-01-01' AND tp.trip_end < '2020-01-01')
GROUP BY travel_guide_employee_AM
HAVING Count(*) > 3;

--------------------------------------------------
#3
SELECT distinct e.travel_agency_branch_travel_agency_branch_id AS travel_agency_brunch_id, COUNT(*) AS number_of_travel_guides
FROM employees e
WHERE e.travel_agency_branch_travel_agency_branch_id IN(
    SELECT tab.travel_agency_branch_id
    FROM travel_agency_branch tab
)
GROUP BY e.travel_agency_branch_travel_agency_branch_id;

#4
SELECT p.trip_package_trip_package_id AS trip_package_id, COUNT(p.trip_package_trip_package_id) AS number_of_reservations
FROM trip_package_has_destination p , reservation r , destination d , trip_package tp
WHERE p.trip_package_trip_package_id = r.offer_trip_package_id
AND tp.trip_start >= '2021-01-01' AND tp.trip_end < '2022-01-01'
AND tp.trip_package_id = r.offer_trip_package_id
AND d.name = 'Paris'
AND d.destination_id = p.destination_destination_id
GROUP BY p.trip_package_trip_package_id
ORDER BY trip_package_trip_package_id;


----------------------------------------------------
#5
SELECT e.name , e.surname
FROM guided_tour gt, employees e
WHERE gt.travel_guide_employee_AM = e.employees_AM
GROUP BY gt.travel_guide_employee_AM
HAVING COUNT(DISTINCT gt.travel_guide_language_id) = 1;


----------------------------------------------------
#6
SELECT 'yes' AS answer
FROM offer o
WHERE NOT EXISTS (
    SELECT r.offer_id
    FROM reservation r
    WHERE r.offer_id = o.offer_id
)
UNION
SELECT 'no' AS solution
FROM offer o
WHERE EXISTS (
    SELECT r.offer_id
    FROM reservation r
    WHERE r.offer_id = o.offer_id
);

----------------------------------------------------

#7
SELECT t.name , t.surname
FROM traveler t
WHERE t.gender = 'male' 
AND t.age > 2040
AND t.traveler_id IN (SELECT Customer_id 
					FROM reservation
					GROUP BY Customer_id
					HAVING COUNT(DISTINCT offer_trip_package_id) > 3);

#8
SELECT e.employees_AM AS travel_guide_id, e.name, e.surname, COUNT(ta.tourist_attraction_id) AS num_attractions
FROM employees e, tourist_attraction ta, guided_tour gt, travel_guide_has_languages t
WHERE e.employees_AM = t.travel_guide_employee_AM 
AND t.languages_id IN (SELECT languages_id FROM languages WHERE name = 'English')
AND ta.tourist_attraction_id = gt.tourist_attraction_id
AND t.travel_guide_employee_AM = gt.travel_guide_employee_AM
AND t.languages_id = gt.travel_guide_language_id
GROUP BY e.employees_AM, e.name, e.surname;


----------------------------------------------------

#9
SELECT d.country
FROM trip_package_has_destination tpd , destination d
WHERE tpd.destination_destination_id = d.destination_id
GROUP BY destination_destination_id
HAVING COUNT(*) >= ALL (
	SELECT COUNT(*)
	FROM trip_package_has_destination
	GROUP BY destination_destination_id);


----------------------------------------------------

#10
SELECT tp.trip_package_id
FROM trip_package tp, trip_package_has_destination thd, destination d
WHERE tp.trip_package_id = thd.trip_package_trip_package_id
AND thd.destination_destination_id = d.destination_id
AND d.country = 'Ireland'
GROUP BY tp.trip_package_id
HAVING COUNT(*) = (
	SELECT COUNT(*)
	FROM destination d
	WHERE d.country = 'Ireland');

----------------------------------------------------