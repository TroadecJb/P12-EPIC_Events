class Permission:
    user_permissions = {
        1: "admin",
        2: "sale",
        3: "manager",
        4: "support",
    }

    @staticmethod
    def check(user, permission):
        if user.role_id in permission:
            return True
        else:
            return False
