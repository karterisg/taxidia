# Travel Agency App

Αυτή η Python εφαρμογή συνδέεται με μια MySQL βάση δεδομένων ταξιδιών (`taxidia.sql`) και παρέχει λειτουργίες για αναζήτηση ταξιδιών, υπολογισμό εσόδων, εύρεση καλύτερων πελατών και δημιουργία προσφορών.

## Απαιτήσεις

- Python 3.8 ή νεότερη  
- MySQL Server  
- Python βιβλιοθήκες:
```bash
pip install pymysql

Ρύθμιση

Εισάγετε τη βάση δεδομένων taxidia.sql στον MySQL server:
mysql -u <username> -p <database_name> < Taxidia.sql

mysql_host = "localhost"
mysql_user = "root"
mysql_passwd = "password"
mysql_schema = "Taxidia"

python app.py
