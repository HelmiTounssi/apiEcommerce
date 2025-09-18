-- Initialisation de la base de données PostgreSQL pour E-commerce
-- Créé le 18/09/2025

-- Créer la base de données si elle n'existe pas
-- (La base est déjà créée par les variables d'environnement Docker)

-- Créer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Créer un schéma pour l'application
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Configurer les permissions
GRANT ALL PRIVILEGES ON SCHEMA ecommerce TO ecommerce_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ecommerce TO ecommerce_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ecommerce TO ecommerce_user;

-- Configurer les permissions par défaut
ALTER DEFAULT PRIVILEGES IN SCHEMA ecommerce GRANT ALL ON TABLES TO ecommerce_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ecommerce GRANT ALL ON SEQUENCES TO ecommerce_user;

-- Commentaires
COMMENT ON SCHEMA ecommerce IS 'Schéma principal de l''application e-commerce';
