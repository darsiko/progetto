alter table product
add constraint check_1 check(amount >= 0);

alter table product
add constraint check_2 check(price > 0);

alter table review
add constraint check_3 check(score >=1 and score <=5);

alter table "order"
add constraint check_4 check(state = 'ordinato' or state = 'spedito' or state = 'in transito' or state = 'consegnato');

alter table "user"
add constraint check_5 check(role = 'buyer' or role = 'seller' or role = 'admin');