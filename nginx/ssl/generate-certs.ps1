# Script PowerShell pour generer des certificats SSL auto-signes
# Pour l'environnement de developpement

Write-Host "Generation des certificats SSL pour Nginx..." -ForegroundColor Green

# Verifier si OpenSSL est disponible
try {
    $opensslVersion = & openssl version 2>$null
    Write-Host "OpenSSL trouve: $opensslVersion" -ForegroundColor Green
    $useOpenSSL = $true
} catch {
    Write-Host "OpenSSL non trouve. Utilisation des outils Windows..." -ForegroundColor Yellow
    $useOpenSSL = $false
}

if ($useOpenSSL) {
    # Creer un fichier de configuration
    $configContent = @"
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=FR
ST=France
L=Paris
O=E-commerce Dev
OU=IT Department
CN=localhost

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
IP.2 = ::1
"@

    $configContent | Out-File -FilePath "nginx/ssl/cert.conf" -Encoding UTF8

    # Generer la cle privee
    & openssl genrsa -out "nginx/ssl/key.pem" 2048

    # Generer le certificat
    & openssl req -new -x509 -key "nginx/ssl/key.pem" -out "nginx/ssl/cert.pem" -days 365 -config "nginx/ssl/cert.conf" -extensions v3_req

    Write-Host "Certificats SSL generes avec OpenSSL!" -ForegroundColor Green
} else {
    # Alternative: utiliser les outils Windows integres
    Write-Host "Generation du certificat avec les outils Windows..." -ForegroundColor Yellow
    
    # Generer la cle privee et le certificat avec PowerShell
    $cert = New-SelfSignedCertificate -DnsName "localhost", "*.localhost" -CertStoreLocation "cert:\LocalMachine\My" -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(1)
    
    # Exporter le certificat en format PEM
    $certPath = "cert:\LocalMachine\My\$($cert.Thumbprint)"
    $certPem = [System.Convert]::ToBase64String($cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)) -replace ".{64}", "`$&`n"
    $certPem = "-----BEGIN CERTIFICATE-----`n$certPem`n-----END CERTIFICATE-----"
    $certPem | Out-File -FilePath "nginx/ssl/cert.pem" -Encoding ASCII
    
    # Exporter la cle privee
    $keyBytes = $cert.PrivateKey.Export([System.Security.Cryptography.CngKeyBlobFormat]::Pkcs8PrivateBlob)
    $keyPem = [System.Convert]::ToBase64String($keyBytes) -replace ".{64}", "`$&`n"
    $keyPem = "-----BEGIN PRIVATE KEY-----`n$keyPem`n-----END PRIVATE KEY-----"
    $keyPem | Out-File -FilePath "nginx/ssl/key.pem" -Encoding ASCII
    
    Write-Host "Certificats generes avec les outils Windows" -ForegroundColor Green
}

Write-Host "Certificat: nginx/ssl/cert.pem" -ForegroundColor Cyan
Write-Host "Cle privee: nginx/ssl/key.pem" -ForegroundColor Cyan
Write-Host "Ces certificats sont auto-signes et ne doivent etre utilises qu'en developpement" -ForegroundColor Yellow