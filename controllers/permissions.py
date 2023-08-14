class Permission:
    user_permissions = {
        1: "admin",
        2: "manager",
        3: "sale",
        4: "support",
    }

    @staticmethod
    def check(user, permission):
        if user.role_id in permission:
            return True
        else:
            return False

    def check_is_assigned_commercial(user, obj):
        """Check if obj.commercial_id is the same as the user.id"""
        pass

    def check_is_assigned_support(user, event):
        """Check if event.support_id is the same as the user.id"""
        pass
