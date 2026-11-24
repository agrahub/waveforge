from pydantic import BaseModel, ConfigDict, Field, model_validator


class ScaleConfiguration(BaseModel):
    """Configuration of DWT filter coefficients at a specific scale."""

    model_config = ConfigDict(extra="forbid")

    min_index: int
    max_index: int
    terms: int = Field(gt=0)
    numerators: list[int]
    denominator: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_configuration(self):
        expected_terms = self.max_index - self.min_index + 1

        if self.terms != expected_terms:
            raise ValueError("Terms must equal max_index - min_index + 1.")

        if len(self.numerators) != self.terms:
            raise ValueError("The number of numerators must equal terms.")

        return self

    @property
    def coefficients(self) -> list[float]:
        """Compute the normalized coefficients from numerators and denominator."""
        return [num / self.denominator for num in self.numerators]


class DWTConfiguration(BaseModel):
    """Configuration containing DWT coefficients across multiple scales."""

    model_config = ConfigDict(extra="forbid")

    wavelet: str
    scales: dict[int, ScaleConfiguration]
