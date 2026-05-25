# Dashboard Abitudini 📊

> ⚠️ **Progetto in sviluppo** — Il progetto è funzionante nelle sue funzionalità principali, ma è ancora in fase di sviluppo attivo. Potrebbero essere presenti bug o comportamenti inattesi. Il codice viene aggiornato e migliorato progressivamente.

App web per tracciare le proprie abitudini quotidiane (lettura, acqua, allenamento, ecc.), costruita con Django. Permette di registrare il completamento giornaliero, visualizzare i progressi in un grafico e monitorare le streak.

---

## Funzionalità

- **Registrazione e login** — ogni utente ha le proprie abitudini private
- **Dashboard giornaliera** — visualizza le abitudini del giorno selezionato e le segna come completate o da fare
- **Navigazione per data** — puoi consultare o modificare i log di giorni precedenti
- **Grafico settimanale** — mostra la percentuale di completamento degli ultimi 7 giorni (Chart.js)
- **Streak** — conta i giorni consecutivi in cui tutte le abitudini sono state completate al 100%
- **Aggiunta abitudini** — form diretto nella dashboard per aggiungere nuove abitudini
- **Eliminazione abitudini** — rimuove l'abitudine e tutti i log storici collegati

---

## Tecnologie

| Tecnologia | Versione | Utilizzo |
|---|---|---|
| Python | 3.12 | Linguaggio base |
| Django | 6.0.5 | Framework web |
| SQLite | — | Database (sviluppo) |
| Chart.js | CDN | Grafico settimanale |
| Pico CSS | CDN | Stile UI |
| python-decouple | 3.8 | Gestione variabili d'ambiente |

---

## Struttura del progetto

```
dashboard-abitudini/
├── manage.py
├── requirements.txt
├── .env                          ← NON incluso nel repo (vedi sotto)
├── .gitignore
│
├── dashboard_habits/             ← configurazione progetto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── tracker/                      ← app principale
    ├── models.py                 ← Abitudine, LogAbitudine
    ├── views.py                  ← dashboard, toggle_abitudine, elimina_abitudine
    ├── views_auth.py             ← registrazione
    ├── urls.py                   ← rotte principali
    ├── urls_auth.py              ← rotta registrazione
    ├── forms.py                  ← AbitudineForm
    ├── admin.py                  ← configurazione pannello admin
    ├── migrations/
    └── templates/
        ├── tracker/
        │   └── dashboard.html
        └── registration/
            ├── login.html
            └── register.html
```

---

## Modelli

### `Abitudine`
Rappresenta una singola abitudine legata a un utente.

| Campo | Tipo | Note |
|---|---|---|
| `nome` | CharField(50) | Nome dell'abitudine |
| `proprietario` | ForeignKey(User) | Utente proprietario |
| `created_at` | DateTimeField | Data di creazione (automatica) |

### `LogAbitudine`
Rappresenta il log giornaliero di un'abitudine (completata o no).

| Campo | Tipo | Note |
|---|---|---|
| `abitudine` | ForeignKey(Abitudine) | Abitudine collegata |
| `data` | DateField | Giorno del log |
| `completata` | BooleanField | Completata (default: False) |

> Un vincolo `UniqueConstraint` garantisce un solo log per abitudine per giorno.

---

## Installazione

### 1. Clona il repository

```bash
git clone https://github.com/ectorr01/dashboard-abitudini.git
cd dashboard-abitudini
```

### 2. Crea e attiva il virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura il file `.env`

Crea un file `.env` nella cartella radice del progetto (dove si trova `manage.py`):

```
SECRET_KEY=la-tua-chiave-segreta-qui
DEBUG=True
```

Per generare una `SECRET_KEY` valida:

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
>>> exit()
```

> ⚠️ Il file `.env` non viene mai committato su Git perché contiene dati sensibili. Ogni sviluppatore deve crearne uno proprio in locale. Non condividere mai la `SECRET_KEY` pubblicamente.

### 5. Esegui le migrazioni

```bash
python manage.py migrate
```

### 6. (Opzionale) Crea un superuser per l'admin

```bash
python manage.py createsuperuser
```

### 7. Avvia il server

```bash
python manage.py runserver
```

L'app è disponibile su [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Note su `.env` e sicurezza

Il file `.env` contiene variabili d'ambiente sensibili e non deve mai essere incluso nel repository Git. Il `.gitignore` lo esclude già automaticamente.

| Variabile | Descrizione | Esempio |
|---|---|---|
| `SECRET_KEY` | Chiave crittografica di Django | Stringa casuale di 50+ caratteri |
| `DEBUG` | Modalità debug (solo sviluppo) | `True` in locale, `False` in produzione |

In produzione, `DEBUG` deve essere impostato a `False` e `ALLOWED_HOSTS` deve contenere il dominio reale.

---

## Autore

Progetto realizzato come esercizio per imparare Django e Git/GitHub.

## Stato del progetto

🚧 **Work in progress** — Il progetto è caricato su GitHub in uno stato funzionante, ma lo sviluppo è ancora in corso. Alcune funzionalità potrebbero essere incomplete o presentare bug. Il codice verrà revisionato, migliorato e corretto nel tempo.

Se noti qualcosa che non funziona, sentiti libero di aprire una [Issue](https://github.com/ectorr01/dashboard-abitudini/issues) su GitHub.
