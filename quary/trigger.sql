CREATE OR REPLACE FUNCTION update_product_amount() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT amount FROM Product WHERE id = NEW.product_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Quantità insufficiente per il prodotto %', NEW.product_id;
    END IF;

    UPDATE Product
    SET amount = amount - NEW.quantity
    WHERE id = NEW.product_id;

    DELETE FROM cart_item
    WHERE product_id IN
    (SELECT product_id FROM "order");

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER after_order_insert
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION update_product_amount();


CREATE OR REPLACE FUNCTION delete_items() RETURNS TRIGGER AS $$
BEGIN
    UPDATE cart
    SET last_modified = CURRENT_DATE
    WHERE id = OLD.cart_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER after_cart_item_delete
AFTER DELETE ON cart_item
FOR EACH ROW
EXECUTE FUNCTION delete_items();


