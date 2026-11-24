from pathlib import Path

from waveforge.models import DWTConfiguration


def load_configuration(filename: str, dir: str | Path | None = None) -> DWTConfiguration:
    """
    Load Quadratic Spline DWT configuration from a JSON file.

    Parameters
    ----------
    filename : str
        Name of the JSON file.
    dir : str or Path, optional
        Directory containing the JSON file.
        Defaults to the current working directory.

    Returns
    -------
    DWTConfiguration
        Validated DWT coefficient configuration.
    """

    input_dir = Path(dir) if dir is not None else Path.cwd()
    file_path = input_dir / filename

    if not file_path.is_file():
        raise FileNotFoundError(f"Coefficient configuration not found: {file_path}")

    json_data = file_path.read_text(encoding="utf-8")

    config = DWTConfiguration.model_validate_json(json_data)

    if config.wavelet != "Quadratic Spline":
        raise ValueError(
            f"Expected Quadratic Spline configuration, got '{config.wavelet}'."
        )

    return config
