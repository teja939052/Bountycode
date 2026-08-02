from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
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
    FREE_TIER_INTERVIEW_BOOKING_LIMIT: int = 3
    # Free can only mock/predict these companies
    FREE_TIER_COMPANIES: str = "tcs,infosys,wipro"
    # Admin emails allowed to reset usage
    ADMIN_EMAILS: str = ""
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    CORS_ALLOW_CREDENTIALS: bool = True
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
    PISTON_TIMEOUT: int = 30

    # Security
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_REQUIRE_NUMBER: bool = True
    
    # Email (optional)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@placementpro.app")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "placementpro.log")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
