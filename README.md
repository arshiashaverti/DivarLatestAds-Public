<div align="center">

# Divar Latest Ads Monitor

**A modular Python application for monitoring new listings on Divar.**

[فارسی](#فارسی) · [English](#english)

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Browser-Playwright-2EAD33?logo=playwright&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Unittest-success)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## English

### Overview

Divar Latest Ads Monitor is an educational Python project that checks a configured Divar search page, extracts listing information, compares listing IDs with previously stored data, and can notify users when new listings are detected.

The project provides three usage modes:

- **Listing export:** collect listings and save them as a JSON file.
- **Local monitoring:** periodically check for new listings and display Windows desktop notifications.
- **Cloud monitoring:** check listings once and send notifications through the Telegram Bot API.

The repository is designed as a modular learning project. It does not include personal credentials, real user data, or an active scheduled monitoring service.

### Why this project?

**Practical value**
- Reduces the need to repeatedly refresh a search page manually.
- Helps users notice newly published listings sooner.
- Demonstrates how a small automation tool can support a focused search workflow.

**Educational value**
- Python modules and separation of responsibilities.
- Asynchronous programming with `asyncio`.
- Browser automation and page interaction with Playwright.
- HTTP requests and Telegram Bot API integration.
- JSON-based persistence and error handling.
- Unit testing and automated checks with GitHub Actions.

### Technology stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Main programming language |
| Playwright | Browser automation |
| asyncio | Asynchronous execution |
| JSON | Local listing-state storage and export |
| Telegram Bot API | Optional cloud notifications |
| winotify | Optional Windows desktop notifications |
| unittest | Automated unit tests |
| Git and GitHub Actions | Version control and CI checks |

### Project structure

```text
DivarLatestAds/
├── src/
│   └── divar_monitor/
│       ├── config.py
│       ├── scraper.py
│       ├── storage.py
│       ├── telegram.py
│       ├── local_monitor.py
│       ├── cloud_monitor.py
│       └── __main__.py
├── tests/
├── examples/
├── docs/
├── .github/
│   └── workflows/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

### Requirements

- Python 3.11 or newer
- Internet access to reach the configured search page
- Chromium browser installed through Playwright
- A Telegram bot and chat ID only if cloud notifications are used
- Windows for native desktop notifications

### Installation

Clone the repository:

```bash
git clone https://github.com/arshiashaverti/DivarLatestAds-Public.git
cd DivarLatestAds-Public
```

Create and activate a virtual environment:

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install --upgrade pip
pip install -e .
python -m playwright install chromium
```

For Windows desktop notifications:

```bash
pip install -e ".[windows]"
```

For development and tests:

```bash
pip install -e ".[dev]"
```

### Usage

**1. Export listings to JSON**

```bash
python -m divar_monitor --output data/ads.json
```

**2. Start local monitoring**

```bash
python -m divar_monitor.local_monitor
```

The local monitor checks the configured search page every five minutes. On its first successful run, it stores a baseline and does not notify for existing listings.

**3. Configure Telegram cloud notifications**

Set these environment variables locally or in your deployment environment:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

PowerShell example:

