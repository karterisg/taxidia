# ART TOUR Travel Agency - Database Application

Η εφαρμογή διαχειρίζεται ταξιδιωτικά πακέτα, κρατήσεις και προσφορές για μια ταξιδιωτική εταιρεία μέσω MySQL και Python. Υποστηρίζει λειτουργίες όπως εύρεση διαθέσιμων πακέτων ανά υποκατάστημα και ημερομηνίες, υπολογισμό εσόδων και στατιστικών ανά υποκατάστημα, εύρεση του καλύτερου πελάτη με βάση δαπάνες και επισκέψεις και τυχαία επιλογή νικητών για προσφορές (giveaway).

## Απαιτήσεις
##
- Python 3.x  
- MySQL με schema `taxidia`  
- Βιβλιοθήκη `pymysql`  

```bash
pip install pymysql
```

Το αρχείο `settings.py` πρέπει να περιέχει τα στοιχεία σύνδεσης στη βάση δεδομένων:

```python
mysql_host = "localhost"
mysql_user = "username"
mysql_passwd = "password"
mysql_schema = "taxidia"
```

## Εκτέλεση

Εισάγετε το `app.py` στο Python περιβάλλον:

```python
import app
```

Κλήση συναρτήσεων:

**Εύρεση διαθέσιμων πακέτων:**
```python
trips = app.findTrips("B01", "2023-06-01", "2023-06-30")
for t in trips:
    print(t)
```

**Υπολογισμός εσόδων ανά υποκατάστημα:**
```python
revenue = app.findRevenue("DESC")
for r in revenue:
    print(r)
```

**Καλύτερος πελάτης:**
```python
best_client = app.bestClient("Best")
for c in best_client:
    print(c)
```

**Give-away προσφορές:**
```python
winners = app.giveAway(5)
for w in winners:
    print(w)
```

## Σημειώσεις

- Το `giveAway` εξασφαλίζει ότι κάθε νικητής λαμβάνει μοναδικό ταξιδιωτικό πακέτο.  
- Όλες οι συναρτήσεις επιστρέφουν αποτελέσματα ως λίστες από tuples για εύκολη χρήση.  
- Η βάση δεδομένων `taxidia.sql` πρέπει να περιέχει όλα τα απαραίτητα δεδομένα για να λειτουργούν σωστά οι συναρτήσεις.  

## Συγγραφείς

- Κάρτερης Γιώργος  
- Κολοκούρας Απόστολος
