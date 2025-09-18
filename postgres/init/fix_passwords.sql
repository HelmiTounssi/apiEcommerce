-- Script pour corriger les mots de passe
UPDATE utilisateurs 
SET mot_de_passe = 'pbkdf2:sha256:600000$LS08ugnMAHLdwCFf$c55a4caf2042d04c00385d34fbb8f9c1bbfff378ce3619acd3d402ad8ba637a0' 
WHERE email IN ('admin@ecommerce.com', 'client1@example.com', 'client2@example.com');
