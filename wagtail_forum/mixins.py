from django.core import checks


class RequiredForeignKeyMixin:
    """
    Validates foreign key requirements for non-abstract models.

    Checks that required foreign key fields are present and have correct expected related names.

    Attributes:
        REQUIRED_FOREIGN_KEYS (list): List of (field_name, related_name) tuples
    """

    REQUIRED_FOREIGN_KEYS = []

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        if not cls._meta.abstract:
            model_field_names = [f.name for f in cls._meta.get_fields()]
            for field, expected_related_name in cls.REQUIRED_FOREIGN_KEYS:
                if field not in model_field_names:
                    errors.append(
                        checks.Error(
                            f"{cls.__name__} must define a '{field}' field",
                            id="wagtail_forum.E001",
                        )
                    )
                else:
                    field_obj = cls._meta.get_field(field)

                    if (
                        field_obj.remote_field
                        and field_obj.remote_field.related_name != expected_related_name
                    ):
                        errors.append(
                            checks.Error(
                                f"{cls.__name__}'s '{field}' field must have related_name='{expected_related_name}'",
                                id="wagtail_forum.E002",
                            )
                        )
        return errors
