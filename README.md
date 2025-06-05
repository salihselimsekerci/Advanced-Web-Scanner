# Advanced-Web-Scanner
Web Zafiyet Tarayıcısı (Advanced Web Vulnerability Scanner)

Bu proje, temel ve orta düzeyde web uygulama güvenlik açıklarını tespit etmek için geliştirilmiş bir Python tabanlı tarayıcıdır. Eğitim, güvenlik testleri ve araştırma amaçlı kullanılmak üzere hazırlanmıştır.

🚀 Özellikler

🔐 HTTP güvenlik header kontrolü (CSP, X-Frame-Options, X-XSS-Protection)

🧪 XSS (Cross-site Scripting) form taraması ve test payload gönderimi

🕳️ Basit SQL Injection (SQLi) testleri (GET parametreleri ile)

📄 HTML formları analiz ederek otomatik veri gönderimi

🧰 Komut satırı üzerinden kullanım kolaylığı

⚙️ Kurulum

pip install requests beautifulsoup4

🕹️ Kullanım

python web_vuln_scanner.py https://hedefsite.com

Örnek çıktı:

[+] Header güvenlik denetimi başlıyor...
  [+] X-Frame-Options: SAMEORIGIN
  [!] Eksik header: Content-Security-Policy

[+] XSS taraması başlıyor...
[!] XSS bulundu: https://hedefsite.com -> <script>alert(1)</script>

[+] SQL Injection taraması başlıyor...
[!] SQL Injection bulundu: https://hedefsite.com?id=' OR '1'='1

📌 Notlar

Bu araç sadece yasal yetkiye sahip olduğunuz sitelerde kullanılmalıdır.

Herhangi bir kötüye kullanım geliştirici sorumluluğunda değildir.

Pentest eğitimi, siber güvenlik çalışmaları ve sistem güvenliği farkındalığı için geliştirilmiştir.

📄 Lisans

MIT Lisansı altında sunulmaktadır.

🔍 Herhangi bir öneriniz veya katkı talebiniz varsa, pull request göndermekten çekinmeyin!

