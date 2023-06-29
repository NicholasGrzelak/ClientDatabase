CREATE TABLE sales(
    invoicenumber number primary key,
    clientnumber number,
    manufacturer text,
    model text,
    serialnum number,
    invoicepaid boolean,
    paymentdate date,
    paymentamount number
);