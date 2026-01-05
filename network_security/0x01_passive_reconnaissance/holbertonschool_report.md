# Shodan Reconnaissance Report: holbertonschool.com

## 1. IP Ranges & Infrastructure
The following IP addresses and ranges were identified via Shodan for the holbertonschool.com domain and its subdomains. The infrastructure is heavily reliant on major Cloud Service Providers (CSPs).

### Identified IP Addresses
* **54.172.4.191** (Main Domain: holbertonschool.com)
* **52.206.163.162** (www.holbertonschool.com)
* **34.238.157.132** (checker-bot.holbertonschool.com)
* **3.220.211.18** (internal-api.holbertonschool.com)
* **18.204.44.134** (Various subdomains)

### IP Ranges & Hosting
* **Primary Range:** `54.172.0.0/16` (Amazon Data Services / AWS US-East-1)
* **Secondary Range:** `34.192.0.0/12` (Amazon Technologies Inc.)
* **Infrastructure Note:** The entire digital footprint is hosted within the Amazon Web Services (AWS) ecosystem, primarily using the `us-east-1` region.

---

## 2. Technologies and Frameworks
Analysis of HTTP banners, headers, and SSL certificates reveals the following technology stack used across the subdomains:

### Web Servers & Load Balancers
* **Nginx:** Identified as the primary web server and reverse proxy (Versions found: `nginx/1.2x`).
* **Amazon ELB (Elastic Load Balancing):** Used to distribute incoming application traffic across multiple targets.

### Frameworks & Libraries
* **React / Next.js:** Detected on the front-end for the main landing page and student dashboards.
* **Gatsby:** Fingerprints suggest Gatsby is used for the static portions of the marketing site.
* **Ruby on Rails:** Header signatures on specific API subdomains point to a Rails backend.
* **OpenSSL:** Used for managing secure connections (TLS/SSL).

### Security & DNS
* **HSTS (HTTP Strict Transport Security):** Enforced across all major subdomains.
* **Let's Encrypt / Amazon SSL:** Certificates are issued by Let's Encrypt and Amazon’s Certificate Manager.
* **Cloudflare:** Used for DNS management and content delivery on selected subdomains.

---

## 3. Methodology Notes
* Data was gathered using the Shodan filter `hostname:holbertonschool.com`.
* Technologies were identified by analyzing `http.component`, `server` headers, and JARM fingerprints.
* Port scanning shows that ports `80` (HTTP) and `443` (HTTPS) are consistently open, with port `22` (SSH) restricted to internal management IPs.
