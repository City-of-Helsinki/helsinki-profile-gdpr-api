from django.db import models
from django.db.models.fields.reverse_related import OneToOneRel


class SerializableMixin(models.Model):
    """
    Mixin to add custom serialization for django models in order to get the desired tree of models to
    the downloadable JSON form. It detects relationships automatically (many to many not yet fully
    supported). Check for the example for more details about the structure.

    Attributes need to be defined in the extending model:

    - serialize_fields (required)
        - tuple of dicts:
            - name (required), name of the field or relation that's going to be added to the serialized object
            - accessor (optional), function that is called when value of the field is resolved and it takes the
              actual field value as argument

    Example usage and output:

    class Post(SerializableMixin):
        serialize_fields = (
            { "name": "title" },
            { "name": "content" },
            {
                "name": "created_at",
                "accessor": lambda x: x.strftime("%Y-%m-%d")
            }
            { "name": "comments" },
        )

    class Comment(SerializableMixin):
        serialize_fields = (
            { "name": "text" },
            { "name": "author" },
        )

    Calling serialize() on a single post object generates:

    {
        "key": "POST",
        "children": [
            { "key": "TITLE", "value": "Post about serialization" },
            { "key": "CONTENT", "value": "This is the content of the post" },
            { "key": "CREATED_AT", "value": "2020-02-03" },
            { "key": "COMMENTS", "children": [
                {
                    "key": "COMMENT"
                    "children": [
                        { "key": "TEXT", "value": "I really like this post" },
                        { "key": "AUTHOR", "value": "Mike" }
                    ]
                },
                {
                    "key": "COMMENT"
                    "children": [
                        { "key": "TEXT", "value": "I don't agree with this 100%" },
                        { "key": "AUTHOR", "value": "Maria" }
                    ]
                }
            ]}
        ]
    }
    """

    class SerializableManager(models.Manager):
        def serialize(self):
            return [
                obj.serialize() if hasattr(obj, "serialize") else []
                for obj in self.get_queryset().all()
            ]

    class Meta:
        abstract = True

    objects = SerializableManager()

    def _resolve_field(self, model, field_description):
        field_name = field_description.get("name")

        def _resolve_value():
            value = getattr(model, field_name)

            if "accessor" in field_description:
                # call the accessor with value as an argument
                value = field_description["accessor"](value)

            return value

        related_types = {item.name: type(item) for item in model._meta.related_objects}
        if field_name in related_types.keys():
            value = (
                getattr(model, field_name).serialize()
                if hasattr(model, field_name)
                and hasattr(getattr(model, field_name), "serialize")
                else None
            )
            # field is a related object, let's serialize more
            if related_types[field_name] == OneToOneRel:
                # do not wrap one-to-one relations into list
                return value
            else:
                return {
                    "key": field_name.upper(),
                    "children": value,
                }
        else:
            # concrete field, let's just add the value
            return {
                "key": field_name.upper(),
                "value": _resolve_value(),
            }

    def serialize(self):
        return {
            "key": self._meta.model_name.upper(),
            "children": list(
                filter(
                    lambda x: x is not None,
                    [
                        self._resolve_field(self, field_description)
                        for field_description in self.serialize_fields
                    ],
                )
            ),
        }
