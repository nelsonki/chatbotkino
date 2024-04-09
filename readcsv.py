import csv
import urllib.request
import io

def read_csv_file(document_premios, miSerial=None, miSorteo=None):
    print(document_premios)
    print(miSerial)
    print(miSorteo)
    premios = []
    with urllib.request.urlopen(document_premios) as csvfile:
        csvfile = io.StringIO(csvfile.read().decode('utf-8'))
        rows = csvfile.read().split('\n')
        for row in rows:
            if row:
                fields = row.split('*')
                print(fields)
                premios.append({
                   'sorteo': fields[0].strip("0"),
                   'serial': fields[1].strip("0"),
                    'categoria': fields[3],
                    'monto': fields[5], 
                })
                print(premios)
    if miSerial:
        output='' 
        arr = miSorteo.split('-')
        sorteoViene =arr[1]
        for premio in premios:
            if premio['serial'] == miSerial.strip("0") and premio['sorteo']== sorteoViene.strip("0"):
                print(premio)
                output += (f"Sorteo: {premio['sorteo']}, Categoría: {premio['categoria']}, Monto: {premio['monto']}, Serial: {premio['serial']}\n")
                output += ("¡Felicitaciones, gracias por confiar en el Kino Táchira!")
        if(output):     
            return output
        else:
            return (f"No existe ningun premio con el serial:  {miSerial}")
 
