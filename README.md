# clamportal - reverse engineerad api för skolportalen och skola24 :)

clamportal är ett python library för att komma åt uppsala skolportal (+ skola24)

jag gjorde detta för min [schemavisare](https://github.com/ingobeans/schemavisare-skola24-skolportalen)

clam.py innehåller själva library:t, medans main.py är exempelanvändning

## authmechs

clamportal har två authmechs, en för "Elever och lärare på skolan" (tillgängliga via Authmechs.AT_SCHOOL), samt "Elever och lärare (Prova gärna!)" (tillgänglig via Authmechs.MICROSOFT).

Authmechs.MICROSOFT använder selenium, medan Authmechs.AT_SCHOOL endast använder requests för att simulera en inloggning.