# CeneoWebScraperS11

## Struktura opinii w serwisie Ceneo [Ceneo.pl](https://www.ceneo.pl/)

|Składowa|Selektor|Nazwa zmiennej|Typ zmiennej|
|--------|--------|--------------|------------|
|opinia|div.js_product-review|opinion|obj|
|indentyfikator opinii|div.js_product-review["data-entry-id"\]|opinion_id|int|
|autor opinii|span.user-post__author-name|author|str|
|rekomendacja|span.user-post__author-recomendation > em|recommendation|str|
|liczba gwiazdek|span.user-post__score_count|stars|str|
|treść opinii|div.user-post__text|content|str|
|lista zalet|div.review-feature__title--positives ~ div.review-feature__item|pros|list|
|lista wad|div.review-feature__title--negatives ~ div.review-feature__item|cons|list|
|dla ilu osób przydatna|buttton.vote-yes > span|useful|int|
|dla ilu osób nieprzydatna|buttton.vote-no > span|useless|int|
|data wystawienie opinii|span.user-post__published > time:nth-child(1)["datetime"]|publish_date|list|
|data zakupu|span.user-post__published > time:nth-child(2)["datetime"]|purchase_date|list|


## Etapy pracy nad projektem
1. Pobranie id opinii produktu z formy
2. Pobranie do pojedynczych zmiennych składowych pojedynczej opinii
3. Zapisanie wszystkich składowych pojedycznej opinii do słownika
4. Pobranie wszytskich opinii z pojedynczej strony do słowników i zapisanie ich na liście
5. Zapisanie wszystkich opinii z listy do pliku .json
6. Pobranie wszytskich opinii o produkcie i zapisanie ich na liście w postaci słowników
7. Dodanie mozliwości podania numeru produktu przez uzytkownika
8. Optymalizacja kodu
    a. utworzenie funkcji do ekstrakcji elementów strony
    b. utworzenie słownika selektorów
    c. użycie dictionary comprehension do pobrania składowych pojedynczej opinii na podstawie słownika selektorów
9. Analiza pobranych opinii dla konkretnego produktu
    a. wyliczenie podstawowych statystyk 
        - liczba opinii
        - liczba opinii dla których podano zalety
        - liczba opinii dla których podanop wady
        - średnia ocena produktu
    b. udział poszczególnych rekomendacji w ogólnej liczbie opinii
        - udział występowania poszczególnych ocen
10. Zapisanie statystyk do pliku .json
11. Utworzenie wykresów za pomocą biblioteki matplotlib
12. Wyświetlenie statystyk i wykresów
13. Dostęp do wygenerowanych stron produktowych poprzez sekcję 'products'



## Użyte biblioteki
|Biblioteka|Funkcja biblioteki|
|----------|------------------|
|Beautiful Soup|Analiza i parsowanie plików html|
|Flask|Framework aplikacji webowych|
|Jinja2|Silnik szablonów|
|matplotlib|Tworzenie grafów|
|numpy|Obsługa tabel|
|pandas|Analiza i manipulacja danych|
|requests|Obsługa żądań HTTP|
|Markdown|Konwersja plików .md na html|