# allegro-zadanie-rekrutacyjne-3
Zadanie rekrutacyjne do Allegro. Wybrane zadanie nr 3 (Software Engineer).

## Spis Treści
* [Technologie](#technologie)
* [Jak uruchomić](#jak-uruchomić)
    * [Z dockerem](#z-dockerem)
    * [Lokalnie](#lokalnie)
* [Endpointy](#endpointy)
* [Brak Tokena do Github API](#brak-tokena-do-github-api)
* [Propozycje rozszerzenia oraz uwagi do projektu](#propozycje-rozszerzenia-oraz-uwagi-do-projektu)
    * [Propozycje rozszerzenia](#propozycje-rozszerzenia)
    * [Uwagi](#uwagi)

## Technologie
* Python 3
* Flask
* [PyGithub](https://github.com/PyGithub/PyGithub)
* [Github API](https://docs.github.com/en/rest)

## Jak uruchomić

### Z dockerem
1. Pobierz repozytorium i wejdź do folderu głównego (tego z `run.py`).
2. Eksportuj zmienną środowiskową:
```
export GITHUB_API_TOKEN=your-github-api-token
```
gdzie `GITHUB_API_TOKEN` to token do GITHUB API (https://docs.github.com/en/rest).  
**Uwaga**: Możliwe jest, aby [nie podać tokena](#brak-tokena-do-github-api), jednak w przypadku dockera jeśli nie 
poda się tej zmiennej środowiskowej to spowoduje to, że docker-compose przypisze do 
tej zmiennej środowiskowej ""(pusty string), który jest niepoprawnym tokenem.  
3. Uruchom kontener
```
docker-compose up --build -d
```
W przypadku chęci włączenia wersji z debugowaniem należy wykonać komendę
```
docker-compose -f docker-compose-dev.yml up --build -d
```
4. Serwer działa pod adresem `http://0.0.0.0:5000`. Dostępne endpointy są [tutaj](#endpointy) 
5. Aby włączyć testy należy użyć komendy
```
docker-compose exec web python3 -m unittest
```
6. Aby włączyć testy z code coverage, należy użyć komendy
```
docker-compose exec web coverage run --source="." -m unittest
```
Aby odczytać `code coverage` z testów, należy użyć komendy:
```
docker-compose exec web coverage report
```
7. Aby wyłączyć serwer, należy użyć komendy
```
docker-compose down
```

### Lokalnie
1. Pobierz repozytorium i wejdź do folderu głównego (tego z `run.py`).

2. Zainstaluj zależności przy użyciu `pipenv`(https://pypi.org/project/pipenv/):
```
pipenv install
```
W przypadku chęci zainstalowania również bibliotek developerskich (np. tych do code coverage) należy użyć komendy
```
pipenv install --dev
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
Tokenu można nie podawać, więcej informacji [tutaj](#brak-tokena-do-github-api)

Aby włączyć aplikację w trybie debugowania, należy dodatkowo eksportować zmienną:
```
export FLASK_ENV=development
```
5. Włącz aplikację przy użyciu polecenia:
```
flask run
```
6. Serwer działa pod adresem `http://127.0.0.1:5000`. Dostępne endpointy są [tutaj](#endpointy) 
7. Aby włączyć testy należy użyć komendy
```
python3 -m unittest
```
8. Aby włączyć testy z code coverage, należy użyć komendy
```
coverage run --source="." -m unittest
```
Aby odczytać `code coverage` z testów, należy użyć komendy:
```
coverage report
```

## Endpointy
* `/api/v1/github/repositories/<username>`
    * Endpoint do listowania repozytoriów danego użytkownika
    * Dostępna metoda: `GET`
    * `<username>` to nazwa interesującego nas użytkownika
    * Wyniki są stronicowane po 50 wyników. Aby dostać się do konkretnej strony należy wyspecyfikować 
      zmienną `page` (pierwsza strona to `0`, domyślnie zwracana jest pierwsza strona). np:
      `/api/v1/github/repositories/some-username?page=3`
* `/api/v1/github/stars/<username>`
    * Endpoint do zwracania sumy gwiazdek danego użytkownika
    * Dostępna metoda: `GET`
    * `<username>` to nazwa interesującego nas użytkownika

## Brak tokena do Github API
Możliwe jest, aby nie podać tokena do Github API. Jednak wtedy 
(zgodnie ze stanem na dzień edytowania tego `README`) możliwe jest wysłanie tylko
60 zapytań na godzinę do Github API, z którego aplikacja korzysta. 
W przypadku wyczerpania tego limitu, aplikacja będzie wysyłać odpowiedzi z kodem 500.

## Propozycje rozszerzenia oraz uwagi do projektu
### Propozycje rozszerzenia
* Udzielanie informacji na temat innych stron, np. gitlab 
(i wtedy dodać nowe endpointy np.`/api/v1/gitlab/repositories/<username>`)
* Udzielanie innych informacji np. na temat `issues` (i wtedy dodać nowe
endpointy np. `/api/v1/github/issues/<username>`)
* Dodanie `Continuous Integration` np. przy użyciu `Github Actions`
* Cachowanie zapytań: token do Github API ma ograniczoną ilość zapytań w określonym
czasie, dlatego dobrym pomysłem byłoby cachowanie wyników, aby nie wysyłać zbyt
dużo zapytań do Github API. W zależności od potrzeb, unieważnienie danych w cache
odbywałoby się po określonym, ustalonym czasie, po którym ponownie wysyłane
byłoby zapytanie do Github API.
* Limit zapytań: innym pomysłem na problem z limitem zapytań do Github API mógłby być
odpowiedni limit zapytań ustawiony po stronie tej aplikacji. 
### Uwagi
* W przypadku przekroczenia limitu zapytań do API lub błędnego tokena, serwer wysyła
do klienta odpowiedź z kodem 500, jednak serwer w żaden sposób nie komunikuje 
(np. w postaci zapisu do pliku z logami) jaki był powód tego błędu, co może 
spowodować, że serwer będzie zwracał błędy i ciężko będzie stwierdzić dlaczego. 
Niestety nie zdążyłem tego zrobić - byłaby to następna rzecz, którą bym zrobił.

