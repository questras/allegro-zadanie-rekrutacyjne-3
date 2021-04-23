# allegro-zadanie-rekrutacyjne-3
Zadanie rekrutacyjne Allegro.

## Jak uruchomić
1. Pobierz repozytorium i wejdź do folderu głównego (tego z run.py).
2. Zainstaluj zależności przy użyciu `pipenv`:
```
pipenv install
```
3. Aktywuj wirtualne środowisko:
```
pipenv shell
```
4. Eksportuj zmienne środowiskowe:
```
export GITHUB_API_TOKEN=your-github-api-token
export FLASK_APP="run.py"
```
gdzie `GITHUB_API_TOKEN` to token do GITHUB API (https://docs.github.com/en/rest).  

Aby włączyć aplikację w trybie debugowania, należy dodatkowo eksportować zmienną:
```
export FLASK_ENV=development
```
5. Włącz aplikację przy użyciu polecenia:
```
flask run
```
