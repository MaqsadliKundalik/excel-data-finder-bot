from aiogram import Router
from message.admin import router as admin_router
from message.users import router as users_router

router = Router()
router.include_router(admin_router)
router.include_router(users_router)