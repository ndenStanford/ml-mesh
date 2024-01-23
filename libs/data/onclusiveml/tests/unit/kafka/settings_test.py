"""Settings test."""

# 3rd party libraries
import pytest
from pydantic import SecretStr

# Internal libraries
from onclusiveml.data.kafka import (
    KafkaBaseSettings,
    KafkaConsumerSettings,
    KafkaProducerSettings,
)


@pytest.mark.parametrize("bootstrap_servers", ["localhost:9092,localhost:9093"])
def test_base_settings_without_auth(bootstrap_servers):
    """Test base settings without authentication."""
    settings = KafkaBaseSettings(
        bootstrap_servers=bootstrap_servers,
    )

    assert settings.config == {"bootstrap.servers": bootstrap_servers}


@pytest.mark.parametrize(
    "bootstrap_servers, security_protocol, sasl_mechanism, sasl_username, sasl_password",
    [("localhost:9092,localhost:9093", "", "", "onclusiveml", "password")],
)
def test_base_settings(
    bootstrap_servers, security_protocol, sasl_mechanism, sasl_username, sasl_password
):
    """Test base settings."""
    settings = KafkaBaseSettings(
        bootstrap_servers=bootstrap_servers,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_username=sasl_username,
        sasl_password=sasl_password,
    )

    assert settings.config == {
        "bootstrap.servers": bootstrap_servers,
        "security.protocol": security_protocol,
        "sasl.mechanism": sasl_mechanism,
        "sasl.username": sasl_username,
        "sasl.password": SecretStr(sasl_password),
    }


@pytest.mark.parametrize(
    "bootstrap_servers, security_protocol, sasl_mechanism, sasl_username, sasl_password, compression_type",  # noqa: E501
    [("localhost:9092,localhost:9093", "", "", "onclusiveml", "password", "gzip")],
)
def test_producer_settings(
    bootstrap_servers,
    security_protocol,
    sasl_mechanism,
    sasl_username,
    sasl_password,
    compression_type,
):
    """Test producer settings."""
    settings = KafkaProducerSettings(
        bootstrap_servers=bootstrap_servers,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_username=sasl_username,
        sasl_password=sasl_password,
        compression_type=compression_type,
    )

    assert settings.config == {
        "bootstrap.servers": bootstrap_servers,
        "security.protocol": security_protocol,
        "sasl.mechanism": sasl_mechanism,
        "sasl.username": sasl_username,
        "sasl.password": SecretStr(sasl_password),
        "compression.type": compression_type,
    }


@pytest.mark.parametrize(
    "bootstrap_servers, security_protocol, sasl_mechanism, sasl_username, sasl_password, group_id, auto_offset_reset",  # noqa: E501
    [
        (
            "localhost:9092,localhost:9093",
            "",
            "",
            "onclusiveml",
            "password",
            "groupid",
            "earliest",
        )
    ],
)
def test_consumer_settings(
    bootstrap_servers,
    security_protocol,
    sasl_mechanism,
    sasl_username,
    sasl_password,
    group_id,
    auto_offset_reset,
):
    """Test consumer settings."""
    settings = KafkaConsumerSettings(
        bootstrap_servers=bootstrap_servers,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_username=sasl_username,
        sasl_password=sasl_password,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
    )

    assert settings.config == {
        "bootstrap.servers": bootstrap_servers,
        "security.protocol": security_protocol,
        "sasl.mechanism": sasl_mechanism,
        "sasl.username": sasl_username,
        "sasl.password": SecretStr(sasl_password),
        "group.id": group_id,
        "auto.offset.reset": auto_offset_reset,
    }
