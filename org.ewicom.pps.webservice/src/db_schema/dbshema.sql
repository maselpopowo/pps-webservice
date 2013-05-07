CREATE FUNCTION merge_unit(unittextid text, unitlink text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
curtime timestamp := now();
BEGIN
    LOOP
        -- first try to update the key
        UPDATE unit SET unit_link = unitlink, unit_lastmodified = curtime WHERE unit_textid = unittextid;
        IF found THEN
            RETURN;
        END IF;
        -- not there, so try to insert the key
        -- if someone else inserts the same key concurrently,
        -- we could get a unique-key failure
        BEGIN
            INSERT INTO unit(unit_textid,unit_link) VALUES (unittextid,unitlink);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END;
$$;

CREATE TABLE details (
    details_id integer NOT NULL,
    unit_id integer NOT NULL,
    unit_name character varying(100) NOT NULL,
    unit_sname character varying(100) NOT NULL,
    unit_latitude character varying(100) NOT NULL,
    unit_longitude character varying(100) NOT NULL,
    unit_street character varying(100) NOT NULL,
    unit_postcode character varying(6) NOT NULL,
    unit_city character varying(100) NOT NULL,
    unit_phone character varying(100) NOT NULL,
    unit_email character varying(100) NOT NULL,
    unit_img character varying(255) NOT NULL,
    unit_simg character varying(255) NOT NULL,
    unit_description text NOT NULL
);

CREATE SEQUENCE details_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000
    CACHE 1
    CYCLE;

ALTER SEQUENCE details_details_id_seq OWNED BY details.details_id;

CREATE TABLE leader (
    unit_id integer,
    leader_position character varying(250) NOT NULL,
    leader_name character varying(250) NOT NULL,
    leader_phone character varying(250) NOT NULL,
    leader_email character varying(100),
    leader_id integer NOT NULL
);

CREATE SEQUENCE leader_leader_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000
    CACHE 1
    CYCLE;

ALTER SEQUENCE leader_leader_id_seq OWNED BY leader.leader_id;

CREATE TABLE phone (
    phone_id integer NOT NULL,
    phone_name character varying(100) NOT NULL,
    phone_number character varying(250) NOT NULL,
    unit_id integer
);

CREATE SEQUENCE phone_phone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000
    CACHE 1
    CYCLE;

ALTER SEQUENCE phone_phone_id_seq OWNED BY phone.phone_id;

CREATE TABLE unit (
    unit_id integer NOT NULL,
    unit_textid character varying(100) NOT NULL,
    unit_link character varying(250) NOT NULL,
    unit_lastmodified timestamp with time zone DEFAULT now() NOT NULL
);

CREATE SEQUENCE unit_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE unit_unit_id_seq OWNED BY unit.unit_id;

ALTER TABLE ONLY details ALTER COLUMN details_id SET DEFAULT nextval('details_details_id_seq'::regclass);

ALTER TABLE ONLY leader ALTER COLUMN leader_id SET DEFAULT nextval('leader_leader_id_seq'::regclass);

ALTER TABLE ONLY phone ALTER COLUMN phone_id SET DEFAULT nextval('phone_phone_id_seq'::regclass);

ALTER TABLE ONLY unit ALTER COLUMN unit_id SET DEFAULT nextval('unit_unit_id_seq'::regclass);

ALTER TABLE ONLY details
    ADD CONSTRAINT details_pk PRIMARY KEY (details_id);

ALTER TABLE ONLY details
    ADD CONSTRAINT details_unit_id_unique UNIQUE (unit_id);

ALTER TABLE ONLY leader
    ADD CONSTRAINT leader_pk PRIMARY KEY (leader_id);

ALTER TABLE ONLY phone
    ADD CONSTRAINT phone_pk PRIMARY KEY (phone_id);

ALTER TABLE ONLY unit
    ADD CONSTRAINT unit_pk PRIMARY KEY (unit_id);

ALTER TABLE ONLY unit
    ADD CONSTRAINT unit_unit_textid_unique UNIQUE (unit_textid);

ALTER TABLE ONLY details
    ADD CONSTRAINT details_unit_fk FOREIGN KEY (unit_id) REFERENCES unit(unit_id) ON DELETE CASCADE;

ALTER TABLE ONLY leader
    ADD CONSTRAINT leader_unit_fk FOREIGN KEY (unit_id) REFERENCES unit(unit_id) ON DELETE CASCADE;

ALTER TABLE ONLY phone
    ADD CONSTRAINT phone_unit_fk FOREIGN KEY (unit_id) REFERENCES unit(unit_id) ON DELETE CASCADE;
