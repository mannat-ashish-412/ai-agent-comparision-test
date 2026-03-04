from pydantic import BaseModel, Field


class CloudProvisioningOutput(BaseModel):
    """The result of the database provisioning task."""

    table_created: bool = Field(
        ..., description="True if the user table was successfully created."
    )
    db_status_final: str = Field(
        ..., description="The final status of the database (e.g., 'AVAILABLE')."
    )
    message: str = Field(
        default="", description="A summary message of the operations performed."
    )
