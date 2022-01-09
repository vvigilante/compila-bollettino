# Compila bollettino da file excel
Compila un bollettino postale per ciascuna riga di un file excel

## Uso
```
.\main.py test.xlsx grafica.pdf
```
Oppure trascinare file excel e grafica direttamente sull'icona dell'eseguibile. Verrà generato un file `stampa.pdf`

## Compilazione
Inizializzare con:
```
python -m pip install pyinstaller virtualenv
python -m venv myenv
.\myenv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

Per creare l'eseguibile, eseguire `make.bat`
