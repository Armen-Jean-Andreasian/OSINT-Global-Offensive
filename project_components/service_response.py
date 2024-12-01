class ServiceResponse:
    """Special class designed for inter-app communication. Supports if true check."""

    def __init__(self, status: bool, data=None, error=None, reason=None):
        self.status = status
        self.data = data
        self.error = error
        self.reason = reason

    def __repr__(self):
        return f"<ServiceResponse(success={self.status}, data={self.data}, error={self.error})>"

    def to_dict(self, non_null=False):
        result = {
            "success": self.status,
            "data": self.data,
            "error": self.error,
            "reason": self.reason
        }

        if non_null:
            if not self.data:
                result.pop('data')
            if not self.error:
                result.pop('error')
            if not self.reason:
                result.pop('reason')

        return result

    def __bool__(self):
        return self.status

    def __str__(self):
        return f"{self.status}"
