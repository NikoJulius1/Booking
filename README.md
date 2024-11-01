# Booking API
## Projektoversigt
Denne Booking API er en Flask-baseret applikation til at administrere hotelværelsesbookinger. API’en gør det muligt for brugere at:

## Liste alle bookinger
- Oprette en ny booking med tilgængelighedstjek
- Eksportere bookingdata som CSV
Integrere med en faktureringsservice for at håndtere omkostninger ved bookinger
API’en sikrer, at værelser er ledige inden en booking bekræftes, for at undgå overlap i reservationer.

## Funktioner
Liste over Bookinger: Hent en liste over alle bookinger i JSON-format.
Opret Booking: Tilføj en ny booking, hvis værelset er tilgængeligt, og send bookingdetaljer til faktureringsservicen.

Tjek Tilgængelighed: Bekræfter værelsets tilgængelighed baseret på datoer.
Eksporter Bookinger i CSV: Eksporter bookingsdata i CSV-format til ekstern behandling.

## Endpoints
1. GET /bookings
Beskrivelse: Henter en liste over alle bookinger.
Respons: Returnerer en JSON-array med bookingoplysninger.
2. POST /bookings
Beskrivelse: Opretter en ny booking, hvis værelset er tilgængeligt.

**Responskoder:**

201 Created: Booking blev oprettet.
409 Conflict: Værelset er ikke tilgængeligt.
400 Bad Request: Mangler nødvendige felter.
Integration med Faktureringsservice: Ved en succesfuld booking sendes en notifikation til faktureringsservicen med bookingdetaljer som room_type, checkin, og checkout.

3. GET /bookings/export/csv
Beskrivelse: Eksporterer alle bookingsdata i CSV-format.
Respons: En downloadbar CSV-fil med bookingsdata.

## Vigtige Komponenter
1. Databaseforbindelse
Funktion: get_db_connection()
Formål: Styrer forbindelsen til SQLite-databasen reservation_database.db, hvor bookingsdata gemmes.

2. Notifikation til Faktureringsservice
Funktion: notify_billing_service(booking_id, room_type, checkin, checkout)
Formål: Sender en POST-forespørgsel til faktureringsservicen (http://billing-service:5002/bills/update/{booking_id}) for at opdatere faktureringen ved en ny booking.

Data der Sendes: room_type, checkin, og checkout