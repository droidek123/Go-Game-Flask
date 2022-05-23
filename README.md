# Go-Game-Flask

Celem laboratorium jest zapoznanie się ze sposobem tworzenia aplikacji sieciowych udostępniających REST API w języku Python i przy wykorzystaniu frameworku Flask. Samo zadanie polega na zaprojektowaniu i zaimplementowaniu systemu oferującego restowy endpoint, umożliwiającego przeprowadzenie rozgrywki GO w trybie on-line. W trakcie implementacji należy wykorzystać silnik gry z poprzedniego laboratorium (rozmiar planszy pozostaje 9x9).

Stworzone API powinno pozwalać na:

zainicjowanie gry (by było wiadomo, kto z kim gra),
pobrania informacji o bieżącym stanie gry (by dało się wyświetlić planszę oraz pionyna interfejsie klienta),
wykonywanie kolejnych ruchów,
zakończenie gry (z możliwością jej wcześniejszego przerwania).
Powyższą listę wymagań można dowolnie rozszerzać. Można np. dodać opcję gromadzenia i wyświetlania statystych (numer bieżącego ruchu, czas wykonania ruchy, średni czas wykonania ruchu, czas gry itp.) czy też udostępnić możliwość przesyłania komentarzy. Tworzenie rozszerzeń nie jest jednak obowiązkowe.

Aplikacja powinna przechowywać dane dotyczące gry na przynajmniej dwa sposoby: w pamięci lub w pliku (opcjonalnie w bazie danych - przy czym baza danych może działać w pamięci, być przechowywana na dysku w postaci pliku lub być uruchomiona jako osobny serwis). Wyróżnienie różnych sposobów przechowywania danych jest celowe. Chodzi w nim o wykazanie, że szybkość generowania odpowiedzi z serwisu zależy mocno od sposobu jego implementacji. Można przypuszczać, że przechowywanie danych w pamięci operacyjnej będzie skutkować krótkim czasem odpowiedzi, a korzystanie z zasobów dyskowych będzie powodować opóźnienia. Weryfikację tej hipotezy mają umożliwić testy obciążeniowe przewidziane na kolejne zajęcia.

Aplikację należy tak zaimplementować, by dało się ją skonfigurować (albo przez pliki konfiguracyjne, albo poprzez atrybuty podane w linii komend lub w zmiennych środowiskowych, czy też przez uruchomienie odpowiedniej restowej metody konfigurującej serwis).

Konwencja nazewnicza projektu na gitlabie:

nazwa projektu INazwisko######_GO_FLASK
