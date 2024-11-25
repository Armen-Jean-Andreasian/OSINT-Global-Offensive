class ServiceResponse:
    """Special class designed for inter-app communication. Supports if true check."""
    def __init__(self, status: bool, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

    def __repr__(self):
        return f"<ServiceResponse(success={self.status}, data={self.data}, error={self.error})>"

    def to_dict(self):
        return {
            "success": self.status,
            "data": self.data,
            "error": self.error,
        }

    def __bool__(self):
        return self.status
