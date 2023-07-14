CREATE TABLE clients(
    clientid number primary key,
    firstname text,
    lastname text,
    email text,
    phonenumber text,
    homeaddress text,
    postalcode text,
    city text,
    province text,
    healthcard text,
    datevisit date,
    datefollowup date,
    hearingtest boolean,
    datetest date,
    notes text,
    status text
);