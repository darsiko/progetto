CREATE OR REPLACE FUNCTION update_product_amount() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT amount FROM Product WHERE id = NEW.product_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Quantità insufficiente per il prodotto %', NEW.product_id;
    END IF;

    UPDATE Product
    SET amount = amount - NEW.quantity
    WHERE id = NEW.product_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_order_insert
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION update_product_amount();

