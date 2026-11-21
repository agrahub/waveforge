import pytest

from wavekit.models import DWTConfiguration, ScaleConfiguration


class TestScaleConfiguration:
    def test_valid_configuration(self):
        scale = ScaleConfiguration(
            min_index=-1, max_index=0, terms=2, numerators=[-1, 1], denominator=0.5
        )

        assert scale.min_index == -1
        assert scale.max_index == 0
        assert scale.terms == 2
        assert scale.numerators == [-1, 1]
        assert scale.denominator == 0.5

    def test_invalid_term_count(self):
        with pytest.raises(ValueError):
            ScaleConfiguration(
                min_index=-1,
                max_index=0,
                terms=3,
                numerators=[-1, 1, 2],
                denominator=0.5,
            )

    def test_invalid_numerator_length(self):
        with pytest.raises(ValueError):
            ScaleConfiguration(
                min_index=-1, max_index=0, terms=2, numerators=[-1], denominator=0.5
            )

    def test_invalid_denominator(self):
        with pytest.raises(ValueError):
            ScaleConfiguration(
                min_index=-1, max_index=0, terms=2, numerators=[-1, 1], denominator=0
            )


class TestDWTConfiguration:
    def test_valid_configuration(self):
        config = DWTConfiguration(
            wavelet="Quadratic Spline",
            version="1.0",
            scales={
                1: ScaleConfiguration(
                    min_index=-1,
                    max_index=0,
                    terms=2,
                    numerators=[-1, 1],
                    denominator=0.5,
                )
            },
        )

        assert config.wavelet == "Quadratic Spline"
        assert config.version == "1.0"
        assert 1 in config.scales

    def test_json_serialization(self):
        config = DWTConfiguration(
            wavelet="Quadratic Spline",
            version="1.0",
            scales={
                1: ScaleConfiguration(
                    min_index=-1,
                    max_index=0,
                    terms=2,
                    numerators=[-1, 1],
                    denominator=0.5,
                )
            },
        )

        json_data = config.model_dump_json()
        restored = DWTConfiguration.model_validate_json(json_data)

        assert restored == config
