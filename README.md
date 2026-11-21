# WaveForge

A Python toolkit for generating, storing, and loading Discrete Wavelet Transform (DWT) coefficient configurations.

## Overview

WaveForge provides a structured approach to managing DWT filter coefficient configurations across different wavelet families.

Currently, WaveForge implements the **Quadratic Spline Wavelet** coefficient generator, supporting the generation of coefficient configurations at multiple scales. Configurations can be saved as JSON files and loaded back into validated Python objects using Pydantic.

## Features

- Generate Quadratic Spline DWT coefficients for individual scales.
- Generate coefficient configurations across multiple scales.
- Automatically generate configuration filenames based on wavelet metadata.
- Save coefficient configurations as JSON files.
- Load and validate coefficient configurations from JSON files.
- Validate configuration structures using Pydantic.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd waveforge
```

Install the package in editable mode:

```bash
pip install -e .
```

## Usage

### 1. Generate Coefficient Configurations

Generate coefficients for a specific scale:

```python
from waveforge.wavelets.quadratic_spline import (
    generate_scale_configuration
)

scale_config = generate_scale_configuration(3)

print(scale_config)
```

Generate configurations from scale 1 up to a specified maximum scale:

```python
from waveforge.wavelets.quadratic_spline import (
    generate_coefficients
)

config = generate_coefficients(5)
```

### 2. Save Coefficient Configurations

Save a configuration as a JSON file:

```python
from waveforge.wavelets.quadratic_spline import (
    generate_coefficients,
    save_coefficients
)

config = generate_coefficients(5)

output_path = save_coefficients(config)

print(output_path)
```

By default, the file is saved in the current working directory.

You can also specify a destination directory:

```python
output_path = save_coefficients(
    config,
    dir="data/coefficients"
)
```

The filename is automatically generated using the wavelet name, configuration version, and scale range.

Example:

```text
quadratic_spline_v1.0_scales_1-5.json
```

### 3. Load Coefficient Configurations

Load a previously saved configuration:

```python
from waveforge.wavelets.quadratic_spline import (
    load_coefficients
)

config = load_coefficients(
    "quadratic_spline_v1.0_scales_1-5.json"
)
```

You can also specify the directory containing the JSON file:

```python
config = load_coefficients(
    "quadratic_spline_v1.0_scales_1-5.json",
    dir="data/coefficients"
)
```

The loader reconstructs and validates the configuration using Pydantic.

## Configuration Models

WaveForge uses two primary data models:

| Model | Description |
|---|---|
| `ScaleConfiguration` | Represents DWT filter coefficients and their associated parameters at a specific scale. |
| `DWTConfiguration` | Represents a complete DWT configuration containing coefficient data across multiple scales. |

Both models are available directly from the main package:

```python
from waveforge import DWTConfiguration, ScaleConfiguration
```

## Project Structure

```text
waveforge/
├── pyproject.toml
├── README.md
├── src/
│   └── waveforge/
│       ├── __init__.py
│       ├── models.py
│       ├── wavelets/
│       │   ├── __init__.py
│       │   └── quadratic_spline/
│       │       ├── __init__.py
│       │       ├── generator.py
│       │       └── loader.py
│       └── data/
└── tests/
    ├── test_models.py
    └── wavelets/
        └── quadratic_spline/
            ├── test_generator.py
            └── test_loader.py
```

## Testing

WaveForge uses `pytest` for automated testing.

Install pytest:

```bash
pip install pytest
```

Run the test suite from the project root:

```bash
pytest -v
```

## Dependencies

- Python 3.10 or later
- Pydantic 2.x
- pytest (development and testing)

## License

No license has been specified yet.

