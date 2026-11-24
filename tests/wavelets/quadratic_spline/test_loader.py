import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from waveforge.models import DWTConfiguration
from waveforge.wavelets.quadratic_spline import generator, loader


class TestLoadConfiguration:
    def test_load_valid_json(self, tmp_path: Path) -> None:
        config = generator.generate_configuration(3)
        output_path = generator.save_configuration(config, dir=tmp_path)

        loaded_config = loader.load_configuration(output_path.name, dir=tmp_path)

        assert isinstance(loaded_config, DWTConfiguration)
        assert loaded_config.wavelet == "Quadratic Spline"
        assert len(loaded_config.scales) == 3
        assert loaded_config == config

    def test_load_from_current_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config = generator.generate_configuration(2)
        output_path = generator.save_configuration(config, dir=tmp_path)

        monkeypatch.chdir(tmp_path)

        loaded_config = loader.load_configuration(output_path.name)

        assert loaded_config == config

    def test_load_nonexistent_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            loader.load_configuration("nonexistent.json", dir=tmp_path)

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{invalid json}", encoding="utf-8")

        with pytest.raises(ValidationError):
            loader.load_configuration(file_path.name, dir=tmp_path)

    def test_load_invalid_configuration(self, tmp_path: Path) -> None:
        invalid_data = {
            "wavelet": "Quadratic Spline",
            "scales": {
                "1": {
                    "min_index": -1,
                    "max_index": 0,
                    "terms": 3,
                    "numerators": [1, -1, 2],
                    "denominator": 0.5,
                }
            },
        }

        file_path = tmp_path / "invalid_config.json"
        file_path.write_text(json.dumps(invalid_data), encoding="utf-8")

        with pytest.raises(ValidationError):
            loader.load_configuration(file_path.name, dir=tmp_path)

    def test_load_different_wavelet(self, tmp_path: Path) -> None:
        config = DWTConfiguration(wavelet="Daubechies", scales={})

        file_path = tmp_path / "other_wavelet.json"
        file_path.write_text(config.model_dump_json(indent=4), encoding="utf-8")

        with pytest.raises(ValueError, match="Expected Quadratic Spline"):
            loader.load_configuration(file_path.name, dir=tmp_path)
