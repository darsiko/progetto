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


CREATE OR REPLACE FUNCTION check_unique_user()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF EXISTS (SELECT 1 FROM "user" WHERE name = NEW.name) THEN
            RAISE EXCEPTION 'Username % already exists', NEW.name;
        END IF;

        IF EXISTS (SELECT 1 FROM "user" WHERE email = NEW.email) THEN
            RAISE EXCEPTION 'Email % already exists', NEW.email;
        END IF;

    ELSIF TG_OP = 'UPDATE' THEN
        IF EXISTS (SELECT 1 FROM "user" WHERE name = NEW.name AND id != OLD.id) THEN
            RAISE EXCEPTION 'Username % already exists', NEW.name;
        END IF;

        IF EXISTS (SELECT 1 FROM "user" WHERE email = NEW.email AND id != OLD.id) THEN
            RAISE EXCEPTION 'Email % already exists', NEW.email;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_insert_or_update_user
BEFORE INSERT OR UPDATE
ON "user"
FOR EACH ROW
EXECUTE FUNCTION check_unique_user();








