from fastapi import FastAPI, HTTPException, Header
from database import (
    get_all_events,
    get_event,
    get_event_registrations,
    get_upcoming_events,
    delete_event,
    create_event,
    update_event,
    get_registration,
    create_registration,
    update_registration,
    delete_registration,
    get_capacity,
    get_number_of_registrations
)
from schema import Event, Registration

app = FastAPI(
    title="Tapahtuma API",
    description="API tapahtumien tietojen hakemiseen",
    version="1.0.0"
)

APP_TOKEN = "123"
def check_token(token: str | None):
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Puuttuva token"
        )
    if token != APP_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Väärä token"
        )

@app.post("/testEvent")
def test_event(event: Event):
    return event

@app.post("/testRegistration")
def test_registration(registration: Registration):
    return registration

@app.get("/")
def root():
    return {"Message": "Tapahtuma API toimii"}

@app.get(
    "/events",
    summary="Hakee kaikki tapahtumat",
    description="Palauttaa kaikki tietokantaan tallennetut tapahtumat.",
    response_description="Lista tapahtumista"
)
def get_events():
    return get_all_events()

@app.get(
    "/events/{event_id}",
    summary="Hae yksi tapahtuma",
    description="Palauttaa yhden tapahtuman ID:n perusteella",
    response_description="Tapahtuman tiedot"
)
def get_single_event(event_id: int):
    event = get_event(event_id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löytynyt"
        )
    return event

@app.get(
    "/events/registrations/{event_id}",
    summary="Hae tapahtuman osallistujat",
    description="Palauttaa tietyn tapahtuman osallistujat",
    response_description="Lista osallistujista"
)
def get_registrations(event_id: int):
    event = get_event(event_id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löytynyt"
        )
    return get_event_registrations(event_id)

@app.get(
    "/events/upcoming/{location}",
    summary="Hae lokaation tulevat tapahtumat",
    description="Palauttaa tietyn lokaation tulevat tapahtumat",
    response_description="Lista tulevista tapahtumista"
)
def get_upcoming(location: str):
    events = get_upcoming_events(location)
    if events is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löytynyt"
        )
    return events

@app.delete(
    "/events/{event_id}",
    summary="Poista tapahtuma",
    description="Poistaa tapahtuma IDn perusteella",
    response_description="Tapahtuma poistettu"
)
def delete_existing_event(event_id: int, x_api_token: str | None = Header(default=None)):
    check_token(x_api_token)
    existing_event = get_event(event_id)
    if existing_event is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löytynyt"
        )
    delete_event(event_id)
    return {"message": "Tapahtuma poistettu"}

@app.post(
    "/events",
    summary="Luo uusi tapahtuma",
    response_description="Luodun tapahtuman tiedot"
)
def create_new_event(event: Event):
    event_id = create_event(
        event.name,
        event.description,
        event.location,
        event.date,
        event.capacity,
    )
    return get_event(event_id)

@app.put(
    "/events/{event_id}",
    summary="Muokkaa tapahtumaa",
    response_description="Päivitetty tapahtuma"
)
def update_existing_event(event_id: int, event: Event):
    existing_event = get_event(event_id)
    if existing_event is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löytynyt"
        )
    update_event(
        event_id,
        event.name,
        event.description,
        event.location,
        event.date,
        event.capacity
    )
    updated_event = get_event(event_id)
    return updated_event

@app.post(
    "/events/{event_id}/registrations",
    summary="Lisää uuden ilmoittautumisen",
    response_description="Uuden ilmoittautumisen tiedot"
)
def create_new_registration(registration: Registration, event_id: int):
    existing_event = get_event(event_id)
    if existing_event is None:
        raise HTTPException(
            status_code=404,
            detail="Tapahtumaa ei löydy"
        )

    capacity = get_capacity(event_id)
    if capacity is None:
        raise HTTPException(
            status_code=500,
            detail="Tapahtuman vapaata tilaa ei voida laskea"
        )
    registrations = get_number_of_registrations(event_id)
    have_room = capacity - registrations
    if have_room < 1:
        raise HTTPException(
            status_code=409,
            detail="Tapahtumassa ei ole tilaa"
        )

    registration_id = create_registration(
        event_id,
        registration.name,
        registration.email
    )
    new_registration = get_registration(registration_id)
    return new_registration

@app.put(
     "/registrations/{registration_id}",
     summary="Muokkaa ilmoittaumista",
     response_description="Muokattu ilmoittautuminen"
 )
def update_existing_registration(registration_id: int, name: str, email: str):
    existing_registration = get_registration(registration_id)
    if existing_registration is None:
        raise HTTPException(
            status_code=404,
            detail="Ilmoittautumista ei löydy"
        )
    update_registration(registration_id, name, email)
    registration = get_registration(registration_id)
    return registration

@app.delete(
    "/registrations/{registration_id}",
    summary="Poistaa tietyn ilmoittautumisen",
    response_description="Ilmoittautuminen poistettu"
)
def delete_existing_registration(registration_id: int, x_api_token: str | None = Header(default=None)):
    check_token(x_api_token)
    existing_registration = get_registration(registration_id)
    if existing_registration is None:
        raise HTTPException(
            status_code=404,
            detail="Ilmoittautumista ei löydy"
        )
    delete_registration(registration_id)
    return {"message": "Ilmoittautuminen poistettu"}
