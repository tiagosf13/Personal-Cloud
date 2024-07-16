DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users') THEN
        -- Table: public.users -- Table for storing user data
        CREATE TABLE public.users (
            id SERIAL NOT NULL,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            admin BOOLEAN NOT NULL,
            PRIMARY KEY (id)
        );
    END IF;
END $$;

