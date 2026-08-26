"""Configuration management using Pydantic Settings.

Loads environment variables from .env with fallback defaults for all
PlacementPro services: MongoDB, JWT, OpenRouter AI, PayPal, Stripe,
Redis, RabbitMQ, Docker sandbox, WebSocket, CORS, and more.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    Attributes are organized by domain:
        - MongoDB / Database connection
        - JWT authentication
        - OpenRouter AI configuration
        - PayPal / Stripe billing
        - Free tier feature limits
        - CORS policy
        - Rate limiting
        - Referral program
        - Revenue targets
        - Code execution (Piston API, local/remote sandboxes)
        - RabbitMQ async job queue
        - Docker sandbox settings
        - WebSocket real-time updates
        - Security and password policies
        - Email (SMTP)
        - Logging
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # API Versioning
    API_VERSION: str = "v1"

    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "placementpro"
    MONGODB_MAX_POOL_SIZE: int = 50
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_IDLE_TIME_MS: int = 10000
    REDIS_URL: str = os.getenv("REDIS_URL", "")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_DAYS: int = 7
    JWT_REFRESH_EXPIRY_DAYS: int = 30
    
    # OpenRouter AI
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-001"
    OPENROUTER_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_TIMEOUT: int = 30
    OPENROUTER_MAX_RETRIES: int = 3
    
    # PayPal
    PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID", "")
    PAYPAL_CLIENT_SECRET: str = os.getenv("PAYPAL_CLIENT_SECRET", "")
    PAYPAL_MODE: str = os.getenv("PAYPAL_MODE", "sandbox")
    PAYPAL_WEBHOOK_ID: str = os.getenv("PAYPAL_WEBHOOK_ID", "")

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/google/callback")
    
    # Free tier limits
    FREE_TIER_INTERVIEW_LIMIT: int = 3
    FREE_TIER_RESUME_LIMIT: int = 3
    FREE_TIER_APTITUDE_LIMIT: int = 5
    FREE_TIER_COVER_LETTER_LIMIT: int = 3
    FREE_TIER_CODING_LIMIT: int = 5
    FREE_TIER_COMPANY_MOCK_LIMIT: int = 1
    FREE_TIER_PREDICTOR_LIMIT: int = 3
    FREE_TIER_QUESTION_BANK_LIMIT: int = 5
    # Daily limits
    FREE_TIER_DAILY_COMPILER_RUNS: int = 20
    FREE_TIER_DAILY_AI_QUESTIONS: int = 5
    FREE_TIER_DAILY_MYSTERY_BOXES: int = 1
    FREE_TIER_DAILY_PROBLEMS: int = 10
    FREE_TIER_DAILY_AI_MISTAKES: int = 3
    FREE_TIER_MOCK_INTERVIEWS_PER_MONTH: int = 1
    FREE_TIER_STREAK_REPAIRS: int = 1
    FREE_TIER_INTERVIEW_BOOKING_LIMIT: int = 3
    # Free can only mock/predict these companies
    FREE_TIER_COMPANIES: str = "tcs,infosys,wipro"
    # Admin emails allowed to reset usage
    ADMIN_EMAILS: str = "sridevi72901@gmail.com"
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    CORS_ALLOW_CREDENTIALS: bool = True
    # Auth cookie SameSite. Use "none" when the frontend is hosted on a
    # different origin than the API (e.g. Vercel frontend + Render backend).
    COOKIE_SAMESITE: str = os.getenv("COOKIE_SAMESITE", "lax")
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS: list[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Request-ID",
        "X-Requested-With",
        "Cache-Control",
        "Pragma",
    ]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    RATE_LIMIT_LOGIN_LOCKOUT: int = 900  # 15 minutes
    
# Stripe (secondary payment processor)
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_MODE: str = os.getenv("STRIPE_MODE", "sandbox")

    # Referral program
    REFERRAL_REWARD_TYPE: str = os.getenv("REFERRAL_REWARD_TYPE", "days")  # "days" or "percent"
    REFERRAL_REWARD_VALUE: int = int(os.getenv("REFERRAL_REWARD_VALUE", "30"))  # days or percent
    REFERRAL_MAX_REWARDS_PER_USER: int = int(os.getenv("REFERRAL_MAX_REWARDS_PER_USER", "12"))
    REFERRAL_MIN_DAYS_USED: int = int(os.getenv("REFERRAL_MIN_DAYS_USED", "30"))

    # Revenue tracking
    REVENUE_TARGET_ANNUAL: int = int(os.getenv("REVENUE_TARGET_ANNUAL", "2000000"))
    MRR_TARGET: int = int(os.getenv("MRR_TARGET", "166667"))
    ARPU_TARGET: float = float(os.getenv("ARPU_TARGET", "12.00"))
    CHURN_TARGET: float = float(os.getenv("CHURN_TARGET", "0.05"))  # 5% monthly churn target

    # Coupons
    COUPON_MAX_USES: int = int(os.getenv("COUPON_MAX_USES", "1000"))
    COUPON_DEFAULT_DISCOUNT_PERCENT: int = int(os.getenv("COUPON_DEFAULT_DISCOUNT_PERCENT", "20"))

    # API product pricing
    API_PRICE_PER_1K_REQUESTS: float = float(os.getenv("API_PRICE_PER_1K_REQUESTS", "0.50"))
    API_MONTHLY_BASE: float = float(os.getenv("API_MONTHLY_BASE", "49.00"))

    # White-label licensing
    WHITE_LABEL_PRICE_MONTHLY: float = float(os.getenv("WHITE_LABEL_PRICE_MONTHLY", "299.00"))
    WHITE_LABEL_PRICE_ANNUAL: float = float(os.getenv("WHITE_LABEL_PRICE_ANNUAL", "2499.00"))

    # Merch store
    MERCH_ENABLED: bool = os.getenv("MERCH_ENABLED", "false").lower() == "true"
    MERCH_BASE_URL: str = os.getenv("MERCH_BASE_URL", "")

    # Code Execution (Piston API)
    PISTON_API_URL: str = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston/execute")
    PISTON_API_KEY: str = os.getenv("PISTON_API_KEY", "")
    PISTON_TIMEOUT: int = 30
    # Local sandboxed fallback for code execution when Piston is rate-limited/down.
    # Self-hosted, zero egress: runs code in a restricted subprocess with resource limits.
    USE_LOCAL_SANDBOX: bool = os.getenv("USE_LOCAL_SANDBOX", "false").lower() == "true"
    SANDBOX_TIMEOUT: int = int(os.getenv("SANDBOX_TIMEOUT", "5"))
    # Free remote fallbacks (Wandbox + Glot.io) tried after Piston and before the
    # local sandbox. Best-effort public APIs with per-IP limits — not a security boundary.
    USE_REMOTE_FALLBACKS: bool = os.getenv("USE_REMOTE_FALLBACKS", "false").lower() == "true"
    REMOTE_FALLBACK_TIMEOUT: int = int(os.getenv("REMOTE_FALLBACK_TIMEOUT", "8"))
    # Optional free Glot.io API token (from glot.io account) — anonymous calls also work.
    GLOT_API_TOKEN: str = os.getenv("GLOT_API_TOKEN", "")
    
    # RabbitMQ for async job queue
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    RABBITMQ_EXECUTION_QUEUE: str = "code_execution"
    RABBITMQ_RESULT_EXCHANGE: str = "code_execution_results"
    RABBITMQ_WORKER_CONCURRENCY: int = 4
    RABBITMQ_PREFETCH_COUNT: int = 8
    
    # Docker sandbox for secure code execution
    DOCKER_SANDBOX_ENABLED: bool = os.getenv("DOCKER_SANDBOX_ENABLED", "false").lower() == "true"
    DOCKER_SANDBOX_IMAGE: str = os.getenv("DOCKER_SANDBOX_IMAGE", "placementpro/sandbox:latest")
    DOCKER_SANDBOX_CPU_QUOTA: int = 50000  # 50% CPU
    DOCKER_SANDBOX_MEMORY_LIMIT: str = "256m"
    DOCKER_SANDBOX_PIDS_LIMIT: int = 64
    DOCKER_SANDBOX_NETWORK_DISABLED: bool = True
    DOCKER_SANDBOX_READ_ONLY_ROOTFS: bool = True
    DOCKER_SANDBOX_TMPFS: str = "/tmp:noexec,nosuid,size=50m"

# WebSocket for real-time updates
    WS_ENABLED: bool = os.getenv("WS_ENABLED", "true").lower() == "true"
    WS_PING_INTERVAL: int = 15  # seconds - reduced for faster detection
    WS_MAX_CONNECTIONS: int = 50000  # increased for scale; Redis-backed in production

# Email (optional)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@placementpro.app")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "placementpro.log")

    # Security
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_REQUIRE_NUMBER: bool = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached Settings instance.

    Creates a singleton Settings object using lru_cache so environment variables
    are read only once per process. If JWT_SECRET is missing, generates an
    ephemeral secret and logs a warning (sessions are invalidated on restart).

    Returns:
        Settings: Cached application settings instance.
    """
    settings = Settings()

    if not settings.JWT_SECRET:
        import logging
        logging.getLogger(__name__).warning(
            "JWT_SECRET is not set. Generating an ephemeral secret — "
            "sessions will be invalidated on every restart. Set JWT_SECRET in .env for production."
        )
        settings.JWT_SECRET = secrets.token_urlsafe(64)

    return settings
