from enum import Enum

from fastapi import Depends, HTTPException, status


class UserRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    CASHIER = "cashier"


class Permission(str, Enum):
    # Dashboard
    VIEW_DASHBOARD = "view_dashboard"
    # Medicine
    VIEW_MEDICINES = "view_medicines"
    CREATE_MEDICINE = "create_medicine"
    UPDATE_MEDICINE = "update_medicine"
    DELETE_MEDICINE = "delete_medicine"
    # Batch
    VIEW_BATCHES = "view_batches"
    CREATE_BATCH = "create_batch"
    UPDATE_BATCH = "update_batch"
    # Inventory
    VIEW_INVENTORY = "view_inventory"
    ADJUST_STOCK = "adjust_stock"
    # Purchase
    VIEW_PURCHASES = "view_purchases"
    CREATE_PURCHASE = "create_purchase"
    # Sales
    VIEW_SALES = "view_sales"
    CREATE_SALE = "create_sale"
    RETURN_SALE = "return_sale"
    # Suppliers
    VIEW_SUPPLIERS = "view_suppliers"
    CREATE_SUPPLIER = "create_supplier"
    UPDATE_SUPPLIER = "update_supplier"
    # Reports
    VIEW_REPORTS = "view_reports"
    VIEW_FINANCIAL_REPORTS = "view_financial_reports"
    # Users
    VIEW_USERS = "view_users"
    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    # Settings
    VIEW_SETTINGS = "view_settings"
    UPDATE_SETTINGS = "update_settings"
    # AI
    USE_AI = "use_ai"


ROLE_PERMISSIONS: dict[UserRole, list[Permission]] = {
    UserRole.OWNER: list(Permission),
    UserRole.MANAGER: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MEDICINES,
        Permission.CREATE_MEDICINE,
        Permission.UPDATE_MEDICINE,
        Permission.VIEW_BATCHES,
        Permission.CREATE_BATCH,
        Permission.UPDATE_BATCH,
        Permission.VIEW_INVENTORY,
        Permission.ADJUST_STOCK,
        Permission.VIEW_PURCHASES,
        Permission.CREATE_PURCHASE,
        Permission.VIEW_SALES,
        Permission.CREATE_SALE,
        Permission.RETURN_SALE,
        Permission.VIEW_SUPPLIERS,
        Permission.CREATE_SUPPLIER,
        Permission.UPDATE_SUPPLIER,
        Permission.VIEW_REPORTS,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.USE_AI,
    ],
    UserRole.CASHIER: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MEDICINES,
        Permission.VIEW_BATCHES,
        Permission.VIEW_INVENTORY,
        Permission.VIEW_SALES,
        Permission.CREATE_SALE,
        Permission.RETURN_SALE,
        Permission.VIEW_SUPPLIERS,
    ],
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, [])


def require_permissions(*permissions: Permission):
    from app.dependencies import get_current_user

    async def checker(current_user=Depends(get_current_user)):
        user_role = UserRole(current_user.role)
        for perm in permissions:
            if not has_permission(user_role, perm):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {perm.value}",
                )
        return current_user

    return checker
