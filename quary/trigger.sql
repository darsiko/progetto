create or replace function fun_1()
returns trigger as $$
    begin
        update product
        set amount = amount - new.quantity
        where id = new.product_id;
    end;
$$ language plpgsql;

create or replace trigger trig_1
after insert on "order"
for each statement
execute function fun_1();
