# 🐦 Twitter Trends Notifier

This Python application automatically monitors trending topics on Twitter in Argentina (country code `29`) using [Apify's](https://apify.com) `twitter-trends-scraper` actor. If it detects any trends related to **Mercado Libre**, **Mercado Pago**, or custom keywords, it sends alert emails to different recipient groups.

## 🚀 Features

- Uses the [Apify SDK](https://docs.apify.com/sdk/python) to get live Twitter trends.
- Scans for custom keyword matches (e.g., "mercadolibre", "mercadopago").
- Sends well-formatted HTML emails with trend position and tweet volume.
- Runs every hour between 9:00 AM and 7:00 PM (ART) using GitHub Actions.
- Keeps sensitive information secure using GitHub Secrets.

---

## 📦 Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

To install locally:

```bash
pip install -r requirements.txt
````

---

## 🔧 Configuration with Secrets

This project uses GitHub Actions secrets to securely store credentials and recipient information.

| Secret Name        | Description                                                 |
| ------------------ | ----------------------------------------------------------- |
| `APIFY_API_TOKEN`  | Your Apify API token                                        |
| `EMAIL_SENDER`     | Sender email address (e.g., Gmail account)                  |
| `EMAIL_PASSWORD`   | Email password or app password for SMTP login               |
| `DESTINATARIOS_ML` | Comma-separated list of recipients for Mercado Libre trends |
| `DESTINATARIOS_MP` | Comma-separated list of recipients for Mercado Pago trends  |

---

## 📤 Email Notification Format

If a relevant trend is detected, an email like the following will be sent:

> **MercadoLibre** is trend No. **4** in Argentina with **50.2K tweets**.

Emails are formatted in HTML for clarity and visual appeal.

---

## ⚙️ GitHub Actions Workflow

The included workflow runs the script every hour between 9:00 and 19:00 (ART), which corresponds to 12:00–22:00 UTC.

Located at `.github/workflows/twitter_trends.yml`.

You can also run the workflow manually from the **Actions** tab.

---

## 🛡 Security Notice

**Never** commit sensitive information like API keys or email passwords directly in the code. Always use [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) to manage credentials securely.

---

## 📄 License

This project is private and not licensed for redistribution. For internal use only at **Publica LATAM**.


Let me know!
```
