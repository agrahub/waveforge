import re
from pathlib import Path

from waveforge.models import DWTConfiguration, ScaleConfiguration


def generate_scale_configuration(scale: int) -> ScaleConfiguration:
    """
    Generate Quadratic Spline DWT coefficients for a given scale.
    """

    if type(scale) is not int or scale < 1:
        raise ValueError("Scale must be a positive integer.")

    # Calculate scale-dependent parameters
    min_index = -(2**scale + 2 ** (scale - 1) - 2)
    max_index = 2 ** (scale - 1) - 1
    terms = 2 ** (scale + 1) - 2
    denominator = float(2 ** (3 * scale - 4))

    half_terms = terms // 2

    # Generate the first half of the numerator sequence
    first_half: list[int] = []

    for k in range(1, half_terms + 1):
        if k <= 2 ** (scale - 1):
            # Triangular number sequence
            numerator = k * (k + 1) // 2

        else:
            # Remaining first-half coefficients
            r = half_terms - k + 1

            numerator = (-3 * r**2 + 3 * r + 2**scale * (2 * r - 1)) // 2

        first_half.append(numerator)

    # Second half: negative reverse of the first half
    second_half = [-value for value in reversed(first_half)]

    numerators = first_half + second_half

    return ScaleConfiguration(
        min_index=min_index,
        max_index=max_index,
        terms=terms,
        numerators=numerators,
        denominator=denominator,
    )


def generate_coefficients(max_scale: int) -> DWTConfiguration:
    """
    Generate Quadratic Spline DWT configurations from scale 1
    up to the specified maximum scale.
    """

    if type(max_scale) is not int or max_scale < 1:
        raise ValueError("Maximum scale must be a positive integer.")

    scales = {
        scale: generate_scale_configuration(scale) for scale in range(1, max_scale + 1)
    }

    return DWTConfiguration(wavelet="Quadratic Spline", version="1.0", scales=scales)


def save_coefficients(config: DWTConfiguration, dir: str | Path | None = None) -> Path:
    """Save coefficients using configuration metadata."""

    wavelet_name = re.sub(r"[^a-zA-Z0-9]+", "_", config.wavelet).strip("_").lower()

    scale_numbers = sorted(config.scales)

    if not scale_numbers:
        raise ValueError("Cannot save an empty configuration.")

    filename = (
        f"{wavelet_name}_v{config.version}_"
        f"scales_{scale_numbers[0]}-{scale_numbers[-1]}.json"
    )

    output_dir = Path(dir) if dir is not None else Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    output_path.write_text(config.model_dump_json(indent=4), encoding="utf-8")

    return output_path
