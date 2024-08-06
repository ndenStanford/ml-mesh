"""Path test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import OnclusivePath


@pytest.mark.parametrize(
    "path, expected",
    [
        ("s3://bucket/foo/bar", (["bucket", "foo", "bar"], "s3")),
        (
            "neptune://onclusive/ner/NER-TRAINED-176",
            (["onclusive", "ner", "NER-TRAINED-176"], "neptune"),
        ),
        ("file:///folder/file.txt", (["/", "folder", "file.txt"], "file")),
        ("file:///", (["/"], "file")),
        ("file://", ([], "file")),
    ],
)
def test_path_module_split(pathmodule, path, expected):
    """Test split method."""
    assert pathmodule.split(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("s3://bucket/foo/bar", ("", "s3://bucket/foo/bar")),
        (
            "file:///ner/serve/models/NER-TRAINED-176",
            ("", "file:///ner/serve/models/NER-TRAINED-176"),
        ),
    ],
)
def test_path_module_splitdrive(pathmodule, path, expected):
    """Test splitdrive method."""
    assert pathmodule.splitdrive(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("s3://bucket/foo/bar", True),
        ("foo/bar", False),
        ("/folder1/folder2", False),
        ("file:///foo/bar", True),
    ],
)
def test_path_module_isabs(pathmodule, path, expected):
    """Test isabs method."""
    assert pathmodule.isabs(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            "s3://bucket/foo/bar",
            "s3://bucket/foo/bar",
        ),
        (
            "neptune://onclusive/ner/NER-TRAINED-176",
            "neptune://onclusive/ner/NER-TRAINED-176",
        ),
        (
            "file:///folder/file.txt",
            "file:///folder/file.txt",
        ),
    ],
)
def test_path_module_normcase(pathmodule, path, expected):
    """Test normcase method."""
    assert pathmodule.normcase(path) == expected


@pytest.mark.parametrize(
    "paths, expected",
    [
        (
            ["s3://bucket", "foo", "bar"],
            "s3://bucket/foo/bar",
        )
    ],
)
def test_path_module_join(pathmodule, paths, expected):
    """Test join method."""
    assert pathmodule.join(*paths) == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///ner/serve/models/NER-TRAINED-176",
            "file",
        ),
        (
            "/home/data/processed/archive.tar.gz",
            "file",
        ),
        (
            "s3://bucket/foo/blob",
            "s3",
        ),
    ],
)
def test_onclusive_path_scheme(str_path, expected):
    """Test OnclusivePath scheme attribute."""
    assert OnclusivePath(str_path).scheme == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///ner/serve/models/SUM-COMPILED-16",
            ["/", "ner", "serve", "models", "SUM-COMPILED-16"],
        ),
        (
            "file:///sentiment/serve/sentiment/SEN-COMPILED/SEN-COMPILED-127/model/model_artifacts/compiled_sent_pipeline/compiled_model/model.pt",  # noqa: E501
            [
                "/",
                "sentiment",
                "serve",
                "sentiment",
                "SEN-COMPILED",
                "SEN-COMPILED-127",
                "model",
                "model_artifacts",
                "compiled_sent_pipeline",
                "compiled_model",
                "model.pt",
            ],
        ),
        (
            "s3://onclusive-model-store-prod/neptune-ai-model-registry/onclusive/topic/",  # noqa: E501
            [
                "onclusive-model-store-prod",
                "neptune-ai-model-registry",
                "onclusive",
                "topic",
            ],
        ),
    ],
)
def test_onclusive_path_parts(str_path, expected):
    """Test OnclusivePath scheme attribute."""
    assert OnclusivePath(str_path).parts == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        ("file:///ner/serve/models/SUM-COMPILED-16", "/"),
        (
            "file:///sentiment/serve/sentiment/SEN-COMPILED/SEN-COMPILED-127/model/model_artifacts/compiled_sent_pipeline/compiled_model/model.pt",  # noqa: E501
            "/",
        ),
    ],
)
def test_onclusive_path_root(str_path, expected):
    """Test OnclusivePath root attribute."""
    assert OnclusivePath(str_path).root == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///sentiment/serve/sentiment/SEN-COMPILED/SEN-COMPILED-127/model/model_artifacts/compiled_sent_pipeline/compiled_model/model.pt",  # noqa: E501
            "file:///",
        )
    ],
)
def test_onclusive_path_anchor(str_path, expected):
    """Test OnclusivePath anchor attribute."""
    assert OnclusivePath(str_path).anchor == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///sentiment/serve/sentiment/SEN-COMPILED/SEN-COMPILED-127/model/model_artifacts/compiled_sent_pipeline/compiled_model/model.pt",  # noqa: E501
            "model.pt",
        ),
        (
            "s3://onclusive-model-store-stage/neptune-ai-model-registry/onclusive/ner/",
            "ner",
        ),
    ],
)
def test_onclusive_path_name(str_path, expected):
    """Test OnclusivePath name attribute."""
    assert OnclusivePath(str_path).name == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///sentiment/serve/sentiment/SEN-COMPILED/SEN-COMPILED-127/model/model_artifacts/compiled_sent_pipeline/compiled_model/model.pt",  # noqa: E501
            ".pt",
        ),
        ("s3://kubeflow-feast-config-stage/feature_store.yaml", ".yaml"),
        ("s3://kubeflow-compiled-pipelines-prod/iptc/", ""),
    ],
)
def test_onclusive_path_suffix(str_path, expected):
    """Test OnclusivePath suffix attribute."""
    assert OnclusivePath(str_path).suffix == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "s3://kubeflow-data-lake-prod/iptc/first_level_multi_lingual/doc_classification_dataset_crawler-4-2022-03-000.parquet",  # noqa: E501
            [".parquet"],
        ),
        ("s3://kubeflow-opoint-data-prod/processed/archive.tar.gz", [".tar", ".gz"]),
    ],
)
def test_onclusive_path_suffixes(str_path, expected):
    """Test OnclusivePath suffixes attribute."""
    assert OnclusivePath(str_path).suffixes == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        ("s3://kubeflow-feast-config-prod/feature_store.yaml", "feature_store"),
        ("s3://kubeflow-opoint-data-prod/processed/archive.tar.gz", "archive.tar"),
    ],
)
def test_onclusive_path_stem_remote(str_path, expected):
    """Test OnclusivePath stem attribute."""
    assert OnclusivePath(str_path).stem == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "s3://kubeflow-feast-config-prod/feature_store.yaml",
            OnclusivePath("s3://kubeflow-feast-config-prod"),
        ),
        (
            "s3://kubeflow-opoint-data-prod/processed/archive.tar.gz",
            OnclusivePath("s3://kubeflow-opoint-data-prod/processed"),
        ),
        (
            "file:///user",
            OnclusivePath("file:///"),
        ),
    ],
)
def test_onclusive_path_parent(str_path, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).parent == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///user",
            (OnclusivePath("file:///"),),
        )
    ],
)
def test_onclusive_path_parents(str_path, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).parents == expected


@pytest.mark.parametrize(
    "str_path, segments, expected",
    [
        (
            "file:///user/local/bin",
            ["/", "home", "lib", "python3.8"],
            OnclusivePath("file:///home/lib/python3.8"),
        )
    ],
)
def test_onclusive_path_with_segments(str_path, segments, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).with_segments(*segments) == expected


@pytest.mark.parametrize(
    "str_path, expected",
    [
        (
            "file:///home/data/processed/archive.tar.gz",
            "archive.tar",
        ),
        (
            "file:///user/file.zip",
            "file",
        ),
        (
            "file:///home",
            "home",
        ),
    ],
)
def test_onclusive_path_stem(str_path, expected):
    """Test OnclusivePath stem attribute."""
    assert OnclusivePath(str_path).stem == expected


@pytest.mark.parametrize(
    "str_path, name, expected",
    [
        (
            "file:///user/local/bin/python3.9",
            "python3.8",
            OnclusivePath("file:///user/local/bin/python3.8"),
        ),
        (
            "file:///home/ec2-user/ml-mesh/projects/ner/serve/models/NER-TRAINED/NER-TRAINED-182/model/model_artifacts/base_ner/pytorch_model.bin",  # noqa: E501
            "tokenizer.json",
            OnclusivePath(
                "file:///home/ec2-user/ml-mesh/projects/ner/serve/models/NER-TRAINED/NER-TRAINED-182/model/model_artifacts/base_ner/tokenizer.json"  # noqa: W505,E501
            ),
        ),
    ],
)
def test_onclusive_path_with_name(str_path, name, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).with_name(name) == expected


@pytest.mark.parametrize(
    "str_path, stem, expected",
    [
        (
            "file:///home/file.txt",
            "newfile",
            OnclusivePath("file:///home/newfile.txt"),
        ),
        (
            "file:///home/ec2-user/ml-mesh/projects/ner/serve/models/NER-TRAINED/NER-TRAINED-182/model/model_artifacts/base_ner/pytorch_model.bin",  # noqa: E501
            "tokenizer",
            OnclusivePath(
                "file:///home/ec2-user/ml-mesh/projects/ner/serve/models/NER-TRAINED/NER-TRAINED-182/model/model_artifacts/base_ner/tokenizer.bin"  # noqa: W505,E501
            ),
        ),
    ],
)
def test_onclusive_path_with_stem(str_path, stem, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).with_stem(stem) == expected


@pytest.mark.parametrize(
    "str_path, suffix, expected",
    [
        (
            "file:///home/ec2-user/data/feature_store.yaml",
            ".txt",
            OnclusivePath("file:///home/ec2-user/data/feature_store.txt"),
        ),
    ],
)
def test_onclusive_path_with_suffix(str_path, suffix, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path).with_suffix(suffix) == expected


@pytest.mark.parametrize(
    "str_path, extra, expected",
    [
        (
            "file:///home/ec2-user/data/",
            "feature_store.yaml",
            OnclusivePath("file:///home/ec2-user/data/feature_store.yaml"),
        ),
    ],
)
def test_onclusive_path_overloaded_operator(str_path, extra, expected):
    """Test OnclusivePath parent attribute."""
    assert OnclusivePath(str_path) / extra == expected


@pytest.mark.parametrize(
    "str_path, other, expected",
    [
        ("file:///home/ec2-user/ml-mesh", "file:///home/ec2-user/", True),
        ("file:///usr/local/lib", "file:///usr/local/bin", False),
    ],
)
def test_onclusive_path_is_relative(str_path, other, expected):
    """Test is_relative method."""
    assert OnclusivePath(str_path).is_relative_to(OnclusivePath(other)) == expected
