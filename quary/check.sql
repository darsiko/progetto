alter table product
add constraint check_1 check(amount >= 0);

alter table product
add constraint check_2 check(price > 0);

alter table review
add constraint check_3 check(score >=1 and score <=5);