import csv
import urllib.request
import io

def read_csv_file(document_premios, miSerial=None, miSorteo=None):
    premios = []
    with urllib.request.urlopen(document_premios) as csvfile:
        csvfile = io.StringIO(csvfile.read().decode('utf-8'))
        rows = csvfile.read().split('\n')
        for row in rows:
            if row:
                fields = row.split('*')
                premios.append({
                   'sorteo': int(fields[0]),
                   'serial': int(fields[1]),
                    'categoria': fields[4],
                    'monto': float(fields[5]), 
                })
    if miSerial:
        output='' 
        arr = miSorteo.split('-')
        sorteoViene =arr[1]
        for premio in premios:
            if premio['serial'] == int(miSerial) and premio['sorteo']== int(sorteoViene):
                print(premio)
                output += (f"Sorteo: {premio['sorteo']}, Categoría: {premio['categoria']}, Monto: {premio['monto']}, Serial: {premio['serial']}\n")
        if(output):     
            return output
        else:
            return (f"No existe ningun premio con el serial:  {miSerial}")
 
