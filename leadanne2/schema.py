from langchain_core.pydantic_v1 import BaseModel, Field


class ActionPoint(BaseModel):
    title: str = Field(description="A short and concise title.")
    description: str = Field(
        description=(
            "A well-explained description of the solution proposed"
            " with the justification of why it will help with the issue."
        )
    )


class EmailTemplate(BaseModel):
    introduction: str = Field(
        description=("A short introduction, saying what it is about.")
    )
    action_points: list[ActionPoint] = Field(
        description="The proposed solutions of for the problem."
    )
