import json

import pytest

from waveforge.wavelets.quadratic_spline import generator


class TestGenerateScaleConfiguration:
    @pytest.mark.parametrize(
        "scale, expected_min, expected_max, expected_terms, expected_denominator",
        [
            (1, -1, 0, 2, 0.5),
            (2, -4, 1, 6, 4.0),
            (3, -10, 3, 14, 32.0),
            (4, -22, 7, 30, 256.0),
            (5, -46, 15, 62, 2048.0),
        ],
    )
    def test_scale_metadata(
        self, scale, expected_min, expected_max, expected_terms, expected_denominator
    ):
        config = generator.generate_scale_configuration(scale)

        assert config.min_index == expected_min
        assert config.max_index == expected_max
        assert config.terms == expected_terms
        assert config.denominator == expected_denominator

    @pytest.mark.parametrize("scale", [1, 2, 3, 4, 5])
    def test_numerator_count(self, scale):
        config = generator.generate_scale_configuration(scale)

        assert len(config.numerators) == config.terms

    @pytest.mark.parametrize("scale", [1, 2, 3, 4, 5])
    def test_numerator_symmetry(self, scale):
        config = generator.generate_scale_configuration(scale)

        half = config.terms // 2

        assert config.numerators[half:] == [
            -value for value in reversed(config.numerators[:half])
        ]

    @pytest.mark.parametrize("scale", [0, -1, -5, 1.5, True, "3"])
    def test_invalid_scale(self, scale):
        with pytest.raises(ValueError):
            generator.generate_scale_configuration(scale)


class TestGenerateCoefficients:
    def test_generate_multiple_scales(self):
        config = generator.generate_configuration(5)

        assert config.wavelet == "Quadratic Spline"
        assert config.version == "1.0"
        assert list(config.scales.keys()) == [1, 2, 3, 4, 5]

    def test_invalid_max_scale(self):
        for invalid_scale in [0, -1, 1.5, True, "5"]:
            with pytest.raises(ValueError):
                generator.generate_configuration(invalid_scale)


class TestSaveCoefficients:
    def test_save_json(self, tmp_path):
        config = generator.generate_configuration(3)

        output_path = generator.save_configuration(config, dir=tmp_path)

        assert output_path.exists()
        assert output_path.name == ("quadratic_spline_v1.0_scales_1-3.json")
        assert output_path.parent == tmp_path

        with output_path.open("r", encoding="utf-8") as file:
            saved_data = json.load(file)

        assert saved_data["wavelet"] == "Quadratic Spline"
        assert saved_data["version"] == "1.0"
        assert len(saved_data["scales"]) == 3

    def test_save_empty_configuration(self):
        config = generator.DWTConfiguration(
            wavelet="Quadratic Spline", version="1.0", scales={}
        )

        with pytest.raises(ValueError):
            generator.save_configuration(config)