```powershell
$env:TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
$env:TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

Run one cloud check:

```bash
python -m divar_monitor.cloud_monitor
```

The first successful cloud run stores a baseline without sending notifications. Later runs compare listing IDs and send a Telegram message for newly detected listings.

**Security:** Never commit real tokens, chat IDs, `.env` files, or credentials. Use environment variables or your deployment platform's secret manager.

### Configuration

The following environment variables are supported:

| Variable | Default | Description |
|---|---|---|
| `DIVAR_URL` | Project search URL | Search page to monitor |
| `DIVAR_MAX_ADS` | `10` | Maximum number of listings to extract |
| `DIVAR_WAIT_MS` | `4000` | Delay after page navigation |
| `DIVAR_STATE_FILE` | `data/known_ads.json` | Listing history file |
| `TELEGRAM_BOT_TOKEN` | Not set | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Not set | Destination chat ID |

See `.env.example` for a configuration template. The application reads environment variables directly; it does not automatically load a `.env` file.

### Tests

Install development dependencies and run:

```bash
python -m unittest discover -s tests -v
```

The tests cover configuration validation, JSON state storage, and basic listing-ID comparison. They do not make live requests to Divar or Telegram.

### Limitations

- Website page structure and selectors may change.
- Access restrictions, network errors, or anti-automation measures may prevent extraction.
- The application only examines a limited number of listings per check.
- Local monitoring requires a running process and does not run as a background service automatically.
- Cloud state persistence depends on the environment in which the application is deployed.
- Telegram delivery depends on valid credentials and Telegram availability.

### Responsible use

Use reasonable request intervals and comply with the target website's terms, applicable laws, and access restrictions. This project is provided for educational purposes and is not affiliated with or endorsed by Divar.

### License

This project is released under the MIT License. See [LICENSE](LICENSE).

---

## فارسی

### معرفی پروژه

**Divar Latest Ads Monitor** یک پروژه آموزشی و کاربردی با زبان Python است که یک صفحه جست‌وجوی مشخص در دیوار را بررسی می‌کند، اطلاعات آگهی‌ها را استخراج می‌کند و با مقایسه شناسه آگهی‌ها با سوابق قبلی، آگهی‌های جدید را تشخیص می‌دهد.

این پروژه سه شیوه استفاده دارد:

- **استخراج آگهی:** دریافت آگهی‌ها و ذخیره آن‌ها در فایل JSON.
- **پایش محلی:** بررسی دوره‌ای آگهی‌ها و نمایش اعلان دسکتاپ ویندوز.
- **پایش ابری:** بررسی آگهی‌ها و ارسال اعلان از طریق ربات تلگرام.

این مخزن با هدف نمایش مهارت‌های برنامه‌نویسی و یادگیری ساخته شده است. هیچ توکن واقعی، اطلاعات شخصی یا سرویس زمان‌بندی‌شده فعالی در آن قرار ندارد.

### هدف و ارزش اقتصادی

در بسیاری از جست‌وجوهای هدفمند، کاربر مجبور است یک صفحه را بارها به‌صورت دستی بررسی کند. این ابزار بخشی از این کار تکراری را خودکار می‌کند.

کاربردهای عملی پروژه:

- کاهش زمان صرف‌شده برای بررسی دستی آگهی‌ها.
- شناسایی سریع‌تر آگهی‌های جدید در یک جست‌وجوی مشخص.
- ارسال اعلان در صورت مشاهده آگهی تازه.
- ارائه یک نمونه واقعی از کاربرد اتوماسیون در یک فرایند روزمره.

این پروژه به‌خودی‌خود درآمد یا سود مالی تضمین نمی‌کند؛ ارزش اقتصادی آن در صرفه‌جویی زمان و امکان توسعه ابزارهای مشابه برای نیازهای دیگر است.

### ارزش آموزشی و مهارت‌های به‌کاررفته

در این پروژه مفاهیم و ابزارهای زیر به کار رفته‌اند:

- **Python:** طراحی و توسعه منطق اصلی برنامه.
- **Asyncio:** اجرای عملیات ناهمگام.
- **Playwright:** کنترل مرورگر و استخراج اطلاعات صفحه.
- **HTTP و Telegram Bot API:** ارتباط با سرویس خارجی و ارسال اعلان.
- **JSON:** ذخیره اطلاعات و سابقه آگهی‌ها.
- **مدیریت خطا:** کنترل خطاهای شبکه، استخراج و ارسال اعلان.
- **Unit Testing:** بررسی خودکار بخش‌های اصلی برنامه.
- **Git و GitHub:** مدیریت نسخه‌های پروژه.
- **GitHub Actions:** اجرای خودکار بررسی‌ها و تست‌های کد.

### پیش‌نیازها

- Python نسخه 3.11 یا بالاتر.
- دسترسی اینترنت.
- مرورگر Chromium نصب‌شده از طریق Playwright.
- برای اعلان ابری: توکن ربات تلگرام و شناسه چت.
- برای اعلان دسکتاپ: سیستم‌عامل Windows.

### نصب و راه‌اندازی

ابتدا مخزن را دریافت کن:

```bash
git clone https://github.com/arshiashaverti/DivarLatestAds-Public.git
cd DivarLatestAds-Public
```

ساخت محیط مجازی در ویندوز:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

نصب وابستگی‌ها:

```bash
python -m pip install --upgrade pip
pip install -e .
python -m playwright install chromium
```

برای اعلان ویندوز:

```bash
pip install -e ".[windows]"
```

برای ابزارهای توسعه و تست:

```bash
pip install -e ".[dev]"
```

### روش استفاده

**۱. استخراج آگهی‌ها و ذخیره در JSON**

```bash
python -m divar_monitor --output data/ads.json
```

**۲. اجرای پایش محلی**

```bash
python -m divar_monitor.local_monitor
```

برنامه هر پنج دقیقه صفحه جست‌وجو را بررسی می‌کند. در اولین اجرای موفق، وضعیت فعلی آگهی‌ها را به‌عنوان سابقه اولیه ذخیره می‌کند و برای آگهی‌های موجود اعلان نمی‌فرستد.

**۳. راه‌اندازی اعلان تلگرام**

دو متغیر محیطی زیر باید تنظیم شوند:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

نمونه در PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
$env:TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

سپس یک بار پایش ابری را اجرا کن:

```bash
python -m divar_monitor.cloud_monitor
```

در اولین اجرای موفق، آگهی‌های موجود ثبت می‌شوند. در اجراهای بعدی، آگهی‌های جدید شناسایی و از طریق تلگرام اطلاع‌رسانی می‌شوند.

**نکته امنیتی:** توکن واقعی، شناسه چت و فایل‌های محرمانه را در GitHub منتشر نکن. از متغیرهای محیطی یا Secretهای محیط اجرا استفاده کن.

### تنظیمات برنامه

| متغیر | مقدار پیش‌فرض | کاربرد |
|---|---|---|
| `DIVAR_URL` | آدرس جست‌وجوی پروژه | صفحه هدف |
| `DIVAR_MAX_ADS` | `10` | حداکثر تعداد آگهی |
| `DIVAR_WAIT_MS` | `4000` | مکث پس از بازشدن صفحه |
| `DIVAR_STATE_FILE` | `data/known_ads.json` | مسیر فایل سابقه |
| `TELEGRAM_BOT_TOKEN` | تعریف‌نشده | توکن ربات |
| `TELEGRAM_CHAT_ID` | تعریف‌نشده | شناسه مقصد تلگرام |

فایل `.env.example` صرفاً الگوی تنظیمات است. برنامه به‌صورت خودکار فایل `.env` را بارگذاری نمی‌کند و متغیرها باید در محیط اجرا تعریف شوند.

### اجرای تست‌ها

```bash
python -m unittest discover -s tests -v
```

تست‌های فعلی تنظیمات، ذخیره‌سازی JSON و مقایسه شناسه آگهی‌ها را بررسی می‌کنند. این تست‌ها درخواست واقعی به دیوار یا تلگرام ارسال نمی‌کنند.

### محدودیت‌ها

- تغییر ساختار HTML دیوار ممکن است استخراج آگهی‌ها را مختل کند.
- محدودیت دسترسی سایت یا خطاهای شبکه می‌توانند باعث شکست پایش شوند.
- در هر نوبت فقط تعداد محدودی آگهی بررسی می‌شود.
- پایش محلی به روشن بودن برنامه نیاز دارد.
- ماندگاری سوابق در اجرای ابری به محیط استقرار بستگی دارد.
- ارسال پیام به درستی تنظیم بودن اطلاعات ربات تلگرام وابسته است.

### استفاده مسئولانه

از فاصله زمانی منطقی بین درخواست‌ها استفاده کن و شرایط استفاده وب‌سایت هدف، محدودیت‌های دسترسی و قوانین مربوط را رعایت کن. این پروژه آموزشی و مستقل است و وابستگی یا تأیید رسمی از طرف دیوار ندارد.

### مجوز

این پروژه تحت مجوز MIT منتشر می‌شود. متن کامل مجوز در فایل [LICENSE](LICENSE) قرار دارد.