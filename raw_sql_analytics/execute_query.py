import sqlite3
import csv

QUERY_FILE = 'query_7.sql'
CSV_FILE = 'result.csv'

def execute_query(file, params=()):
    with open(file, 'r') as f:
        query = f.read()

    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        cur.execute(query, params)
        results = cur.fetchall()
        columns = [description[0] for description in cur.description]
        print(results)
        return results, columns
        
def save_to_file(data, file_for_save):
    results, columns = data
    with open(file_for_save, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
        
if __name__ == "__main__":
    save_to_file(execute_query(QUERY_FILE, (5, 2)), CSV_FILE)