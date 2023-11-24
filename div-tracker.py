import pandas as pd
from tabulate import tabulate
import sqlite3
import yfinance as yf

def add_dividend():
    stock_symbol = input("Ticker Symbol: ")

    try:
        stock = yf.Ticker(stock_symbol)
        dividend_data = stock.dividends
        latest_dividend = dividend_data.tail(1)

        if latest_dividend.empty():
            print("Keine Dividendendaten verfügbar!")
            return
        
        amount = float(latest_dividend.iloc[0])
        date = str(latest_dividend.index[0].date())

        try:
            df = pd.read_sql("SELECT * FROM dividends", conn)
        except pd.io.sql.DatabaseError:
            df = pd.DataFrame(columns=["Symbol","Betrag","Datum"])

        new_row = {"Symbol": stock_symbol, "Betrag": amount, "Datum": date}
        df = df.append(new_row, ignore_index = True)

        df.to_sql("dividends", conn, index=False, if_exists="replace")
        print("Dividende erfolgreich hinzugefügt!")

    except Exception as e:
        print(f"Fehler beim Abrufen der Dividendeninformation: {e}")

def show_dividends():
    try:
        df = pd.read_sql("SELECT * FROM dividends", conn)
        if not df.empty:
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("Keine Dividenden vorhanden")
    except pd.io.sql.DatabaseError:
        print("Keine Dividenden vorhanden")

def main():
    while True:
        print("\nDividenden Tracker")
        print("1. Dividende hinzufügen")
        print("2. Alle Dividenden anzeigen")
        print("3. Beenden")

        choice = input("Wähle eine Option (1/2/3): ")

        if choice == 1:
            add_dividend()
        if choice == 2:
            show_dividends()
        elif choice == 3:
            break
        else:
            print("Ungültige Eingabe. Versuche es bitte erneut!")

if __name__ == "__main__":

    conn = sqlite3.connect("dividends.db")

    try:
        pd.read_sql("SELECT * FROM dividends", conn)
    except pd.io.sql.DatabaseError:
        pd.DataFrame(columns=["Symbol", "Betrag", "Datum"]).to_sql("dividends", conn, index=False)

    main()

    conn.close()