from db.repositories.user import PermissionRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def add_base_permissions(session: AsyncSession):
    admin = await PermissionRepository(session).get_by_name("admin")
    if admin:
        return

    await PermissionRepository(session).create_permission("admin")
