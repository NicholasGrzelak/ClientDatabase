CREATE TABLE sales(
    invoicenumber number primary key,
    clientnumber number,
    manufacturer text,
    model text,
    type text,
    Lserialnum number,
    Rserialnum number,
    dispensedate date,
    invoicepaid boolean,
    paymentdate date,
    paymentamount number,
    status text,
    quantity number,
    msrp text
);