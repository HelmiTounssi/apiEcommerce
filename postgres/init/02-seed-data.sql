-- Données de test pour l'application E-commerce
-- Créé le 18/09/2025

-- Utiliser le schéma ecommerce
SET search_path TO ecommerce, public;

-- Insérer des utilisateurs de test
INSERT INTO utilisateurs (email, mot_de_passe, nom, role, date_creation) VALUES
('admin@ecommerce.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'Admin E-commerce', 'admin', NOW()),
('client1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'Jean Dupont', 'client', NOW()),
('client2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'Marie Martin', 'client', NOW())
ON CONFLICT (email) DO NOTHING;

-- Insérer des produits de test
INSERT INTO produits (nom, description, categorie, prix, quantite_stock, image_url, date_creation) VALUES
('Laptop Gaming Pro', 'Ordinateur portable gaming haute performance avec RTX 4070', 'Informatique', 1299.99, 15, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400', NOW()),
('Smartphone Premium', 'Smartphone dernier cri avec caméra 108MP', 'Téléphonie', 899.99, 25, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400', NOW()),
('Casque Audio Pro', 'Casque audio professionnel avec réduction de bruit', 'Audio', 299.99, 30, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', NOW()),
('Tablette Graphique', 'Tablette graphique pour créateurs numériques', 'Informatique', 599.99, 12, 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=400', NOW()),
('Montre Connectée', 'Montre connectée avec suivi santé avancé', 'Wearables', 199.99, 40, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400', NOW()),
('Écouteurs Sans Fil', 'Écouteurs sans fil avec charge rapide', 'Audio', 149.99, 50, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', NOW())
ON CONFLICT DO NOTHING;

-- Insérer des commandes de test
INSERT INTO commandes (utilisateur_id, date_commande, adresse_livraison, statut) VALUES
(2, NOW() - INTERVAL '5 days', '123 Rue de la Paix, 75001 Paris', 'expediee'),
(3, NOW() - INTERVAL '3 days', '456 Avenue des Champs, 69000 Lyon', 'validee'),
(2, NOW() - INTERVAL '1 day', '789 Boulevard Saint-Germain, 13000 Marseille', 'en_attente')
ON CONFLICT DO NOTHING;

-- Insérer des lignes de commande
INSERT INTO lignes_commande (commande_id, produit_id, quantite, prix_unitaire) VALUES
(1, 1, 1, 1299.99),
(2, 2, 1, 899.99),
(3, 3, 1, 299.99)
ON CONFLICT DO NOTHING;

-- Mettre à jour les séquences
SELECT setval('utilisateurs_id_seq', (SELECT MAX(id) FROM utilisateurs));
SELECT setval('produits_id_seq', (SELECT MAX(id) FROM produits));
SELECT setval('commandes_id_seq', (SELECT MAX(id) FROM commandes));
SELECT setval('lignes_commande_id_seq', (SELECT MAX(id) FROM lignes_commande));

-- Commentaires
COMMENT ON TABLE utilisateurs IS 'Table des utilisateurs de l''application';
COMMENT ON TABLE produits IS 'Table des produits du catalogue';
COMMENT ON TABLE commandes IS 'Table des commandes clients';
COMMENT ON TABLE lignes_commande IS 'Table des lignes de commande';
