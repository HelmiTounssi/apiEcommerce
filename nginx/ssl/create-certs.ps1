# Script pour generer les certificats SSL
$opensslPath = "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

if (Test-Path $opensslPath) {
    Write-Host "OpenSSL trouve: $opensslPath" -ForegroundColor Green
    
    # Generer la cle privee et le certificat
    & $opensslPath req -x509 -newkey rsa:2048 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=FR/ST=France/L=Paris/O=E-commerce Dev/CN=localhost"
    
    Write-Host "Certificats SSL generes avec succes!" -ForegroundColor Green
    Write-Host "Certificat: nginx/ssl/cert.pem" -ForegroundColor Cyan
    Write-Host "Cle privee: nginx/ssl/key.pem" -ForegroundColor Cyan
} else {
    Write-Host "OpenSSL non trouve dans $opensslPath" -ForegroundColor Red
    Write-Host "Veuillez installer OpenSSL ou verifier le chemin d'installation" -ForegroundColor Yellow
}
