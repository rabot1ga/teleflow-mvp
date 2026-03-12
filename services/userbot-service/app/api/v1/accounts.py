"""API routers for userbot accounts."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session
from app.models.userbot import UserbotAccount, AccountStatus
from app.schemas.userbot import (
    UserbotAccountCreate,
    UserbotAccountResponse,
    UserbotAccountUpdate,
    UserbotAccountAuthRequest,
    UserbotAccountVerifyRequest,
    UserbotAccount2FARequest,
)
from teleflow_common.schemas.responses import StandardResponse

router = APIRouter(prefix="/accounts", tags=["Userbot Accounts"])


@router.post("", response_model=StandardResponse[UserbotAccountResponse])
async def create_account(
    account_data: UserbotAccountCreate,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[UserbotAccountResponse]:
    """Create a new userbot account."""
    account = UserbotAccount(
        project_id=account_data.project_id,
        name=account_data.name,
        status=AccountStatus.NEEDS_AUTH,
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)

    return StandardResponse[UserbotAccountResponse](
        success=True,
        data=UserbotAccountResponse.model_validate(account),
    )


@router.get("", response_model=StandardResponse[list[UserbotAccountResponse]])
async def list_accounts(
    project_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[list[UserbotAccountResponse]]:
    """List all userbot accounts for a project."""
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.project_id == project_id)
    )
    accounts = result.scalars().all()

    return StandardResponse[list[UserbotAccountResponse]](
        success=True,
        data=[UserbotAccountResponse.model_validate(acc) for acc in accounts],
    )


@router.get("/{account_id}", response_model=StandardResponse[UserbotAccountResponse])
async def get_account(
    account_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[UserbotAccountResponse]:
    """Get account by ID."""
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    
    return StandardResponse[UserbotAccountResponse](
        success=True,
        data=UserbotAccountResponse.model_validate(account),
    )


@router.delete("/{account_id}", response_model=StandardResponse[dict])
async def delete_account(
    account_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Delete account by ID."""
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    
    await session.delete(account)
    await session.commit()
    
    return StandardResponse[dict](
        success=True,
        data={"message": "Account deleted"},
    )


@router.post("/{account_id}/send-code", response_model=StandardResponse[dict])
async def send_auth_code(
    account_id: str,
    auth_data: UserbotAccountAuthRequest,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Send authentication code to phone number.

    This initiates the Telegram authentication process.
    """
    import os
    from app.services.telegram_auth import TelegramAuthService
    
    # Get account
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.id == account_id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    # Get API credentials from env
    api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
    api_hash = os.getenv("TELEGRAM_API_HASH", "")

    if not api_id or not api_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram API credentials not configured",
        )

    # Send code
    auth_service = TelegramAuthService(
        api_id=api_id,
        api_hash=api_hash,
        phone=auth_data.phone,
    )

    auth_result = await auth_service.send_code()

    if not auth_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=auth_result["error"],
        )

    # Save phone and code hash to account
    account.auth_phone = auth_data.phone
    account.phone_code_hash = auth_result["phone_code_hash"]
    account.status = AccountStatus.NEEDS_AUTH
    await session.commit()

    return StandardResponse[dict](
        success=True,
        data={
            "message": "Code sent successfully",
            "account_id": account_id,
            "phone": auth_data.phone,
            "code_type": auth_result["type"],
            "timeout": auth_result["timeout"],
        },
    )


@router.post("/{account_id}/verify", response_model=StandardResponse[dict])
async def verify_auth_code(
    account_id: str,
    verify_data: UserbotAccountVerifyRequest,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Verify authentication code."""
    import os
    from cryptography.fernet import Fernet
    from app.services.telegram_auth import TelegramAuthService
    
    # Get account
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.id == account_id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    if not account.auth_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number not set. Call send-code first.",
        )

    # Get API credentials from env
    api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
    api_hash = os.getenv("TELEGRAM_API_HASH", "")
    encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")

    if not api_id or not api_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram API credentials not configured",
        )

    # Verify code
    auth_service = TelegramAuthService(
        api_id=api_id,
        api_hash=api_hash,
        phone=account.auth_phone,
    )
    auth_service.phone_code_hash = account.phone_code_hash

    auth_result = await auth_service.verify_code(verify_data.code)

    if auth_result["needs_2fa"]:
        account.status = AccountStatus.NEEDS_2FA
        await session.commit()
        
        return StandardResponse[dict](
            success=True,
            data={
                "message": "2FA password required",
                "account_id": account_id,
                "needs_2fa": True,
            },
        )

    if not auth_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=auth_result["error"],
        )

    # Save session and user info
    fernet = Fernet(encryption_key.encode())
    encrypted_session = fernet.encrypt(auth_result["session_string"].encode())

    account.telegram_id = auth_result["user_info"]["id"]
    account.username = auth_result["user_info"]["username"]
    account.first_name = auth_result["user_info"]["first_name"]
    account.last_name = auth_result["user_info"]["last_name"]
    account.phone_number = auth_result["user_info"]["phone"]
    account.session_string = encrypted_session.decode()
    account.status = AccountStatus.ACTIVE
    await session.commit()

    return StandardResponse[dict](
        success=True,
        data={
            "message": "Authentication successful",
            "account_id": account_id,
            "user_info": auth_result["user_info"],
        },
    )


@router.post("/{account_id}/2fa", response_model=StandardResponse[dict])
async def submit_2fa_password(
    account_id: str,
    password_data: UserbotAccount2FARequest,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Submit 2FA password if account has cloud password enabled."""
    import os
    from cryptography.fernet import Fernet
    from app.services.telegram_auth import TelegramAuthService
    
    # Get account
    result = await session.execute(
        select(UserbotAccount).where(UserbotAccount.id == account_id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    if account.status != AccountStatus.NEEDS_2FA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account does not require 2FA verification",
        )

    # Get API credentials from env
    api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
    api_hash = os.getenv("TELEGRAM_API_HASH", "")
    encryption_key = os.getenv("USERBOT_ENCRYPTION_KEY", "test-key-32-bytes-long!!!!")

    if not api_id or not api_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram API credentials not configured",
        )

    # Verify 2FA
    auth_service = TelegramAuthService(
        api_id=api_id,
        api_hash=api_hash,
        phone=account.auth_phone,
    )
    auth_service.phone_code_hash = account.phone_code_hash

    auth_result = await auth_service.verify_2fa(password_data.password)

    if not auth_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=auth_result["error"],
        )

    # Save session and user info
    fernet = Fernet(encryption_key.encode())
    encrypted_session = fernet.encrypt(auth_result["session_string"].encode())

    account.telegram_id = auth_result["user_info"]["id"]
    account.username = auth_result["user_info"]["username"]
    account.first_name = auth_result["user_info"]["first_name"]
    account.last_name = auth_result["user_info"]["last_name"]
    account.phone_number = auth_result["user_info"]["phone"]
    account.session_string = encrypted_session.decode()
    account.status = AccountStatus.ACTIVE
    await session.commit()

    return StandardResponse[dict](
        success=True,
        data={
            "message": "2FA verification successful",
            "account_id": account_id,
            "user_info": auth_result["user_info"],
        },
    )


@router.post("/{account_id}/logout", response_model=StandardResponse[dict])
async def logout_account(
    account_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StandardResponse[dict]:
    """Logout and clear session for account."""
    # TODO: Implement logout
    return StandardResponse[dict](
        success=True,
        data={
            "message": "Logged out (not implemented)",
            "account_id": account_id,
        },
    )
