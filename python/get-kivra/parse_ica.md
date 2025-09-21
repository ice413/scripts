# Fetch from Kivra:

## req:
kör:
```python
python3 -m venv venv
source venv/bin/activate
pip install requests qrcode Pillow weasyprint
```

## The fetchscript:
Uppdatera scriptet föratt passa dina behov, på rad 69:
```python
# Konfiguration
FETCH_RECEIPTS = True  # Sätt till True för att hämta kvitton
FETCH_LETTERS = False    # Sätt till True för att hämta brev
MAX_RECEIPTS = None    # Sätt till ett heltal för att begränsa antalet kvitton som hämtas (None = obegränsat)
MAX_LETTERS = None     # Sätt till ett heltal för att begränsa antalet brev som hämtas (None = obegränsat)

```
Kör sedan:
```sh
python ./fetch-kivra.py
```

Kvittona kommer att sparas i $scriptdir/<födelsenummer>/Receipts
där finns dom som både .pdf och som .json

# The parse-script:
Uppdatera PATH på rad 5
Kör sedan:
```sh
python ./parse-ica.py
```

## SQL:
Nu har du en .sql som du kan importrea i valfri databas.
### Skapa en DB:
```sql
CREATE DATABASE ica_db;
```

```sql
CREATE TABLE receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME,
    store VARCHAR(255),
    total VARCHAR(32),
    product VARCHAR(255),
    price VARCHAR(32),
    quantity INT,
    price_per_item VARCHAR(32) DEFAULT '0',
    price_per_kilo VARCHAR(32) DEFAULT '0'
);
```
exit the database and run this:

```sh
mysql -u <USER> -p ica_db < ./receipts.sql
```
