TODO: write a Readme

use cases:

parameter:
currency -> gibt alle agencies und deren wechselkurs zur genannten waehrung zum aktuellen datum aus
agency, currency -> gibt den wechselkurs zur genannten waehrung zum aktuellen datum aus von der gewaehlten agentur
currency_from, currency_to -> gibt alle agencies und deren wechselkurs von currency_from zu currency_to aus
agency, currency_from, currency_to -> gibt den wechselkurs von currency_from zu currency_to zum aktuellen datum aus von der gewaehlten agentur
wenn jeweils ein datum parameter uebergeben wird wird der kurs mit dem genannten datum angegeben

eventstorming

events:
    update rates
    get rate
    list rates

refactor the tests  
separate error tests from creational tests
use parametrized and ids where ids and fn name follow this schema:
unit under test name_when_xshould_y
where x is the given detailed testing context and y is the expected result in detail