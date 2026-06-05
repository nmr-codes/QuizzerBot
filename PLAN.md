# QuizMaster AI — Complete Engineering Blueprint
> **Version:** 1.0.0  
> **Status:** Production Blueprint  
> **Audience:** AI Agent / Senior Engineer  
> **Goal:** Build a production-ready Telegram SaaS from 0% to 100%

---

## ⚠️ AGENT INSTRUCTIONS

You are building **QuizMaster AI** — an enterprise-grade Telegram SaaS. This document is your single source of truth. Read every section completely before writing a single line of code. Follow the phases in exact order. Do not skip steps. Do not improvise architecture. Every decision is pre-made here.

**Rules:**
1. Follow folder structure exactly as defined.
2. Follow database schema exactly as defined.
3. Follow API contracts exactly as defined.
4. Use the specified tech stack only.
5. Write production-grade code — no shortcuts, no TODOs left behind.
6. Every module must have error handling, logging, and tests.
7. After each phase, verify it works before moving to next phase.

---

## TABLE OF CONTENTS

1. [Product Overview](#1-product-overview)
2. [System Architecture](#2-system-architecture)
3. [Folder Structure](#3-folder-structure)
4. [Database Schema](#4-database-schema)
5. [Environment Configuration](#5-environment-configuration)
6. [Phase 1 — Project Bootstrap](#phase-1--project-bootstrap)
7. [Phase 2 — Database Layer](#phase-2--database-layer)
8. [Phase 3 — Core Backend API](#phase-3--core-backend-api)
9. [Phase 4 — AI Engine](#phase-4--ai-engine)
10. [Phase 5 — File Processing Pipeline](#phase-5--file-processing-pipeline)
11. [Phase 6 — Telegram Bot](#phase-6--telegram-bot)
12. [Phase 7 — Payment System](#phase-7--payment-system)
13. [Phase 8 — Gamification Engine](#phase-8--gamification-engine)
14. [Phase 9 — Admin Panel](#phase-9--admin-panel)
15. [Phase 10 — Analytics & Monitoring](#phase-10--analytics--monitoring)
16. [Phase 11 — Security Hardening](#phase-11--security-hardening)
17. [Phase 12 — DevOps & Deployment](#phase-12--devops--deployment)
18. [Phase 13 — Testing](#phase-13--testing)
19. [API Reference](#api-reference)
20. [Telegram Bot Flow](#telegram-bot-flow)
21. [Admin Panel Design Spec](#admin-panel-design-spec)
22. [Implementation Checklist](#implementation-checklist)

---

## 1. PRODUCT OVERVIEW

### What It Is
QuizMaster AI is a Telegram-native SaaS platform that converts educational documents into interactive learning experiences using Google Gemini AI.

### Who Uses It
- **Students** preparing for exams
- **Teachers** creating assessments
- **Self-learners** studying any topic
- **Corporate trainers** building training materials

### Core Value Proposition
Upload any document → Get AI-powered quizzes, flashcards, summaries, and a full exam experience in seconds.

### Revenue Model
Dynamic subscription plans + Credit-based AI consumption. Admin controls everything without code changes.

---

## 2. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        TELEGRAM CLIENTS                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Webhook HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX (Reverse Proxy)                          │
│              SSL Termination + Rate Limiting                      │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌───────────────────────────────────┐
│   Aiogram Bot        │      │     FastAPI Backend                │
│   (Python 3.12)      │      │     (Python 3.12)                 │
│   Port: 8001         │      │     Port: 8000                    │
└──────────┬───────────┘      └────────────┬──────────────────────┘
           │                               │
           └──────────────┬────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REDIS (Message Broker + Cache)               │
│                          Port: 6379                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CELERY WORKERS                                 │
│   Worker 1: File Processing    Worker 2: AI Generation           │
│   Worker 3: Notifications      Worker 4: Analytics               │
└──────────────────────────────┬──────────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
┌───────────────────┐ ┌───────────────┐ ┌─────────────────────┐
│   PostgreSQL      │ │  Local/S3     │ │  Google Gemini API  │
│   Port: 5432      │ │  Storage      │ │  (AI Processing)    │
└───────────────────┘ └───────────────┘ └─────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **Nginx** | SSL, reverse proxy, rate limiting, static files |
| **FastAPI** | REST API, auth, business logic, admin panel backend |
| **Aiogram Bot** | Telegram interface, user interactions |
| **PostgreSQL** | Persistent data storage |
| **Redis** | Session cache, task queue, rate limiting, result cache |
| **Celery** | Async file processing, AI generation, background jobs |
| **Gemini API** | Text analysis, quiz/flashcard/summary generation |
| **Local Storage** | Uploaded files (abstracted for future S3 migration) |

---

## 3. FOLDER STRUCTURE

```
quizmaster-ai/
│
├── 📄 docker-compose.yml
├── 📄 docker-compose.prod.yml
├── 📄 .env.example
├── 📄 .env
├── 📄 .gitignore
├── 📄 Makefile
├── 📄 README.md
│
├── 📁 nginx/
│   ├── nginx.conf
│   ├── ssl/
│   └── conf.d/
│       └── quizmaster.conf
│
├── 📁 backend/
│   ├── 📄 Dockerfile
│   ├── 📄 requirements.txt
│   ├── 📄 alembic.ini
│   ├── 📄 main.py                    # FastAPI app entry point
│   │
│   ├── 📁 alembic/
│   │   ├── env.py
│   │   └── versions/                  # Migration files
│   │
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Settings (pydantic-settings)
│   │   │   ├── security.py            # JWT, password hashing
│   │   │   ├── logging.py             # Structured logging setup
│   │   │   ├── exceptions.py          # Custom exceptions
│   │   │   └── dependencies.py        # FastAPI deps (auth, db, etc.)
│   │   │
│   │   ├── 📁 db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # SQLAlchemy base, session
│   │   │   └── session.py             # DB session factory
│   │   │
│   │   ├── 📁 models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── plan.py
│   │   │   ├── subscription.py
│   │   │   ├── credit.py
│   │   │   ├── transaction.py
│   │   │   ├── payment.py
│   │   │   ├── upload.py
│   │   │   ├── quiz.py
│   │   │   ├── flashcard.py
│   │   │   ├── summary.py
│   │   │   ├── referral.py
│   │   │   ├── achievement.py
│   │   │   ├── leaderboard.py
│   │   │   ├── channel.py
│   │   │   ├── broadcast.py
│   │   │   ├── analytics.py
│   │   │   ├── ai_usage.py
│   │   │   ├── setting.py
│   │   │   ├── audit_log.py
│   │   │   └── notification.py
│   │   │
│   │   ├── 📁 schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── plan.py
│   │   │   ├── subscription.py
│   │   │   ├── credit.py
│   │   │   ├── payment.py
│   │   │   ├── upload.py
│   │   │   ├── quiz.py
│   │   │   ├── flashcard.py
│   │   │   ├── summary.py
│   │   │   ├── referral.py
│   │   │   ├── achievement.py
│   │   │   ├── analytics.py
│   │   │   ├── broadcast.py
│   │   │   ├── setting.py
│   │   │   └── common.py
│   │   │
│   │   ├── 📁 repositories/           # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Generic CRUD base
│   │   │   ├── user_repo.py
│   │   │   ├── plan_repo.py
│   │   │   ├── subscription_repo.py
│   │   │   ├── credit_repo.py
│   │   │   ├── payment_repo.py
│   │   │   ├── upload_repo.py
│   │   │   ├── quiz_repo.py
│   │   │   ├── flashcard_repo.py
│   │   │   ├── summary_repo.py
│   │   │   ├── referral_repo.py
│   │   │   ├── achievement_repo.py
│   │   │   ├── analytics_repo.py
│   │   │   ├── setting_repo.py
│   │   │   └── ai_usage_repo.py
│   │   │
│   │   ├── 📁 services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── plan_service.py
│   │   │   ├── subscription_service.py
│   │   │   ├── credit_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── upload_service.py
│   │   │   ├── quiz_service.py
│   │   │   ├── flashcard_service.py
│   │   │   ├── summary_service.py
│   │   │   ├── referral_service.py
│   │   │   ├── achievement_service.py
│   │   │   ├── gamification_service.py
│   │   │   ├── leaderboard_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── broadcast_service.py
│   │   │   ├── channel_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── cache_service.py
│   │   │   ├── storage_service.py
│   │   │   └── setting_service.py
│   │   │
│   │   ├── 📁 ai/                     # AI Engine
│   │   │   ├── __init__.py
│   │   │   ├── gemini_client.py       # Gemini API wrapper + key rotation
│   │   │   ├── prompt_builder.py      # All prompts centralized
│   │   │   ├── quiz_generator.py
│   │   │   ├── flashcard_generator.py
│   │   │   ├── summary_generator.py
│   │   │   ├── concept_extractor.py
│   │   │   ├── definition_extractor.py
│   │   │   ├── adaptive_engine.py
│   │   │   ├── exam_engine.py
│   │   │   ├── content_hasher.py      # For cache dedup
│   │   │   └── token_tracker.py       # Cost tracking
│   │   │
│   │   ├── 📁 file_processing/        # File Parser Pipeline
│   │   │   ├── __init__.py
│   │   │   ├── base_parser.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── docx_parser.py
│   │   │   ├── pptx_parser.py
│   │   │   ├── txt_parser.py
│   │   │   ├── html_parser.py
│   │   │   ├── image_parser.py        # OCR via Gemini Vision
│   │   │   ├── parser_factory.py      # Selects correct parser
│   │   │   └── text_cleaner.py        # Normalize extracted text
│   │   │
│   │   ├── 📁 payments/               # Payment Providers
│   │   │   ├── __init__.py
│   │   │   ├── base_provider.py
│   │   │   ├── telegram_stars.py
│   │   │   ├── click.py
│   │   │   ├── payme.py
│   │   │   ├── uzum.py
│   │   │   ├── paynet.py
│   │   │   └── payment_router.py      # Routes to correct provider
│   │   │
│   │   ├── 📁 tasks/                  # Celery Tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── file_tasks.py          # File processing tasks
│   │   │   ├── ai_tasks.py            # AI generation tasks
│   │   │   ├── notification_tasks.py  # Telegram notify tasks
│   │   │   ├── analytics_tasks.py     # Aggregation tasks
│   │   │   ├── cleanup_tasks.py       # Temp file cleanup
│   │   │   └── scheduler.py           # Periodic tasks (celery beat)
│   │   │
│   │   ├── 📁 api/                    # FastAPI Routes
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Main router aggregator
│   │   │   │
│   │   │   ├── 📁 v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── uploads.py
│   │   │   │   ├── quizzes.py
│   │   │   │   ├── flashcards.py
│   │   │   │   ├── summaries.py
│   │   │   │   ├── plans.py
│   │   │   │   ├── subscriptions.py
│   │   │   │   ├── credits.py
│   │   │   │   ├── payments.py
│   │   │   │   ├── referrals.py
│   │   │   │   ├── achievements.py
│   │   │   │   ├── leaderboard.py
│   │   │   │   └── webhooks.py        # Payment webhooks
│   │   │   │
│   │   │   └── 📁 admin/
│   │   │       ├── __init__.py
│   │   │       ├── dashboard.py
│   │   │       ├── users.py
│   │   │       ├── plans.py
│   │   │       ├── settings.py
│   │   │       ├── analytics.py
│   │   │       ├── broadcast.py
│   │   │       ├── channels.py
│   │   │       ├── ai_monitor.py
│   │   │       ├── payments.py
│   │   │       └── owner.py           # Owner-only endpoints
│   │   │
│   │   ├── 📁 middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth_middleware.py
│   │   │   ├── rate_limit_middleware.py
│   │   │   ├── logging_middleware.py
│   │   │   ├── cors_middleware.py
│   │   │   └── audit_middleware.py
│   │   │
│   │   └── 📁 utils/
│   │       ├── __init__.py
│   │       ├── pagination.py
│   │       ├── validators.py
│   │       ├── formatters.py
│   │       ├── crypto.py
│   │       └── helpers.py
│   │
│   └── 📁 tests/
│       ├── conftest.py
│       ├── 📁 unit/
│       │   ├── test_ai_generators.py
│       │   ├── test_file_parsers.py
│       │   ├── test_credit_service.py
│       │   ├── test_gamification.py
│       │   └── test_payment_providers.py
│       └── 📁 integration/
│           ├── test_auth_flow.py
│           ├── test_upload_flow.py
│           ├── test_quiz_flow.py
│           └── test_payment_flow.py
│
├── 📁 bot/
│   ├── 📄 Dockerfile
│   ├── 📄 requirements.txt
│   ├── 📄 main.py                     # Bot entry point
│   │
│   ├── 📁 handlers/
│   │   ├── __init__.py
│   │   ├── start.py                   # /start, onboarding
│   │   ├── upload.py                  # File upload handling
│   │   ├── quiz.py                    # Quiz interaction
│   │   ├── flashcard.py               # Flashcard interaction
│   │   ├── summary.py                 # Summary display
│   │   ├── exam.py                    # Exam mode
│   │   ├── profile.py                 # User profile & stats
│   │   ├── subscription.py            # Plans & payment
│   │   ├── referral.py                # Referral system
│   │   ├── achievements.py            # Achievements display
│   │   ├── leaderboard.py             # Leaderboard
│   │   ├── settings.py                # User settings
│   │   ├── help.py                    # Help & FAQ
│   │   └── admin.py                   # In-bot admin commands
│   │
│   ├── 📁 keyboards/
│   │   ├── __init__.py
│   │   ├── main_menu.py
│   │   ├── quiz_keyboards.py
│   │   ├── flashcard_keyboards.py
│   │   ├── exam_keyboards.py
│   │   ├── profile_keyboards.py
│   │   ├── subscription_keyboards.py
│   │   ├── admin_keyboards.py
│   │   └── inline_keyboards.py
│   │
│   ├── 📁 states/
│   │   ├── __init__.py
│   │   ├── upload_states.py
│   │   ├── quiz_states.py
│   │   ├── exam_states.py
│   │   └── subscription_states.py
│   │
│   ├── 📁 middlewares/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py         # Register/authenticate user
│   │   ├── channel_check.py           # Mandatory channel subscription
│   │   ├── subscription_check.py      # Plan/credit check
│   │   ├── rate_limit.py
│   │   ├── anti_spam.py
│   │   └── i18n_middleware.py         # Multi-language
│   │
│   ├── 📁 services/
│   │   ├── __init__.py
│   │   ├── api_client.py              # HTTP client to FastAPI backend
│   │   └── message_builder.py         # Format Telegram messages
│   │
│   ├── 📁 locales/
│   │   ├── uz.json                    # Uzbek
│   │   ├── ru.json                    # Russian
│   │   └── en.json                    # English
│   │
│   └── 📁 tests/
│       ├── conftest.py
│       └── test_handlers.py
│
├── 📁 admin_panel/
│   ├── 📄 package.json
│   ├── 📄 vite.config.js
│   ├── 📁 src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── 📁 pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Users.jsx
│   │   │   ├── Plans.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Broadcasts.jsx
│   │   │   ├── Channels.jsx
│   │   │   ├── Payments.jsx
│   │   │   ├── AIMonitor.jsx
│   │   │   ├── Settings.jsx
│   │   │   └── Owner.jsx
│   │   ├── 📁 components/
│   │   ├── 📁 hooks/
│   │   ├── 📁 services/
│   │   └── 📁 utils/
│   └── 📄 Dockerfile
│
├── 📁 scripts/
│   ├── init_db.py                     # First-time DB setup
│   ├── seed_data.py                   # Seed initial settings
│   ├── backup_db.sh
│   ├── restore_db.sh
│   ├── deploy.sh
│   └── health_check.sh
│
└── 📁 docs/
    ├── api.md
    ├── deployment.md
    ├── bot_flow.md
    └── admin_guide.md
```

---

## 4. DATABASE SCHEMA

### 4.1 Complete ERD Description

Every table uses UUID primary keys. All timestamps are `TIMESTAMPTZ`. Soft deletes where applicable.

---

### Table: `users`
```sql
CREATE TABLE users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id         BIGINT UNIQUE NOT NULL,
    username            VARCHAR(255),
    first_name          VARCHAR(255),
    last_name           VARCHAR(255),
    language_code       VARCHAR(10) DEFAULT 'uz',
    phone               VARCHAR(20),
    is_active           BOOLEAN DEFAULT TRUE,
    is_banned           BOOLEAN DEFAULT FALSE,
    ban_reason          TEXT,
    is_admin            BOOLEAN DEFAULT FALSE,
    is_owner            BOOLEAN DEFAULT FALSE,
    referral_code       VARCHAR(20) UNIQUE NOT NULL,
    referred_by         UUID REFERENCES users(id),
    xp_points           INTEGER DEFAULT 0,
    level               INTEGER DEFAULT 1,
    daily_streak        INTEGER DEFAULT 0,
    weekly_streak       INTEGER DEFAULT 0,
    longest_streak      INTEGER DEFAULT 0,
    last_activity_date  DATE,
    last_seen_at        TIMESTAMPTZ,
    timezone            VARCHAR(50) DEFAULT 'Asia/Tashkent',
    notification_enabled BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_referral_code ON users(referral_code);
CREATE INDEX idx_users_referred_by ON users(referred_by);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Table: `plans`
```sql
CREATE TABLE plans (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                VARCHAR(100) NOT NULL,
    slug                VARCHAR(100) UNIQUE NOT NULL,
    description         TEXT,
    price_uzs           DECIMAL(15,2) NOT NULL DEFAULT 0,
    duration_days       INTEGER NOT NULL,
    credits             INTEGER NOT NULL DEFAULT 0,
    bonus_credits       INTEGER NOT NULL DEFAULT 0,
    features            JSONB DEFAULT '[]',
    max_uploads_per_day INTEGER DEFAULT -1,  -- -1 = unlimited
    max_file_size_mb    INTEGER DEFAULT 10,
    priority_processing BOOLEAN DEFAULT FALSE,
    is_active           BOOLEAN DEFAULT TRUE,
    sort_order          INTEGER DEFAULT 0,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `subscriptions`
```sql
CREATE TABLE subscriptions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    plan_id         UUID NOT NULL REFERENCES plans(id),
    status          VARCHAR(20) DEFAULT 'active'
                    CHECK (status IN ('active','expired','cancelled','paused')),
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL,
    auto_renew      BOOLEAN DEFAULT FALSE,
    cancelled_at    TIMESTAMPTZ,
    cancel_reason   TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_expires_at ON subscriptions(expires_at);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

### Table: `credits`
```sql
CREATE TABLE credits (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id),
    balance         INTEGER NOT NULL DEFAULT 0,
    lifetime_earned INTEGER NOT NULL DEFAULT 0,
    lifetime_spent  INTEGER NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `credit_transactions`
```sql
CREATE TABLE credit_transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    amount          INTEGER NOT NULL,        -- positive = earn, negative = spend
    balance_after   INTEGER NOT NULL,
    type            VARCHAR(30) NOT NULL
                    CHECK (type IN (
                        'purchase','subscription','welcome_bonus',
                        'daily_bonus','referral_bonus','achievement_bonus',
                        'promotional','admin_grant','admin_remove',
                        'quiz_generation','flashcard_generation',
                        'summary_generation','exam_mode',
                        'concept_extraction','definition_extraction',
                        'wrong_answer_explanation','refund'
                    )),
    description     TEXT,
    reference_id    UUID,           -- FK to payment, quiz, upload, etc.
    reference_type  VARCHAR(50),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_credit_tx_user_id ON credit_transactions(user_id);
CREATE INDEX idx_credit_tx_type ON credit_transactions(type);
CREATE INDEX idx_credit_tx_created_at ON credit_transactions(created_at);
```

### Table: `payments`
```sql
CREATE TABLE payments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id),
    plan_id             UUID REFERENCES plans(id),
    provider            VARCHAR(30) NOT NULL
                        CHECK (provider IN (
                            'telegram_stars','click','payme','uzum','paynet'
                        )),
    external_id         VARCHAR(255),           -- Provider's transaction ID
    amount_uzs          DECIMAL(15,2) NOT NULL,
    amount_stars        INTEGER,                -- For Telegram Stars
    status              VARCHAR(20) DEFAULT 'pending'
                        CHECK (status IN (
                            'pending','processing','completed','failed','refunded'
                        )),
    provider_response   JSONB,
    webhook_data        JSONB,
    completed_at        TIMESTAMPTZ,
    failed_at           TIMESTAMPTZ,
    failure_reason      TEXT,
    credits_granted     INTEGER DEFAULT 0,
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_provider ON payments(provider);
CREATE INDEX idx_payments_external_id ON payments(external_id);
CREATE INDEX idx_payments_created_at ON payments(created_at);
```

### Table: `uploads`
```sql
CREATE TABLE uploads (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id),
    original_filename   VARCHAR(500) NOT NULL,
    file_type           VARCHAR(10) NOT NULL
                        CHECK (file_type IN ('pdf','docx','pptx','txt','html','image')),
    file_size_bytes     BIGINT NOT NULL,
    storage_path        TEXT NOT NULL,
    mime_type           VARCHAR(100),
    content_hash        VARCHAR(64),            -- SHA-256 for dedup
    extracted_text      TEXT,
    word_count          INTEGER,
    page_count          INTEGER,
    language            VARCHAR(10),
    subject             VARCHAR(100),
    processing_status   VARCHAR(20) DEFAULT 'pending'
                        CHECK (processing_status IN (
                            'pending','processing','completed','failed'
                        )),
    processing_started_at TIMESTAMPTZ,
    processing_ended_at   TIMESTAMPTZ,
    error_message       TEXT,
    ai_analyzed         BOOLEAN DEFAULT FALSE,
    ai_analyzed_at      TIMESTAMPTZ,
    is_cached           BOOLEAN DEFAULT FALSE,  -- Reused from another upload
    source_upload_id    UUID REFERENCES uploads(id),
    telegram_file_id    VARCHAR(255),
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_uploads_user_id ON uploads(user_id);
CREATE INDEX idx_uploads_content_hash ON uploads(content_hash);
CREATE INDEX idx_uploads_processing_status ON uploads(processing_status);
CREATE INDEX idx_uploads_created_at ON uploads(created_at);
```

### Table: `quizzes`
```sql
CREATE TABLE quizzes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id       UUID NOT NULL REFERENCES uploads(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    title           VARCHAR(500),
    difficulty      VARCHAR(10) DEFAULT 'medium'
                    CHECK (difficulty IN ('easy','medium','hard','mixed')),
    question_count  INTEGER NOT NULL,
    question_types  JSONB DEFAULT '["multiple_choice"]',
    questions       JSONB NOT NULL,             -- Full questions array
    is_adaptive     BOOLEAN DEFAULT FALSE,
    weak_topics     JSONB DEFAULT '[]',
    total_attempts  INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_quizzes_upload_id ON quizzes(upload_id);
CREATE INDEX idx_quizzes_user_id ON quizzes(user_id);
```

### Table: `quiz_sessions`
```sql
CREATE TABLE quiz_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quiz_id             UUID NOT NULL REFERENCES quizzes(id),
    user_id             UUID NOT NULL REFERENCES users(id),
    mode                VARCHAR(20) DEFAULT 'practice'
                        CHECK (mode IN ('practice','exam','adaptive')),
    status              VARCHAR(20) DEFAULT 'in_progress'
                        CHECK (status IN ('in_progress','completed','abandoned')),
    total_questions     INTEGER NOT NULL,
    answered_questions  INTEGER DEFAULT 0,
    correct_answers     INTEGER DEFAULT 0,
    wrong_answers       INTEGER DEFAULT 0,
    skipped_answers     INTEGER DEFAULT 0,
    score_percentage    DECIMAL(5,2),
    time_limit_seconds  INTEGER,
    time_spent_seconds  INTEGER,
    started_at          TIMESTAMPTZ DEFAULT NOW(),
    completed_at        TIMESTAMPTZ,
    xp_earned           INTEGER DEFAULT 0,
    detailed_results    JSONB DEFAULT '[]'      -- Per-question breakdown
);

CREATE INDEX idx_quiz_sessions_user_id ON quiz_sessions(user_id);
CREATE INDEX idx_quiz_sessions_quiz_id ON quiz_sessions(quiz_id);
```

### Table: `flashcard_sets`
```sql
CREATE TABLE flashcard_sets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id       UUID NOT NULL REFERENCES uploads(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    title           VARCHAR(500),
    card_count      INTEGER NOT NULL,
    cards           JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `flashcard_sessions`
```sql
CREATE TABLE flashcard_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flashcard_set_id    UUID NOT NULL REFERENCES flashcard_sets(id),
    user_id             UUID NOT NULL REFERENCES users(id),
    status              VARCHAR(20) DEFAULT 'in_progress',
    total_cards         INTEGER NOT NULL,
    reviewed_cards      INTEGER DEFAULT 0,
    easy_count          INTEGER DEFAULT 0,
    medium_count        INTEGER DEFAULT 0,
    hard_count          INTEGER DEFAULT 0,
    started_at          TIMESTAMPTZ DEFAULT NOW(),
    completed_at        TIMESTAMPTZ
);
```

### Table: `summaries`
```sql
CREATE TABLE summaries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id       UUID NOT NULL REFERENCES uploads(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    summary_text    TEXT NOT NULL,
    key_concepts    JSONB DEFAULT '[]',
    definitions     JSONB DEFAULT '[]',
    word_count      INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `referrals`
```sql
CREATE TABLE referrals (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_id         UUID NOT NULL REFERENCES users(id),
    referred_id         UUID NOT NULL REFERENCES users(id),
    status              VARCHAR(20) DEFAULT 'pending'
                        CHECK (status IN ('pending','converted','rewarded')),
    referrer_reward     INTEGER DEFAULT 0,      -- Credits given
    referred_reward     INTEGER DEFAULT 0,
    converted_at        TIMESTAMPTZ,
    rewarded_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(referrer_id, referred_id)
);
```

### Table: `achievements`
```sql
CREATE TABLE achievements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            VARCHAR(100) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    icon            VARCHAR(10),               -- Emoji
    xp_reward       INTEGER DEFAULT 0,
    credit_reward   INTEGER DEFAULT 0,
    condition_type  VARCHAR(50) NOT NULL,
    condition_value INTEGER NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `user_achievements`
```sql
CREATE TABLE user_achievements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    achievement_id  UUID NOT NULL REFERENCES achievements(id),
    earned_at       TIMESTAMPTZ DEFAULT NOW(),
    notified        BOOLEAN DEFAULT FALSE,
    UNIQUE(user_id, achievement_id)
);
```

### Table: `channels`
```sql
CREATE TABLE channels (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id     BIGINT NOT NULL,
    username        VARCHAR(255),
    title           VARCHAR(500),
    is_required     BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    sort_order      INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `broadcasts`
```sql
CREATE TABLE broadcasts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id        UUID NOT NULL REFERENCES users(id),
    title           VARCHAR(500),
    content_type    VARCHAR(20) CHECK (content_type IN ('text','photo','video','document')),
    text_content    TEXT,
    media_file_id   VARCHAR(255),
    buttons         JSONB DEFAULT '[]',
    target_segment  VARCHAR(30) DEFAULT 'all'
                    CHECK (target_segment IN ('all','premium','active','custom')),
    segment_filter  JSONB,
    status          VARCHAR(20) DEFAULT 'draft'
                    CHECK (status IN ('draft','scheduled','sending','completed','failed')),
    scheduled_at    TIMESTAMPTZ,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    total_recipients INTEGER DEFAULT 0,
    sent_count      INTEGER DEFAULT 0,
    failed_count    INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `ai_usage_logs`
```sql
CREATE TABLE ai_usage_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    upload_id       UUID REFERENCES uploads(id),
    operation       VARCHAR(50) NOT NULL,
    model           VARCHAR(100),
    prompt_tokens   INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    total_tokens    INTEGER DEFAULT 0,
    estimated_cost_usd DECIMAL(10,6) DEFAULT 0,
    latency_ms      INTEGER,
    api_key_index   INTEGER DEFAULT 0,          -- Which key rotation index
    success         BOOLEAN DEFAULT TRUE,
    error_message   TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ai_usage_created_at ON ai_usage_logs(created_at);
CREATE INDEX idx_ai_usage_operation ON ai_usage_logs(operation);
CREATE INDEX idx_ai_usage_user_id ON ai_usage_logs(user_id);
```

### Table: `settings`
```sql
CREATE TABLE settings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key             VARCHAR(200) UNIQUE NOT NULL,
    value           JSONB NOT NULL,
    type            VARCHAR(20) DEFAULT 'string'
                    CHECK (type IN ('string','integer','boolean','json','list')),
    category        VARCHAR(100),
    description     TEXT,
    is_secret       BOOLEAN DEFAULT FALSE,
    updated_by      UUID REFERENCES users(id),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Table: `audit_logs`
```sql
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    action          VARCHAR(100) NOT NULL,
    resource_type   VARCHAR(50),
    resource_id     UUID,
    old_values      JSONB,
    new_values      JSONB,
    ip_address      VARCHAR(45),
    user_agent      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

### Table: `daily_analytics`
```sql
CREATE TABLE daily_analytics (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date            DATE UNIQUE NOT NULL,
    new_users       INTEGER DEFAULT 0,
    active_users    INTEGER DEFAULT 0,
    total_uploads   INTEGER DEFAULT 0,
    total_quizzes   INTEGER DEFAULT 0,
    total_flashcards INTEGER DEFAULT 0,
    total_summaries INTEGER DEFAULT 0,
    quiz_sessions   INTEGER DEFAULT 0,
    revenue_uzs     DECIMAL(15,2) DEFAULT 0,
    new_subscriptions INTEGER DEFAULT 0,
    ai_tokens_used  BIGINT DEFAULT 0,
    ai_cost_usd     DECIMAL(10,4) DEFAULT 0,
    new_referrals   INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Default Settings (Seed Data)
```json
{
  "welcome_credits": 50,
  "daily_bonus_credits": 5,
  "referral_bonus_referrer": 30,
  "referral_bonus_referred": 20,
  "credit_cost_quiz": 10,
  "credit_cost_flashcards": 8,
  "credit_cost_summary": 5,
  "credit_cost_exam_mode": 15,
  "credit_cost_concept_extraction": 5,
  "credit_cost_definition_extraction": 5,
  "credit_cost_wrong_answer_explanation": 3,
  "xp_per_correct_answer": 10,
  "xp_per_quiz_complete": 50,
  "xp_per_exam_complete": 100,
  "xp_per_flashcard_session": 20,
  "max_file_size_mb_free": 10,
  "max_file_size_mb_premium": 50,
  "gemini_api_keys": [],
  "gemini_model": "gemini-1.5-flash",
  "mandatory_channels_enabled": true,
  "payment_click_enabled": false,
  "payment_payme_enabled": false,
  "payment_telegram_stars_enabled": true,
  "ai_cache_enabled": true,
  "ai_cache_ttl_days": 30
}
```

---

## 5. ENVIRONMENT CONFIGURATION

### `.env.example`
```bash
# ==========================================
# QUIZMASTER AI — Environment Configuration
# ==========================================

# App
APP_NAME=QuizMaster AI
APP_ENV=production          # development | production
DEBUG=false
SECRET_KEY=your-secret-key-min-32-chars-here
ALLOWED_HOSTS=yourdomain.com,localhost

# Database
DATABASE_URL=postgresql+asyncpg://quizmaster:password@postgres:5432/quizmaster_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_CACHE_DB=1
REDIS_RATE_LIMIT_DB=2

# Bot
BOT_TOKEN=your-telegram-bot-token
WEBHOOK_URL=https://yourdomain.com/webhook/bot
WEBHOOK_SECRET=your-webhook-secret
ADMIN_TELEGRAM_IDS=123456789,987654321
OWNER_TELEGRAM_ID=123456789

# AI
GEMINI_API_KEY_1=your-gemini-key-1
GEMINI_API_KEY_2=your-gemini-key-2
GEMINI_API_KEY_3=your-gemini-key-3
GEMINI_MODEL=gemini-1.5-flash

# Storage
STORAGE_BACKEND=local           # local | s3
STORAGE_LOCAL_PATH=/app/storage
STORAGE_MAX_FILE_SIZE_MB=50
# Future S3:
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_BUCKET_NAME=
# AWS_REGION=

# JWT
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# Celery
CELERY_BROKER_URL=redis://redis:6379/3
CELERY_RESULT_BACKEND=redis://redis:6379/4

# Admin Panel
ADMIN_SECRET_KEY=your-admin-secret
ADMIN_SESSION_EXPIRE_HOURS=24

# Payment Providers
CLICK_MERCHANT_ID=
CLICK_SECRET_KEY=
CLICK_SERVICE_ID=

PAYME_MERCHANT_ID=
PAYME_SECRET_KEY=

UZUM_MERCHANT_ID=
UZUM_SECRET_KEY=

PAYNET_MERCHANT_ID=
PAYNET_SECRET_KEY=

# Monitoring
SENTRY_DSN=
LOG_LEVEL=INFO
```

---

## PHASE 1 — PROJECT BOOTSTRAP

### Goal
Set up complete project skeleton with working Docker environment.

### Steps

#### 1.1 Create root-level files

**`docker-compose.yml`:**
```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: quizmaster_db
      POSTGRES_USER: quizmaster
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U quizmaster"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    volumes:
      - ./backend:/app
      - storage_data:/app/storage
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  bot:
    build:
      context: ./bot
      dockerfile: Dockerfile
    env_file: .env
    volumes:
      - ./bot:/app
    depends_on:
      - backend
      - redis
    command: python main.py

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    volumes:
      - ./backend:/app
      - storage_data:/app/storage
    depends_on:
      - postgres
      - redis
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4 -Q file_processing,ai_generation,notifications,analytics

  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
    command: celery -A app.tasks.celery_app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

  flower:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file: .env
    ports:
      - "5555:5555"
    depends_on:
      - redis
    command: celery -A app.tasks.celery_app flower --port=5555

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - static_files:/app/static
    depends_on:
      - backend
      - bot

volumes:
  postgres_data:
  redis_data:
  storage_data:
  static_files:
```

**`Makefile`:**
```makefile
.PHONY: up down restart build migrate seed logs shell test

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

build:
	docker-compose build

migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python scripts/seed_data.py

logs:
	docker-compose logs -f $(service)

shell:
	docker-compose exec backend bash

test:
	docker-compose exec backend pytest tests/ -v

clean:
	docker-compose down -v --remove-orphans
```

#### 1.2 Backend `requirements.txt`
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy[asyncio]==2.0.35
asyncpg==0.29.0
alembic==1.13.3
pydantic==2.9.2
pydantic-settings==2.5.2
redis[asyncio]==5.1.1
celery[redis]==5.4.0
flower==2.0.1
google-generativeai==0.8.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
httpx==0.27.2
aiofiles==24.1.0
Pillow==10.4.0
PyMuPDF==1.24.11        # PDF parsing (fitz)
python-docx==1.1.2
python-pptx==1.0.2
beautifulsoup4==4.12.3
pytesseract==0.3.13
langdetect==1.0.9
bleach==6.1.0
slowapi==0.1.9
sentry-sdk[fastapi]==2.14.0
structlog==24.4.0
pytest==8.3.3
pytest-asyncio==0.24.0
pytest-cov==5.0.0
httpx==0.27.2
factory-boy==3.3.1
Faker==30.3.0
```

#### 1.3 Backend `Dockerfile`
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System dependencies for file processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-uzb \
    tesseract-ocr-rus \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create storage directory
RUN mkdir -p /app/storage/uploads /app/storage/temp

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 1.4 FastAPI entry point `backend/main.py`
```python
"""
QuizMaster AI — FastAPI Application Entry Point
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import create_db_tables
from app.api.router import api_router
from app.middleware.rate_limit_middleware import setup_rate_limiting
from app.middleware.logging_middleware import RequestLoggingMiddleware

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    logger.info("🚀 QuizMaster AI starting up...")
    await create_db_tables()
    logger.info("✅ Database ready")
    yield
    logger.info("🛑 QuizMaster AI shutting down...")


app = FastAPI(
    title="QuizMaster AI",
    description="AI-powered study assistant API",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not settings.DEBUG:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

setup_rate_limiting(app)

# Routers
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
```

---

## PHASE 2 — DATABASE LAYER

### Goal
Implement all SQLAlchemy models, Alembic migrations, and repository pattern.

### Steps

#### 2.1 Base Model
```python
# app/db/base.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
```

#### 2.2 Session Factory
```python
# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

#### 2.3 Base Repository
```python
# app/repositories/base.py
from typing import TypeVar, Generic, Type, Optional, List, Any
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: UUID) -> Optional[ModelType]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_many(
        self,
        filters: dict = None,
        skip: int = 0,
        limit: int = 50,
        order_by: Any = None
    ) -> List[ModelType]:
        query = select(self.model)
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        if order_by is not None:
            query = query.order_by(order_by)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: dict = None) -> int:
        query = select(func.count()).select_from(self.model)
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: UUID, obj_in: dict) -> Optional[ModelType]:
        await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in)
        )
        return await self.get(id)

    async def delete(self, id: UUID) -> bool:
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount > 0
```

#### 2.4 Migration Setup
```bash
# Run in backend/ directory
alembic init alembic

# In alembic/env.py — configure to use async engine and import all models
# Then:
alembic revision --autogenerate -m "initial_schema"
alembic upgrade head
```

---

## PHASE 3 — CORE BACKEND API

### Goal
Implement all FastAPI routes with proper auth, validation, and service layer.

### 3.1 Settings (Core Config)
```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "QuizMaster AI"
    APP_ENV: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = ["*"]

    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40

    REDIS_URL: str
    REDIS_CACHE_DB: int = 1
    REDIS_RATE_LIMIT_DB: int = 2

    BOT_TOKEN: str
    WEBHOOK_URL: str
    WEBHOOK_SECRET: str
    ADMIN_TELEGRAM_IDS: List[int] = []
    OWNER_TELEGRAM_ID: int

    GEMINI_API_KEYS: List[str] = []
    GEMINI_MODEL: str = "gemini-1.5-flash"

    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str = "/app/storage"
    STORAGE_MAX_FILE_SIZE_MB: int = 50

    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### 3.2 Authentication Flow

**JWT Token Creation:**
```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise ValueError("Invalid token")
```

**Bot Authentication Endpoint:**
The bot authenticates users by hitting `POST /api/v1/auth/telegram` with the Telegram user object (validated via bot token HMAC). Backend returns JWT token. Bot stores token in Redis session.

### 3.3 API Router Structure
```python
# app/api/router.py
from fastapi import APIRouter
from app.api.v1 import (
    auth, users, uploads, quizzes, flashcards,
    summaries, plans, subscriptions, credits,
    payments, referrals, achievements, leaderboard, webhooks
)
from app.api.admin import (
    dashboard, users as admin_users, plans as admin_plans,
    settings as admin_settings, analytics, broadcast,
    channels, ai_monitor, payments as admin_payments, owner
)

api_router = APIRouter()

# Public/User routes
api_router.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/v1/users", tags=["Users"])
api_router.include_router(uploads.router, prefix="/v1/uploads", tags=["Uploads"])
api_router.include_router(quizzes.router, prefix="/v1/quizzes", tags=["Quizzes"])
api_router.include_router(flashcards.router, prefix="/v1/flashcards", tags=["Flashcards"])
api_router.include_router(summaries.router, prefix="/v1/summaries", tags=["Summaries"])
api_router.include_router(plans.router, prefix="/v1/plans", tags=["Plans"])
api_router.include_router(subscriptions.router, prefix="/v1/subscriptions", tags=["Subscriptions"])
api_router.include_router(credits.router, prefix="/v1/credits", tags=["Credits"])
api_router.include_router(payments.router, prefix="/v1/payments", tags=["Payments"])
api_router.include_router(referrals.router, prefix="/v1/referrals", tags=["Referrals"])
api_router.include_router(achievements.router, prefix="/v1/achievements", tags=["Achievements"])
api_router.include_router(leaderboard.router, prefix="/v1/leaderboard", tags=["Leaderboard"])
api_router.include_router(webhooks.router, prefix="/v1/webhooks", tags=["Webhooks"])

# Admin routes
api_router.include_router(dashboard.router, prefix="/admin/dashboard", tags=["Admin"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["Admin"])
# ... (all admin routes)
```

---

## PHASE 4 — AI ENGINE

### Goal
Build a robust AI engine with key rotation, cost tracking, caching, and all generation functions.

### 4.1 Gemini Client with Auto-Rotation
```python
# app/ai/gemini_client.py
import asyncio
import hashlib
import json
import time
from typing import Optional
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import get_logger
from app.ai.token_tracker import TokenTracker

logger = get_logger(__name__)


class GeminiClient:
    """
    Production Gemini client with:
    - Automatic API key rotation
    - Retry with exponential backoff
    - Token usage tracking
    - Cost estimation
    - Error handling
    """

    COST_PER_1K_INPUT_TOKENS = 0.000075    # USD (Flash)
    COST_PER_1K_OUTPUT_TOKENS = 0.0003     # USD (Flash)

    def __init__(self):
        self._keys = settings.GEMINI_API_KEYS
        self._current_key_idx = 0
        self._lock = asyncio.Lock()
        self._tracker = TokenTracker()
        self._configure_current_key()

    def _configure_current_key(self):
        genai.configure(api_key=self._keys[self._current_key_idx])
        self._model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def _rotate_key(self):
        async with self._lock:
            self._current_key_idx = (self._current_key_idx + 1) % len(self._keys)
            self._configure_current_key()
            logger.info(f"Rotated to Gemini key index {self._current_key_idx}")

    async def generate(
        self,
        prompt: str,
        user_id: str = None,
        upload_id: str = None,
        operation: str = "unknown",
        temperature: float = 0.7,
        max_retries: int = 3,
    ) -> dict:
        """
        Core generation method. Returns:
        {
            "text": str,
            "prompt_tokens": int,
            "completion_tokens": int,
            "total_tokens": int,
            "cost_usd": float,
            "latency_ms": int
        }
        """
        last_error = None
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                response = self._model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=8192,
                    )
                )
                latency_ms = int((time.time() - start_time) * 1000)

                # Extract usage
                usage = response.usage_metadata
                prompt_tokens = usage.prompt_token_count
                completion_tokens = usage.candidates_token_count
                total_tokens = usage.total_token_count

                cost = (
                    (prompt_tokens / 1000) * self.COST_PER_1K_INPUT_TOKENS +
                    (completion_tokens / 1000) * self.COST_PER_1K_OUTPUT_TOKENS
                )

                # Track usage
                await self._tracker.record(
                    user_id=user_id,
                    upload_id=upload_id,
                    operation=operation,
                    model=settings.GEMINI_MODEL,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    key_index=self._current_key_idx,
                )

                return {
                    "text": response.text,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "cost_usd": cost,
                    "latency_ms": latency_ms,
                }

            except Exception as e:
                last_error = e
                logger.warning(f"Gemini attempt {attempt + 1} failed: {e}")
                if "quota" in str(e).lower() or "rate" in str(e).lower():
                    await self._rotate_key()
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        raise RuntimeError(f"Gemini failed after {max_retries} attempts: {last_error}")


# Singleton
gemini_client = GeminiClient()
```

### 4.2 Prompt Builder (ALL PROMPTS CENTRALIZED)
```python
# app/ai/prompt_builder.py

SYSTEM_CONTEXT = """You are QuizMaster AI, an expert educational content analyzer.
You analyze academic texts and produce structured learning materials.
Always respond in valid JSON format as specified. Never add explanations outside JSON."""


def build_quiz_prompt(
    text: str,
    count: int,
    difficulty: str,
    question_types: list,
    language: str = "uz"
) -> str:
    return f"""
{SYSTEM_CONTEXT}

Analyze this educational text and generate exactly {count} quiz questions.

TEXT:
{text[:15000]}

REQUIREMENTS:
- Difficulty: {difficulty}
- Question types: {', '.join(question_types)}
- Language: {language} (respond in this language)
- Cover different topics from the text
- For multiple_choice: 4 options with exactly 1 correct
- For true_false: clear factual statements
- For fill_blank: remove key terms
- For short_answer: open-ended conceptual questions

RESPOND WITH THIS EXACT JSON:
{{
  "title": "Quiz title based on content",
  "questions": [
    {{
      "id": 1,
      "type": "multiple_choice|true_false|fill_blank|short_answer",
      "question": "Question text",
      "options": ["A", "B", "C", "D"],  // only for multiple_choice
      "correct_answer": "Correct option or answer",
      "explanation": "Why this is correct",
      "topic": "Subtopic this covers",
      "difficulty": "easy|medium|hard"
    }}
  ]
}}
"""


def build_flashcard_prompt(text: str, count: int, language: str = "uz") -> str:
    return f"""
{SYSTEM_CONTEXT}

Create {count} flashcards from this educational text.

TEXT:
{text[:15000]}

RESPOND WITH THIS EXACT JSON:
{{
  "title": "Flashcard set title",
  "cards": [
    {{
      "id": 1,
      "front": "Question or term (concise)",
      "back": "Answer or definition (clear and complete)",
      "topic": "Subtopic",
      "hint": "Optional memory hint"
    }}
  ]
}}
"""


def build_summary_prompt(text: str, language: str = "uz") -> str:
    return f"""
{SYSTEM_CONTEXT}

Create a comprehensive study summary of this text.

TEXT:
{text[:20000]}

RESPOND WITH THIS EXACT JSON:
{{
  "title": "Document title",
  "summary": "3-5 paragraph comprehensive summary",
  "key_concepts": [
    {{
      "concept": "Concept name",
      "explanation": "Clear explanation",
      "importance": "high|medium|low"
    }}
  ],
  "definitions": [
    {{
      "term": "Technical term",
      "definition": "Precise definition",
      "example": "Usage example"
    }}
  ],
  "main_topics": ["Topic 1", "Topic 2"],
  "study_tips": ["Tip 1", "Tip 2"]
}}
"""


def build_adaptive_quiz_prompt(
    text: str,
    weak_topics: list,
    previous_wrong: list,
    language: str = "uz"
) -> str:
    return f"""
{SYSTEM_CONTEXT}

Generate an ADAPTIVE quiz targeting student's weak areas.

STUDENT'S WEAK TOPICS: {', '.join(weak_topics)}
PREVIOUS WRONG ANSWERS: {json.dumps(previous_wrong[:10])}

TEXT:
{text[:15000]}

Focus 70% of questions on weak topics. Vary difficulty.
Use same JSON format as standard quiz.
"""


def build_wrong_explanation_prompt(
    question: str,
    correct_answer: str,
    student_answer: str,
    language: str = "uz"
) -> str:
    return f"""
{SYSTEM_CONTEXT}

Explain why the student's answer is wrong and teach the correct concept.

QUESTION: {question}
CORRECT ANSWER: {correct_answer}
STUDENT'S WRONG ANSWER: {student_answer}

RESPOND WITH THIS EXACT JSON:
{{
  "what_went_wrong": "Brief explanation of the mistake",
  "correct_explanation": "Full explanation of the correct answer",
  "key_concept": "The concept to remember",
  "memory_tip": "Easy way to remember this",
  "related_topics": ["Related topic 1"]
}}
"""
```

### 4.3 Content Cache (Deduplication)
```python
# app/ai/content_hasher.py
import hashlib


def compute_content_hash(text: str) -> str:
    """SHA-256 hash of normalized text for dedup."""
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()
```

```python
# app/services/cache_service.py
import json
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings

CACHE_TTL = 60 * 60 * 24 * 30  # 30 days


class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url(
            settings.REDIS_URL.replace("/0", f"/{settings.REDIS_CACHE_DB}")
        )

    def _key(self, content_hash: str, operation: str, params: dict) -> str:
        param_str = json.dumps(params, sort_keys=True)
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        return f"ai:cache:{operation}:{content_hash}:{param_hash}"

    async def get(self, content_hash: str, operation: str, params: dict) -> Optional[dict]:
        data = await self.redis.get(self._key(content_hash, operation, params))
        return json.loads(data) if data else None

    async def set(self, content_hash: str, operation: str, params: dict, result: dict):
        await self.redis.setex(
            self._key(content_hash, operation, params),
            CACHE_TTL,
            json.dumps(result)
        )
```

---

## PHASE 5 — FILE PROCESSING PIPELINE

### Goal
Parse all file types, extract clean text, trigger AI analysis via Celery.

### 5.1 Parser Factory
```python
# app/file_processing/parser_factory.py
from app.file_processing.pdf_parser import PDFParser
from app.file_processing.docx_parser import DocxParser
from app.file_processing.pptx_parser import PptxParser
from app.file_processing.txt_parser import TxtParser
from app.file_processing.html_parser import HtmlParser
from app.file_processing.image_parser import ImageParser


def get_parser(file_type: str):
    parsers = {
        "pdf": PDFParser,
        "docx": DocxParser,
        "pptx": PptxParser,
        "txt": TxtParser,
        "html": HtmlParser,
        "image": ImageParser,
    }
    parser_class = parsers.get(file_type.lower())
    if not parser_class:
        raise ValueError(f"Unsupported file type: {file_type}")
    return parser_class()
```

### 5.2 PDF Parser
```python
# app/file_processing/pdf_parser.py
import fitz  # PyMuPDF
from app.file_processing.base_parser import BaseParser
from app.file_processing.text_cleaner import clean_text


class PDFParser(BaseParser):
    async def extract(self, file_path: str) -> dict:
        doc = fitz.open(file_path)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        raw_text = "\n".join(text_parts)
        doc.close()
        return {
            "text": clean_text(raw_text),
            "page_count": len(doc),
            "word_count": len(raw_text.split()),
        }
```

### 5.3 Image Parser (OCR via Gemini Vision)
```python
# app/file_processing/image_parser.py
import base64
from pathlib import Path
import google.generativeai as genai
from app.file_processing.base_parser import BaseParser


class ImageParser(BaseParser):
    async def extract(self, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        suffix = Path(file_path).suffix.lower().lstrip(".")
        mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                    "png": "image/png", "webp": "image/webp"}
        mime_type = mime_map.get(suffix, "image/jpeg")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            },
            "Extract ALL text from this image. Return only the extracted text, nothing else."
        ])
        text = response.text
        return {
            "text": text,
            "page_count": 1,
            "word_count": len(text.split()),
        }
```

### 5.4 Celery Tasks
```python
# app/tasks/file_tasks.py
from app.tasks.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(
    bind=True,
    name="tasks.process_file",
    queue="file_processing",
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
)
def process_file_task(self, upload_id: str):
    """
    1. Download file from storage
    2. Detect file type
    3. Extract text using correct parser
    4. Clean text
    5. Compute content hash
    6. Check if identical content was processed before (cache)
    7. Save extracted text to DB
    8. Trigger AI analysis
    9. Notify user via bot
    """
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_process_file_async(upload_id))
    except Exception as exc:
        logger.error(f"File processing failed for {upload_id}: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="tasks.generate_ai_content",
    queue="ai_generation",
    max_retries=2,
    default_retry_delay=60,
)
def generate_ai_content_task(self, upload_id: str, operations: list):
    """
    operations: list of ["quiz", "flashcards", "summary"]
    Generates requested content and saves to DB.
    Deducts credits.
    Notifies user.
    """
    pass
```

---

## PHASE 6 — TELEGRAM BOT

### Goal
Build the full Telegram bot with all user flows, keyboards, states, and middleware.

### 6.1 Bot Entry Point
```python
# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from handlers import start, upload, quiz, flashcard, summary, exam, profile
from handlers import subscription, referral, achievements, leaderboard, settings, help
from middlewares.auth_middleware import AuthMiddleware
from middlewares.channel_check import ChannelCheckMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.anti_spam import AntiSpamMiddleware
from middlewares.i18n_middleware import I18nMiddleware

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


async def on_startup(bot: Bot):
    await bot.set_webhook(
        url=f"{WEBHOOK_URL}/webhook/bot",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query", "pre_checkout_query",
                         "successful_payment", "inline_query"]
    )
    logging.info("✅ Bot webhook set")


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Middlewares (order matters!)
    dp.message.middleware(I18nMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    dp.message.middleware(AntiSpamMiddleware())
    dp.message.middleware(ChannelCheckMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    dp.callback_query.middleware(ChannelCheckMiddleware())

    # Register handlers
    dp.include_router(start.router)
    dp.include_router(upload.router)
    dp.include_router(quiz.router)
    dp.include_router(flashcard.router)
    dp.include_router(summary.router)
    dp.include_router(exam.router)
    dp.include_router(profile.router)
    dp.include_router(subscription.router)
    dp.include_router(referral.router)
    dp.include_router(achievements.router)
    dp.include_router(leaderboard.router)
    dp.include_router(settings.router)
    dp.include_router(help.router)

    # Webhook
    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET)
    handler.register(app, path="/webhook/bot")
    setup_application(app, dp, bot=bot)
    dp.startup.register(on_startup)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8001)
    await site.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
```

### 6.2 Auth Middleware (Register/Authenticate Every User)
```python
# bot/middlewares/auth_middleware.py
from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.services.api_client import APIClient


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict
    ) -> Any:
        user = event.from_user
        api = APIClient()

        # Register or login user, get JWT
        auth_response = await api.post("/v1/auth/telegram", json={
            "telegram_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code,
            "referral_code": data.get("start_param"),  # From /start deep link
        })

        data["current_user"] = auth_response["user"]
        data["access_token"] = auth_response["access_token"]
        data["api"] = APIClient(token=auth_response["access_token"])

        return await handler(event, data)
```

### 6.3 Channel Check Middleware
```python
# bot/middlewares/channel_check.py
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class ChannelCheckMiddleware(BaseMiddleware):
    EXEMPT_COMMANDS = ["/start"]

    async def __call__(self, handler, event, data):
        api: APIClient = data.get("api")
        user = data.get("current_user")

        # Get required channels from API
        channels = await api.get("/v1/channels/required")

        if not channels["mandatory_enabled"]:
            return await handler(event, data)

        # Check membership for each channel
        not_joined = []
        for channel in channels["channels"]:
            try:
                member = await event.bot.get_chat_member(
                    channel["telegram_id"], user["telegram_id"]
                )
                if member.status in ["left", "kicked", "banned"]:
                    not_joined.append(channel)
            except Exception:
                not_joined.append(channel)

        if not_joined:
            # Show subscribe prompt with buttons
            await show_channel_subscription_prompt(event, not_joined)
            return  # Block handler

        return await handler(event, data)
```

### 6.4 Complete Start Handler
```python
# bot/handlers/start.py
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.main_menu import get_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, current_user: dict, **kwargs):
    user = current_user
    is_new = user.get("is_new", False)

    if is_new:
        welcome_text = (
            f"🎓 <b>Xush kelibsiz, {message.from_user.first_name}!</b>\n\n"
            f"Men <b>QuizMaster AI</b> — sizning shaxsiy AI o'qituvchingizman.\n\n"
            f"📚 Har qanday hujjat yuboring va men:\n"
            f"• ✅ Quiz savollari yarataman\n"
            f"• 🃏 Flashcard kartochkalar tayyorlayman\n"
            f"• 📝 Qisqacha mazmun chiqaraman\n"
            f"• 💡 Asosiy tushunchalarni ajrataman\n\n"
            f"🎁 Sizga <b>{user['welcome_credits']} kredit</b> sovg'a!\n\n"
            f"Boshlash uchun istalgan hujjat yuboring 👇"
        )
    else:
        stats = user.get("stats", {})
        welcome_text = (
            f"👋 <b>Qaytib keldingiz, {message.from_user.first_name}!</b>\n\n"
            f"📊 Sizning statistikangiz:\n"
            f"• 🏆 XP: {stats.get('xp', 0)} ball\n"
            f"• 🔥 Streak: {stats.get('streak', 0)} kun\n"
            f"• 💳 Kredit: {stats.get('credits', 0)}\n\n"
            f"Nima qilishni xohlaysiz?"
        )

    await message.answer(welcome_text, reply_markup=get_main_menu(user))
```

### 6.5 Main Menu Keyboard
```python
# bot/keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(user: dict) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="📤 Hujjat yuklash")],
        [
            KeyboardButton(text="📚 Mening materiallarim"),
            KeyboardButton(text="📊 Profil"),
        ],
        [
            KeyboardButton(text="🏆 Reyting"),
            KeyboardButton(text="🎁 Chegirma kodi"),
        ],
        [
            KeyboardButton(text="💎 Premium"),
            KeyboardButton(text="❓ Yordam"),
        ],
    ]

    if user.get("is_admin"):
        buttons.append([KeyboardButton(text="⚙️ Admin Panel")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
```

### 6.6 Upload Handler (Core Flow)
```python
# bot/handlers/upload.py
from aiogram import Router, F
from aiogram.types import Message, Document, PhotoSize
from aiogram.fsm.context import FSMContext
from bot.states.upload_states import UploadStates
from bot.keyboards.inline_keyboards import get_generation_options_keyboard

router = Router()

ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "text/plain": "txt",
    "text/html": "html",
}


@router.message(F.document)
async def handle_document(message: Message, state: FSMContext, api, current_user):
    doc = message.document

    # Validate file type
    file_type = ALLOWED_MIME_TYPES.get(doc.mime_type)
    if not file_type:
        await message.answer(
            "❌ Bu fayl turi qo'llab-quvvatlanmaydi.\n\n"
            "✅ Qo'llab-quvvatlanadigan turlar:\n"
            "PDF, DOCX, PPTX, TXT, HTML, rasm"
        )
        return

    # Check credits
    credits = current_user.get("credits", 0)
    if credits < 5:  # Minimum for any operation
        await message.answer(
            "❌ Kredit yetarli emas!\n\n"
            "💳 Hozirgi kredit: {credits}\n\n"
            "💎 Kredit sotib olish uchun /premium buyrug'ini yuboring."
        )
        return

    # Check file size
    max_size = current_user.get("max_file_size_mb", 10) * 1024 * 1024
    if doc.file_size > max_size:
        await message.answer(
            f"❌ Fayl hajmi juda katta!\n"
            f"Maksimal: {max_size // (1024*1024)}MB\n"
            f"Sizning faylingiz: {doc.file_size // (1024*1024)}MB"
        )
        return

    # Send processing message
    processing_msg = await message.answer(
        "⏳ <b>Fayl qabul qilindi!</b>\n\n"
        "🔄 Yuklanmoqda..."
    )

    # Upload to backend
    file = await message.bot.get_file(doc.file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    response = await api.upload_file(
        file_bytes=file_bytes.read(),
        filename=doc.file_name,
        file_type=file_type,
        telegram_file_id=doc.file_id,
    )

    upload_id = response["upload_id"]
    await state.update_data(upload_id=upload_id)

    await processing_msg.edit_text(
        f"✅ <b>Fayl muvaffaqiyatli yuklandi!</b>\n\n"
        f"📄 Fayl: {doc.file_name}\n"
        f"📊 Hajm: {doc.file_size // 1024}KB\n\n"
        f"Nima yaratishni xohlaysiz? 👇",
        reply_markup=get_generation_options_keyboard(upload_id)
    )


@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext, api, current_user):
    """Handle image uploads — OCR via Gemini Vision"""
    photo = message.photo[-1]  # Highest resolution
    # Same flow as document but file_type = "image"
    ...
```

### 6.7 Quiz Interaction Handler
```python
# bot/handlers/quiz.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.quiz_states import QuizStates
from bot.keyboards.quiz_keyboards import (
    get_quiz_answer_keyboard,
    get_quiz_result_keyboard,
    get_quiz_settings_keyboard,
)

router = Router()


@router.callback_query(F.data.startswith("quiz:start:"))
async def start_quiz(callback: CallbackQuery, state: FSMContext, api, current_user):
    quiz_id = callback.data.split(":")[2]

    # Deduct credits
    deduct_resp = await api.post(f"/v1/credits/deduct", json={
        "amount": 10,
        "type": "quiz_generation",
        "reference_id": quiz_id,
    })
    if not deduct_resp["success"]:
        await callback.answer("❌ Kredit yetarli emas!", show_alert=True)
        return

    # Fetch quiz
    quiz = await api.get(f"/v1/quizzes/{quiz_id}")

    # Create session
    session = await api.post("/v1/quizzes/sessions", json={"quiz_id": quiz_id})

    await state.set_state(QuizStates.answering)
    await state.update_data(
        quiz=quiz,
        session_id=session["id"],
        current_q=0,
        correct=0,
        wrong=0,
        results=[],
    )

    await send_question(callback.message, state, 0, quiz)
    await callback.answer()


async def send_question(message, state: FSMContext, q_index: int, quiz: dict):
    data = await state.get_data()
    question = quiz["questions"][q_index]
    total = len(quiz["questions"])

    progress_bar = "█" * (q_index + 1) + "░" * (total - q_index - 1)

    text = (
        f"📝 <b>Savol {q_index + 1}/{total}</b>\n"
        f"<code>{progress_bar}</code>\n\n"
        f"❓ {question['question']}"
    )

    keyboard = get_quiz_answer_keyboard(question, q_index)
    await message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("quiz:answer:"), QuizStates.answering)
async def handle_answer(callback: CallbackQuery, state: FSMContext, api, current_user):
    _, _, q_index, answer_index = callback.data.split(":")
    q_index = int(q_index)

    data = await state.get_data()
    quiz = data["quiz"]
    question = quiz["questions"][q_index]
    correct_answer = question["correct_answer"]
    selected_option = question["options"][int(answer_index)]

    is_correct = selected_option == correct_answer

    # Update state
    results = data["results"]
    results.append({
        "question_id": question["id"],
        "selected": selected_option,
        "correct": correct_answer,
        "is_correct": is_correct,
    })

    correct = data["correct"] + (1 if is_correct else 0)
    wrong = data["wrong"] + (0 if is_correct else 1)

    await state.update_data(
        current_q=q_index + 1,
        correct=correct,
        wrong=wrong,
        results=results,
    )

    # Show result for this question
    result_emoji = "✅" if is_correct else "❌"
    await callback.answer(
        f"{result_emoji} {'To\'g\'ri!' if is_correct else 'Noto\'g\'ri!'}\n"
        f"Javob: {correct_answer}",
        show_alert=not is_correct
    )

    # Next question or finish
    next_q = q_index + 1
    if next_q < len(quiz["questions"]):
        await send_question(callback.message, state, next_q, quiz)
    else:
        await finish_quiz(callback.message, state, api, current_user)


async def finish_quiz(message, state: FSMContext, api, current_user):
    data = await state.get_data()
    total = len(data["quiz"]["questions"])
    correct = data["correct"]
    score = (correct / total) * 100

    # Save session results
    await api.patch(f"/v1/quizzes/sessions/{data['session_id']}", json={
        "status": "completed",
        "correct_answers": correct,
        "wrong_answers": data["wrong"],
        "score_percentage": score,
        "detailed_results": data["results"],
    })

    # XP earned
    xp_earned = correct * 10 + 50  # 10 per correct + 50 completion bonus

    grade = "🏆 A+" if score >= 90 else "🥇 A" if score >= 80 else \
            "🥈 B" if score >= 70 else "🥉 C" if score >= 60 else "📚 F"

    result_text = (
        f"🎉 <b>Quiz yakunlandi!</b>\n\n"
        f"📊 <b>Natijalar:</b>\n"
        f"✅ To'g'ri: {correct}/{total}\n"
        f"❌ Noto'g'ri: {data['wrong']}/{total}\n"
        f"📈 Ball: {score:.1f}%  {grade}\n\n"
        f"⚡ +{xp_earned} XP qo'shildi!\n\n"
        f"{'🔥 Ajoyib natija!' if score >= 80 else '💪 Davom eting, kuchayib borasiz!'}"
    )

    await state.clear()
    await message.edit_text(result_text, reply_markup=get_quiz_result_keyboard(
        quiz_id=data["quiz"]["id"],
        score=score,
        results=data["results"]
    ))
```

---

## PHASE 7 — PAYMENT SYSTEM

### Goal
Build payment provider abstraction with webhook handling.

### 7.1 Base Provider
```python
# app/payments/base_provider.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentIntent:
    payment_id: str
    amount_uzs: float
    user_id: str
    plan_id: str
    redirect_url: str
    metadata: dict


@dataclass
class PaymentResult:
    external_id: str
    status: str  # completed | failed | pending
    amount: float
    provider_response: dict


class BasePaymentProvider(ABC):
    @abstractmethod
    async def create_payment(self, intent: PaymentIntent) -> dict:
        """Returns payment URL or invoice data."""
        ...

    @abstractmethod
    async def verify_payment(self, webhook_data: dict) -> PaymentResult:
        """Verify incoming webhook and extract result."""
        ...

    @abstractmethod
    async def refund(self, external_id: str, amount: float) -> bool:
        ...
```

### 7.2 Telegram Stars Provider
```python
# app/payments/telegram_stars.py
from app.payments.base_provider import BasePaymentProvider, PaymentIntent, PaymentResult


class TelegramStarsProvider(BasePaymentProvider):
    # 1 Star = ~13 UZS (approximate, configurable)

    async def create_invoice(self, intent: PaymentIntent) -> dict:
        """Bot sends invoice via send_invoice Aiogram method."""
        stars_amount = int(intent.amount_uzs / 13)  # Configurable rate
        return {
            "title": "QuizMaster AI Premium",
            "description": f"Plan: {intent.metadata.get('plan_name')}",
            "payload": str(intent.payment_id),
            "currency": "XTR",
            "prices": [{"label": "Total", "amount": stars_amount}],
        }

    async def verify_payment(self, webhook_data: dict) -> PaymentResult:
        return PaymentResult(
            external_id=webhook_data["telegram_payment_charge_id"],
            status="completed",
            amount=webhook_data["total_amount"],
            provider_response=webhook_data,
        )

    async def refund(self, external_id: str, amount: float) -> bool:
        # Telegram Stars refund via refund_star_payment API
        return True
```

### 7.3 Payment Service
```python
# app/services/payment_service.py
class PaymentService:
    async def initiate_payment(
        self, user_id: str, plan_id: str, provider_name: str
    ) -> dict:
        """
        1. Load plan details
        2. Check provider is enabled
        3. Create payment record (status=pending)
        4. Call provider.create_payment()
        5. Return payment URL/invoice data
        """
        pass

    async def handle_webhook(
        self, provider_name: str, webhook_data: dict
    ) -> dict:
        """
        1. Find provider
        2. Verify payment signature
        3. Update payment record
        4. If completed: activate subscription, grant credits
        5. Send Telegram notification to user
        6. Return appropriate HTTP response
        """
        pass

    async def activate_subscription(
        self, user_id: str, plan_id: str, payment_id: str
    ):
        """
        1. Create/extend subscription
        2. Add credits (plan.credits + plan.bonus_credits)
        3. Record credit transaction
        4. Record audit log
        5. Check achievements (first purchase, etc.)
        6. Notify via Telegram
        """
        pass
```

---

## PHASE 8 — GAMIFICATION ENGINE

### Goal
XP system, streaks, achievements, leaderboard.

### 8.1 Gamification Service
```python
# app/services/gamification_service.py
from datetime import date, timedelta
from typing import List
from app.repositories.user_repo import UserRepository
from app.repositories.achievement_repo import AchievementRepository
from app.services.notification_service import NotificationService


class GamificationService:
    XP_TABLE = {
        "correct_answer": 10,
        "quiz_complete": 50,
        "exam_complete": 100,
        "flashcard_session": 20,
        "daily_login": 5,
        "upload_document": 15,
        "perfect_quiz": 100,      # 100% score
        "streak_7_day": 200,
        "streak_30_day": 1000,
    }

    LEVEL_THRESHOLDS = [
        0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500,
        5500, 7000, 9000, 11000, 14000, 17000, 20000, 24000, 29000, 35000
    ]

    async def award_xp(
        self,
        user_id: str,
        action: str,
        amount: int = None,
        db=None
    ) -> dict:
        """Award XP and check for level up."""
        xp = amount or self.XP_TABLE.get(action, 0)
        user_repo = UserRepository(db)

        user = await user_repo.get(user_id)
        old_level = self._compute_level(user.xp_points)
        new_xp = user.xp_points + xp
        new_level = self._compute_level(new_xp)

        await user_repo.update(user_id, {"xp_points": new_xp})

        result = {"xp_awarded": xp, "total_xp": new_xp, "leveled_up": False}

        if new_level > old_level:
            result["leveled_up"] = True
            result["new_level"] = new_level
            # Notify user of level up

        return result

    def _compute_level(self, xp: int) -> int:
        for level, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if xp < threshold:
                return level
        return len(self.LEVEL_THRESHOLDS)

    async def update_streak(self, user_id: str, db=None):
        """Call on every user activity. Update daily/weekly streaks."""
        user_repo = UserRepository(db)
        user = await user_repo.get(user_id)
        today = date.today()

        if user.last_activity_date == today:
            return  # Already active today

        if user.last_activity_date == today - timedelta(days=1):
            # Consecutive day
            new_streak = user.daily_streak + 1
        else:
            new_streak = 1  # Reset

        longest = max(user.longest_streak, new_streak)
        await user_repo.update(user_id, {
            "daily_streak": new_streak,
            "longest_streak": longest,
            "last_activity_date": today,
        })

        # Check streak achievements
        if new_streak in [7, 30, 100]:
            await self.check_and_award_achievement(
                user_id, f"streak_{new_streak}_day", db
            )

    async def check_and_award_achievement(
        self, user_id: str, achievement_slug: str, db=None
    ):
        """Award achievement if not already earned."""
        ach_repo = AchievementRepository(db)
        achievement = await ach_repo.get_by_slug(achievement_slug)
        if not achievement:
            return

        already_earned = await ach_repo.user_has_achievement(user_id, achievement.id)
        if already_earned:
            return

        await ach_repo.award_to_user(user_id, achievement.id)

        # Grant rewards
        if achievement.credit_reward > 0:
            await credit_service.add_credits(
                user_id, achievement.credit_reward, "achievement_bonus"
            )

        if achievement.xp_reward > 0:
            await self.award_xp(user_id, "achievement", achievement.xp_reward, db)

        # Notify user
        await NotificationService().send_achievement_notification(
            user_id, achievement
        )
```

### 8.2 Default Achievements to Seed
```python
ACHIEVEMENTS = [
    {"slug": "first_upload", "name": "📤 Birinchi Yuklash", "description": "Birinchi hujjat yukladingiz", "xp_reward": 50, "credit_reward": 10, "condition_type": "uploads_count", "condition_value": 1},
    {"slug": "first_quiz", "name": "📝 Birinchi Quiz", "description": "Birinchi quiz yechildi", "xp_reward": 50, "credit_reward": 10, "condition_type": "quizzes_completed", "condition_value": 1},
    {"slug": "first_perfect", "name": "💯 Mukammal!", "description": "100% ball yig'ildi", "xp_reward": 200, "credit_reward": 20, "condition_type": "perfect_quizzes", "condition_value": 1},
    {"slug": "streak_7_day", "name": "🔥 Haftalik Seriya", "description": "7 kun ketma-ket", "xp_reward": 200, "credit_reward": 30, "condition_type": "streak", "condition_value": 7},
    {"slug": "streak_30_day", "name": "👑 Oylik Seriya", "description": "30 kun ketma-ket", "xp_reward": 1000, "credit_reward": 100, "condition_type": "streak", "condition_value": 30},
    {"slug": "answers_100", "name": "🎯 100 Javob", "description": "100 ta to'g'ri javob", "xp_reward": 300, "credit_reward": 50, "condition_type": "correct_answers", "condition_value": 100},
    {"slug": "quiz_master", "name": "🏆 Quiz Master", "description": "50 ta quiz yakunlandi", "xp_reward": 500, "credit_reward": 100, "condition_type": "quizzes_completed", "condition_value": 50},
    {"slug": "knowledge_seeker", "name": "📚 Bilim Izlovchi", "description": "10 ta fayl yuklandi", "xp_reward": 200, "credit_reward": 30, "condition_type": "uploads_count", "condition_value": 10},
    {"slug": "social_butterfly", "name": "🦋 Referral Ustasi", "description": "5 ta do'st taklif qilindi", "xp_reward": 300, "credit_reward": 50, "condition_type": "referrals_count", "condition_value": 5},
    {"slug": "exam_champion", "name": "🎖️ Imtihon Chempioni", "description": "10 ta imtihon o'tildi", "xp_reward": 400, "credit_reward": 80, "condition_type": "exams_completed", "condition_value": 10},
]
```

---

## PHASE 9 — ADMIN PANEL

### Goal
Build a complete React-based admin SaaS dashboard.

### 9.1 Tech Stack for Admin
```
React 18 + Vite
TailwindCSS
Recharts (charts)
React Query (data fetching)
React Router v6
shadcn/ui (components)
Lucide Icons
```

### 9.2 Admin Panel Pages

#### Dashboard Page — Key Metrics
Displays:
- KPI cards: Total Users, Active Today/Week/Month
- Revenue cards: Today / Week / Month / All Time
- AI Cost cards: Today / Month + Net Profit
- Charts: User Growth (line), Revenue (bar), AI Costs (area)
- Recent uploads table
- Recent payments table
- Live user count (WebSocket)

#### Users Page
- Searchable, filterable user table
- Columns: Avatar, Name, Telegram ID, Credits, Plan, Joined, Last Active, Status
- Actions: View Profile, Grant Credits, Ban/Unban, Grant Premium, Delete
- User detail modal with full history

#### Plans Page
- List of all plans with toggle active/inactive
- Create Plan form: Name, Price, Duration, Credits, Bonus Credits, Features (tag input)
- Edit in-place
- Delete with confirmation

#### Analytics Page
- DAU/WAU/MAU charts
- Retention cohort table (heatmap)
- Conversion rate funnel
- File type distribution (pie chart)
- Subject popularity (bar chart)
- Quiz completion rate over time

#### Broadcasts Page
- Compose: Select content type (Text/Photo/Video/Document)
- Target segment selector
- Schedule or send immediately
- History table with delivery stats (sent/failed %)

#### Channels Page
- List mandatory channels
- Add channel (by username or ID)
- Enable/Disable toggle
- Reorder drag-and-drop

#### AI Monitor Page
- Token usage today/week/month
- Cost breakdown by operation type (pie chart)
- Requests timeline chart
- API key status indicators
- Alert thresholds configuration
- Unusual activity detector

#### Settings Page
Grouped settings:
- **Credit Economy**: Set credit cost for each AI operation
- **Free User Model**: Welcome credits, daily bonus
- **Referral System**: Referrer/referred rewards
- **Payment Providers**: Enable/disable each, set credentials
- **Mandatory Channels**: Already covered in Channels page
- **AI Configuration**: Model selection, temperature

#### Owner Page (Owner Only)
- API Keys management (add/remove/rotate Gemini keys)
- Database backup/restore
- Export Users (CSV)
- Export Analytics (CSV)
- System Health Monitor
- Error Logs viewer

### 9.3 Admin Authentication
```python
# app/api/admin/auth.py
@router.post("/login")
async def admin_login(
    telegram_id: int,
    admin_secret: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin must be in ADMIN_TELEGRAM_IDS list AND
    know the admin secret key.
    Returns short-lived JWT with is_admin=True claim.
    """
    if telegram_id not in settings.ADMIN_TELEGRAM_IDS:
        raise HTTPException(403, "Access denied")
    if admin_secret != settings.ADMIN_SECRET_KEY:
        raise HTTPException(403, "Invalid secret")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_telegram_id(telegram_id)

    token = create_access_token({
        "sub": str(user.id),
        "is_admin": True,
        "exp_override": 86400  # 24 hours for admin
    })
    return {"access_token": token}
```

---

## PHASE 10 — ANALYTICS & MONITORING

### Goal
Track all metrics, generate reports, send alerts.

### 10.1 Analytics Aggregation (Celery Beat Tasks)
```python
# app/tasks/analytics_tasks.py
from app.tasks.celery_app import celery_app


@celery_app.task(name="tasks.aggregate_daily_analytics")
def aggregate_daily_analytics():
    """
    Runs at midnight UTC every day.
    Aggregates yesterday's data into daily_analytics table.
    """
    pass


@celery_app.task(name="tasks.check_ai_cost_alerts")
def check_ai_cost_alerts():
    """
    Runs every hour.
    If daily AI cost > threshold, send Telegram alert to owner.
    If token usage > 90% of budget, alert.
    """
    pass


@celery_app.task(name="tasks.send_daily_report")
def send_daily_report():
    """
    Send daily summary to owner Telegram account.
    Format:
    📊 QuizMaster AI — Kunlik Hisobot
    👥 Yangi foydalanuvchilar: 45
    📤 Yuklamalar: 123
    💳 Daromad: 150,000 UZS
    🤖 AI narxi: $2.50
    💰 Sof foyda: $10.20
    """
    pass


@celery_app.task(name="tasks.check_subscription_expirations")
def check_subscription_expirations():
    """
    Runs daily.
    Find subscriptions expiring in 3 days.
    Send renewal reminder to users.
    """
    pass


@celery_app.task(name="tasks.reset_daily_bonuses")
def reset_daily_bonuses():
    """
    Grant daily bonus credits to eligible users.
    """
    pass
```

### 10.2 Celery Beat Schedule
```python
# app/tasks/scheduler.py
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "aggregate-daily-analytics": {
        "task": "tasks.aggregate_daily_analytics",
        "schedule": crontab(hour=0, minute=5),
    },
    "check-ai-cost-alerts": {
        "task": "tasks.check_ai_cost_alerts",
        "schedule": crontab(minute=0),  # Every hour
    },
    "daily-report": {
        "task": "tasks.send_daily_report",
        "schedule": crontab(hour=7, minute=0),  # 7am Tashkent time
    },
    "check-subscription-expirations": {
        "task": "tasks.check_subscription_expirations",
        "schedule": crontab(hour=8, minute=0),
    },
    "reset-daily-bonuses": {
        "task": "tasks.reset_daily_bonuses",
        "schedule": crontab(hour=0, minute=0),
    },
    "cleanup-temp-files": {
        "task": "tasks.cleanup_temp_files",
        "schedule": crontab(hour=3, minute=0),
    },
}
```

### 10.3 Structured Logging
```python
# app/core/logging.py
import structlog
import logging


def setup_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    return structlog.get_logger(name)
```

---

## PHASE 11 — SECURITY HARDENING

### Goal
Implement all security layers.

### 11.1 Rate Limiting
```python
# app/middleware/rate_limit_middleware.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI

limiter = Limiter(key_func=get_remote_address)

def setup_rate_limiting(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Usage on routes:
# @limiter.limit("10/minute")  # Auth endpoints
# @limiter.limit("100/minute") # Regular endpoints
# @limiter.limit("5/minute")   # Payment endpoints
```

### 11.2 Anti-Abuse Checks

```python
# app/services/anti_abuse_service.py
import redis.asyncio as aioredis

class AntiAbuseService:
    DUPLICATE_WINDOW = 60  # seconds

    async def check_duplicate_request(
        self, user_id: str, content_hash: str
    ) -> bool:
        """Prevent same user uploading same file multiple times in 60s."""
        key = f"upload:dedup:{user_id}:{content_hash}"
        result = await self.redis.set(key, "1", nx=True, ex=self.DUPLICATE_WINDOW)
        return result is None  # True = duplicate (blocked)

    async def check_credit_abuse(self, user_id: str) -> bool:
        """Flag unusual credit spending patterns."""
        key = f"credits:spend:{user_id}:{date.today()}"
        daily_spend = await self.redis.get(key)
        return int(daily_spend or 0) > 5000  # Configurable threshold

    async def check_referral_abuse(
        self, referrer_id: str, referred_telegram_id: int
    ) -> bool:
        """Detect self-referral via multiple accounts."""
        # Check if referred_telegram_id IP matches referrer's known IPs
        # Simplified: flag if referred user joined < 1 min after referrer
        pass
```

### 11.3 Input Validation

All file uploads must be validated:
- File type check by MAGIC BYTES (not just extension or MIME)
- File size limits enforced
- Filename sanitized
- Extracted text sanitized with bleach before storage

```python
# app/utils/validators.py
import magic

ALLOWED_MAGIC_BYTES = {
    "pdf": [b"%PDF"],
    "docx": [b"PK\x03\x04"],
    "pptx": [b"PK\x03\x04"],
    "txt": None,  # Skip magic check
    "html": None,
}

def validate_file_type(file_bytes: bytes, claimed_type: str) -> bool:
    """Validate file by magic bytes, not just extension."""
    magic_bytes = ALLOWED_MAGIC_BYTES.get(claimed_type)
    if magic_bytes is None:
        return True
    return any(file_bytes.startswith(mb) for mb in magic_bytes)
```

---

## PHASE 12 — DEVOPS & DEPLOYMENT

### Goal
Production-ready deployment on Linux VPS.

### 12.1 Nginx Configuration
```nginx
# nginx/conf.d/quizmaster.conf
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    add_header Content-Security-Policy "default-src 'self'";

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=upload:10m rate=10r/m;

    # Backend API
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        client_max_body_size 55M;
    }

    # Bot webhook
    location /webhook/bot {
        proxy_pass http://bot:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Admin panel (static files)
    location /admin/ {
        root /app/static;
        try_files $uri $uri/ /admin/index.html;
    }

    # Payment webhooks — higher rate limit
    location /api/v1/webhooks/ {
        limit_req zone=api burst=50 nodelay;
        proxy_pass http://backend:8000;
    }
}
```

### 12.2 Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Deploying QuizMaster AI..."

# Pull latest code
git pull origin main

# Build images
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# Restart services
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Health check
sleep 10
curl -f http://localhost/health || (echo "❌ Health check failed" && exit 1)

echo "✅ Deployment successful!"
```

### 12.3 Database Backup Script
```bash
#!/bin/bash
# scripts/backup_db.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="quizmaster_backup_${DATE}.sql.gz"

mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U quizmaster quizmaster_db | \
    gzip > "${BACKUP_DIR}/${FILENAME}"

echo "✅ Backup created: ${FILENAME}"

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
echo "🧹 Old backups cleaned"
```

### 12.4 System Health Monitor Endpoint
```python
# app/api/admin/owner.py
@router.get("/health")
async def system_health(current_user = Depends(require_owner)):
    """Returns system health metrics."""
    import psutil

    db_ok = await check_db_connection()
    redis_ok = await check_redis_connection()

    return {
        "status": "ok" if all([db_ok, redis_ok]) else "degraded",
        "database": "ok" if db_ok else "error",
        "redis": "ok" if redis_ok else "error",
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "uptime_seconds": int(time.time() - START_TIME),
    }
```

---

## PHASE 13 — TESTING

### Goal
Comprehensive test coverage.

### 13.1 Test Configuration
```python
# backend/tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.base import Base
from main import app

TEST_DB_URL = "postgresql+asyncpg://quizmaster:password@localhost:5432/quizmaster_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    async_session = async_sessionmaker(test_engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
```

### 13.2 Key Tests to Write

```python
# backend/tests/unit/test_credit_service.py
async def test_deduct_credits_success()
async def test_deduct_credits_insufficient()
async def test_add_credits_records_transaction()
async def test_credit_balance_never_negative()

# backend/tests/unit/test_ai_generators.py
async def test_quiz_generation_returns_valid_json()
async def test_flashcard_generation_correct_count()
async def test_summary_contains_key_concepts()
async def test_cache_hit_skips_api_call()

# backend/tests/unit/test_file_parsers.py
async def test_pdf_parser_extracts_text()
async def test_docx_parser_extracts_text()
async def test_image_parser_ocr()
async def test_parser_factory_invalid_type_raises()

# backend/tests/integration/test_upload_flow.py
async def test_upload_pdf_triggers_processing()
async def test_duplicate_file_uses_cache()
async def test_upload_fails_without_credits()
async def test_file_size_limit_enforced()

# backend/tests/integration/test_quiz_flow.py
async def test_generate_quiz_deducts_credits()
async def test_quiz_session_records_results()
async def test_xp_awarded_on_completion()
async def test_achievement_triggered_on_perfect_score()
```

---

## API REFERENCE

### Authentication
```
POST   /api/v1/auth/telegram       — Register/login via Telegram
POST   /api/v1/auth/refresh        — Refresh JWT token
```

### Users
```
GET    /api/v1/users/me            — Current user profile + stats
PATCH  /api/v1/users/me            — Update preferences
GET    /api/v1/users/me/history    — Upload + quiz history
```

### Uploads
```
POST   /api/v1/uploads             — Upload file (multipart)
GET    /api/v1/uploads             — List user's uploads
GET    /api/v1/uploads/{id}        — Upload details + AI content
DELETE /api/v1/uploads/{id}        — Delete upload
```

### Quizzes
```
POST   /api/v1/quizzes             — Generate quiz {upload_id, count, difficulty, types}
GET    /api/v1/quizzes/{id}        — Get quiz with questions
POST   /api/v1/quizzes/sessions    — Start quiz session
PATCH  /api/v1/quizzes/sessions/{id} — Submit session results
GET    /api/v1/quizzes/{id}/explain  — Explain wrong answers
```

### Flashcards
```
POST   /api/v1/flashcards          — Generate flashcard set
GET    /api/v1/flashcards/{id}     — Get flashcard set
POST   /api/v1/flashcards/sessions — Start flashcard session
PATCH  /api/v1/flashcards/sessions/{id} — Update session progress
```

### Summaries
```
POST   /api/v1/summaries           — Generate summary
GET    /api/v1/summaries/{id}      — Get summary
```

### Plans & Subscriptions
```
GET    /api/v1/plans               — List active plans
GET    /api/v1/subscriptions/me    — Current subscription
```

### Credits
```
GET    /api/v1/credits/me          — Balance + transaction history
POST   /api/v1/credits/deduct      — Deduct credits for operation (internal)
```

### Payments
```
POST   /api/v1/payments/initiate   — Start payment {plan_id, provider}
POST   /api/v1/webhooks/click      — Click webhook
POST   /api/v1/webhooks/payme      — Payme webhook
POST   /api/v1/webhooks/uzum       — Uzum webhook
POST   /api/v1/webhooks/telegram-stars — Stars webhook
```

### Referrals
```
GET    /api/v1/referrals/me        — My referral stats
GET    /api/v1/referrals/link      — My referral link
```

### Gamification
```
GET    /api/v1/achievements        — All achievements + earned status
GET    /api/v1/leaderboard         — Top users by XP
GET    /api/v1/leaderboard/weekly  — Weekly leaderboard
```

### Admin Routes (require is_admin JWT claim)
```
GET    /api/admin/dashboard        — All KPIs
GET    /api/admin/users            — User list with filters
PATCH  /api/admin/users/{id}       — Update user (ban, credits, etc.)
GET    /api/admin/plans            — All plans
POST   /api/admin/plans            — Create plan
PATCH  /api/admin/plans/{id}       — Update plan
GET    /api/admin/analytics        — Analytics data with date range
GET    /api/admin/ai-monitor       — AI cost/token data
POST   /api/admin/broadcasts       — Create & send broadcast
GET    /api/admin/settings         — All settings
PATCH  /api/admin/settings/{key}   — Update setting
GET    /api/admin/channels         — Mandatory channels
POST   /api/admin/channels         — Add channel
DELETE /api/admin/channels/{id}    — Remove channel
GET    /api/admin/payments         — Payment history
```

### Owner Routes (require is_owner JWT claim)
```
GET    /api/admin/owner/health     — System health
POST   /api/admin/owner/backup     — Trigger DB backup
GET    /api/admin/owner/keys       — Gemini API keys status
POST   /api/admin/owner/keys       — Add Gemini API key
DELETE /api/admin/owner/keys/{idx} — Remove Gemini API key
GET    /api/admin/owner/export/users     — Export users CSV
GET    /api/admin/owner/export/analytics — Export analytics CSV
```

---

## TELEGRAM BOT FLOW

```
/start
  └─► Auth Middleware (register or login)
  └─► Channel Check (if mandatory channels exist)
       ├─ Not subscribed → Show subscribe buttons → Wait → Re-check
       └─ Subscribed ↓
  └─► Main Menu

Main Menu:
├─► 📤 Hujjat yuklash
│    └─► Accepts: Document | Photo | Text (URL future)
│    └─► Validates: type, size, credits
│    └─► Uploads to backend
│    └─► Celery: Extract text
│    └─► Shows generation options keyboard:
│         [✅ Quiz] [🃏 Flashcard] [📝 Summary] [💡 Tushunchalar]
│         └─► User selects (can select multiple)
│         └─► Celery: Generate AI content
│         └─► Notify user when ready
│         └─► Show content
│
├─► 📚 Mening materiallarim
│    └─► List of uploads (paginated)
│    └─► Select upload → Show generated content
│    └─► For each: Open Quiz / Flashcards / Summary / Exam
│
├─► 📊 Profil
│    └─► Stats: XP, Level, Streak, Credits, Uploads, Quizzes
│    └─► Achievement progress bars
│    └─► Subscription info
│
├─► 🏆 Reyting
│    └─► Global Leaderboard (top 20)
│    └─► Weekly Leaderboard
│    └─► My Rank
│
├─► 🎁 Chegirma kodi
│    └─► Show my referral link
│    └─► Stats: invited / converted / earned credits
│
├─► 💎 Premium
│    └─► Show available plans (from admin-configured)
│    └─► Select plan → Select payment provider
│    └─► Initiate payment
│    └─► Wait for webhook → Notify user
│
└─► ❓ Yordam
     └─► FAQ inline buttons
     └─► Support contact

Quiz Flow:
  Select Quiz → Difficulty picker → Count picker
  → [Savol 1/10] + answer options (inline keyboard)
  → Show ✅/❌ after each answer
  → Final results screen: score, XP, achievements
  → [Qayta urinish] [Yanlishlarni tushuntir] [Bosh menu]

Exam Mode:
  Select Exam → Confirm credit deduction
  → Timer starts (countdown shown in message)
  → Questions one by one (no immediate feedback)
  → Time up or all answered → Show full results
  → Analytics: time per question, topic breakdown

Flashcard Flow:
  Select Set → [Show Front] → [Show Back]
  → Rate: [😅 Qiyin] [🤔 O'rta] [😊 Oson]
  → Track progress → Completion screen
```

---

## ADMIN PANEL DESIGN SPEC

### Color Palette
```css
Primary:    #6366f1  (Indigo)
Secondary:  #8b5cf6  (Purple)
Success:    #10b981  (Emerald)
Warning:    #f59e0b  (Amber)
Danger:     #ef4444  (Red)
Background: #0f172a  (Slate 900) — dark mode
Surface:    #1e293b  (Slate 800)
Card:       #334155  (Slate 700)
Text:       #f1f5f9  (Slate 100)
```

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR (240px)          │  MAIN CONTENT               │
│  ─────────────────────    │  ─────────────────────────  │
│  🎓 QuizMaster AI         │  TOP BAR: Page title + user │
│                           │  ─────────────────────────  │
│  📊 Dashboard             │                             │
│  👥 Foydalanuvchilar      │  PAGE CONTENT               │
│  💎 Rejalar               │  (KPI cards, charts,        │
│  📈 Analitika             │   tables, forms)            │
│  📣 Xabar yuborish        │                             │
│  📢 Kanallar              │                             │
│  💳 To'lovlar             │                             │
│  🤖 AI Monitor            │                             │
│  ⚙️  Sozlamalar           │                             │
│  👑 Owner Panel           │                             │
│                           │                             │
│  ─────────────────────    │                             │
│  Admin: John Doe          │                             │
└─────────────────────────────────────────────────────────┘
```

### Dashboard KPI Cards (Row 1)
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 👥 Jami      │ │ 🟢 Bugun    │ │ 📅 Bu hafta │ │ 📆 Bu oy    │
│ Foydalanuvchi│ │ Faol        │ │ Faol        │ │ Faol        │
│   12,450     │ │    234      │ │    1,230    │ │    4,560    │
│  ▲ +5.2%    │ │  ▲ +12%    │ │  ▲ +8%     │ │  ▲ +15%    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### Dashboard KPI Cards (Row 2)
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 💰 Bugungi  │ │ 💰 Haftalik │ │ 💰 Oylik    │ │ 💰 Jami     │
│ Daromad     │ │ Daromad     │ │ Daromad     │ │ Daromad     │
│ 450,000 UZS │ │ 2.1M UZS   │ │ 8.5M UZS   │ │ 45M UZS    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## IMPLEMENTATION CHECKLIST

Work through each item in order. Check off before moving to next.

### Phase 1 — Bootstrap
- [ ] Create root directory structure
- [ ] Write `docker-compose.yml`
- [ ] Write `Makefile`
- [ ] Write `backend/Dockerfile`
- [ ] Write `bot/Dockerfile`
- [ ] Write `backend/requirements.txt`
- [ ] Write `bot/requirements.txt`
- [ ] Write `.env.example`
- [ ] Write `backend/main.py`
- [ ] Verify: `docker-compose up` runs without errors
- [ ] Verify: `GET /health` returns 200

### Phase 2 — Database
- [ ] Write all SQLAlchemy models (18 models)
- [ ] Write `app/db/base.py` and `app/db/session.py`
- [ ] Configure Alembic
- [ ] Generate initial migration
- [ ] Run migration: `alembic upgrade head`
- [ ] Write `scripts/seed_data.py` and run it
- [ ] Write all repositories (BaseRepository + 14 specific)
- [ ] Verify: All tables created with correct schema

### Phase 3 — Core API
- [ ] Write `app/core/config.py`
- [ ] Write `app/core/security.py` (JWT)
- [ ] Write `app/core/exceptions.py`
- [ ] Write `app/core/dependencies.py`
- [ ] Write all Pydantic schemas (15 schema files)
- [ ] Write all service layer files (20 service files)
- [ ] Write all API route files (14 user routes + 10 admin routes)
- [ ] Write middleware (auth, rate limit, logging, CORS, audit)
- [ ] Verify: Auth flow works end-to-end
- [ ] Verify: CRUD operations work via Postman/httpie

### Phase 4 — AI Engine
- [ ] Write `app/ai/gemini_client.py` with key rotation
- [ ] Write `app/ai/prompt_builder.py` with all prompts
- [ ] Write `app/ai/quiz_generator.py`
- [ ] Write `app/ai/flashcard_generator.py`
- [ ] Write `app/ai/summary_generator.py`
- [ ] Write `app/ai/concept_extractor.py`
- [ ] Write `app/ai/definition_extractor.py`
- [ ] Write `app/ai/adaptive_engine.py`
- [ ] Write `app/ai/exam_engine.py`
- [ ] Write `app/ai/content_hasher.py`
- [ ] Write `app/ai/token_tracker.py`
- [ ] Write `app/services/cache_service.py`
- [ ] Verify: Quiz generation returns valid JSON
- [ ] Verify: Cache returns same result for same content

### Phase 5 — File Processing
- [ ] Write `app/file_processing/pdf_parser.py`
- [ ] Write `app/file_processing/docx_parser.py`
- [ ] Write `app/file_processing/pptx_parser.py`
- [ ] Write `app/file_processing/txt_parser.py`
- [ ] Write `app/file_processing/html_parser.py`
- [ ] Write `app/file_processing/image_parser.py`
- [ ] Write `app/file_processing/parser_factory.py`
- [ ] Write `app/file_processing/text_cleaner.py`
- [ ] Write `app/services/storage_service.py`
- [ ] Write `app/tasks/celery_app.py`
- [ ] Write `app/tasks/file_tasks.py`
- [ ] Write `app/tasks/ai_tasks.py`
- [ ] Verify: Upload PDF → text extracted → AI content generated

### Phase 6 — Telegram Bot
- [ ] Write `bot/main.py` with webhook setup
- [ ] Write all middlewares (auth, channel check, rate limit, anti-spam, i18n)
- [ ] Write all handlers (start, upload, quiz, flashcard, summary, exam, profile, subscription, referral, achievements, leaderboard, settings, help)
- [ ] Write all keyboards (main menu, quiz, flashcard, exam, subscription, etc.)
- [ ] Write all FSM states
- [ ] Write `bot/services/api_client.py`
- [ ] Write `bot/locales/uz.json`, `ru.json`, `en.json`
- [ ] Verify: `/start` flow works
- [ ] Verify: File upload → AI content generated → User receives result
- [ ] Verify: Quiz flow works end-to-end
- [ ] Verify: Payment flow works (Telegram Stars)

### Phase 7 — Payments
- [ ] Write `app/payments/base_provider.py`
- [ ] Write `app/payments/telegram_stars.py`
- [ ] Write `app/payments/click.py`
- [ ] Write `app/payments/payme.py`
- [ ] Write `app/payments/uzum.py`
- [ ] Write `app/payments/paynet.py`
- [ ] Write `app/payments/payment_router.py`
- [ ] Write `app/services/payment_service.py`
- [ ] Write webhook handlers for each provider
- [ ] Verify: Payment creates subscription and adds credits

### Phase 8 — Gamification
- [ ] Write `app/services/gamification_service.py`
- [ ] Write `app/services/leaderboard_service.py`
- [ ] Write `app/services/achievement_service.py`
- [ ] Seed achievements data
- [ ] Verify: XP awarded on quiz completion
- [ ] Verify: Streak updates on daily activity
- [ ] Verify: Achievements unlock correctly
- [ ] Verify: Leaderboard shows correct rankings

### Phase 9 — Admin Panel
- [ ] Bootstrap React + Vite + Tailwind project
- [ ] Write admin login page
- [ ] Write Dashboard page with charts
- [ ] Write Users management page
- [ ] Write Plans management page
- [ ] Write Analytics page
- [ ] Write Broadcasts page
- [ ] Write Channels page
- [ ] Write AI Monitor page
- [ ] Write Settings page
- [ ] Write Owner Panel page
- [ ] Build Docker image for admin panel
- [ ] Verify: All admin pages load and display correct data

### Phase 10 — Analytics & Monitoring
- [ ] Write `app/tasks/analytics_tasks.py`
- [ ] Write `app/tasks/notification_tasks.py`
- [ ] Write `app/tasks/cleanup_tasks.py`
- [ ] Write `app/tasks/scheduler.py` (Celery Beat config)
- [ ] Verify: Daily analytics aggregation runs
- [ ] Verify: Owner receives daily Telegram report
- [ ] Verify: Low credit alerts sent correctly

### Phase 11 — Security
- [ ] Implement rate limiting on all endpoints
- [ ] Implement file magic byte validation
- [ ] Implement duplicate upload detection
- [ ] Implement credit abuse detection
- [ ] Implement referral abuse detection
- [ ] Implement RBAC (user/admin/owner roles)
- [ ] Implement audit logging for all admin actions
- [ ] Run security checklist (SQL injection, XSS, CSRF)
- [ ] Verify: No sensitive data in logs

### Phase 12 — DevOps
- [ ] Write `docker-compose.prod.yml`
- [ ] Write `nginx/conf.d/quizmaster.conf`
- [ ] Configure SSL certificates
- [ ] Write `scripts/deploy.sh`
- [ ] Write `scripts/backup_db.sh`
- [ ] Write `scripts/health_check.sh`
- [ ] Configure log rotation
- [ ] Set up automated daily backups via cron
- [ ] Verify: Full production deployment works
- [ ] Verify: SSL works correctly
- [ ] Verify: Health endpoint returns 200

### Phase 13 — Testing
- [ ] Write unit tests for AI generators
- [ ] Write unit tests for file parsers
- [ ] Write unit tests for credit service
- [ ] Write unit tests for gamification
- [ ] Write unit tests for payment providers
- [ ] Write integration tests for auth flow
- [ ] Write integration tests for upload flow
- [ ] Write integration tests for quiz flow
- [ ] Write integration tests for payment flow
- [ ] Achieve >80% code coverage
- [ ] All tests pass: `pytest tests/ -v --cov`

---

## EXTRA FEATURES (Bonus Implementations)

These are additional features beyond the base spec that will make the product significantly better.

### 1. Study Schedule AI
After user completes a quiz with weak scores, AI generates a personalized study plan with recommended topics and daily goals.

### 2. Collaborative Study Groups (Future)
Users can create study groups. Shared quiz results and group leaderboard.

### 3. Smart Notifications
- "You haven't studied in 2 days! Your streak is at risk 🔥"
- "5 users solved your uploaded material's quiz today"
- "New achievement available: Complete 5 more quizzes for Quiz Master"

### 4. Multi-Language AI Generation
Quiz and flashcards generated in user's preferred language. Detected automatically from document + user preference.

### 5. PDF Report Generation
After exam completion, generate PDF report with:
- Score breakdown
- Wrong answers with explanations
- Personalized improvement tips
- QR code to retake quiz

### 6. Streak Insurance
Users can buy "streak protection" with credits — if they miss a day, streak stays intact.

### 7. Dark Mode Admin Panel
Toggle between light/dark mode. State saved to localStorage.

### 8. Real-time Dashboard Updates
WebSocket connection on admin dashboard. New users, payments, uploads appear live without page refresh.

### 9. A/B Test Plan Pricing
Admin can create A/B test variants for plan pricing. System shows different prices to different user segments and tracks conversion.

### 10. Voice Note Support (Future)
User sends voice note → Gemini transcribes → Quiz generated from transcript.

---

## FINAL NOTES FOR AGENT

1. **Never hardcode values** that admins should control. Every threshold, credit cost, message text goes through the `settings` table.

2. **Every AI call must be tracked** in `ai_usage_logs`. No exception. This is how we calculate profitability.

3. **Every credit movement must be recorded** in `credit_transactions`. No direct balance manipulation without a transaction record.

4. **Celery tasks are idempotent**. If a task runs twice (e.g., after retry), it must not create duplicate data. Use database constraints and "check before insert" logic.

5. **The payment webhook handler is the most critical code path.** It must be bulletproof. Use database transactions. If subscription activation fails, the payment must not be marked as completed.

6. **File storage is abstracted.** Never call `open()` directly in services. Always go through `StorageService`. This makes S3 migration a single file change.

7. **Gemini prompts always expect JSON responses.** Always wrap in try/except when parsing. If JSON parsing fails, retry with a cleaner prompt.

8. **Bot handlers should be thin.** Business logic belongs in services. Handlers only translate Telegram events to service calls and format responses.

9. **Admin panel is a separate app.** It consumes the same FastAPI backend via REST. No server-side rendering. Pure React SPA.

10. **Test first, then ship.** Each phase has test verification steps. Do not skip them.

---

*QuizMaster AI Blueprint — Complete. Start with Phase 1.*