# scaffold.py

from pathlib import Path
import logging


# ==================================================
# PROJECT CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent

SRC_DIR = PROJECT_ROOT / "src"
PACKAGE_DIR = SRC_DIR / "github_recommender"


# ==================================================
# PACKAGE STRUCTURE
# ==================================================

PACKAGE_STRUCTURE = {
    "config": [
        "settings.py",
    ],

    "data": [
        "database.py",
        "extraction.py",
        "preprocessing.py",
    ],

    "features": [
        "user_features.py",
        "repository_features.py",
        "interaction_features.py",
    ],

    "models": [
        "popularity.py",
        "content_based.py",
        "collaborative.py",
        "hybrid.py",
    ],

    "recommendation": [
        "ranking.py",
        "service.py",
    ],

    "evaluation": [
        "metrics.py",
        "evaluate.py",
    ],

    "api": [
        "main.py",
        "schemas.py",
    ],
}


# ==================================================
# ROOT-LEVEL DIRECTORIES AND FILES
# ==================================================

PROJECT_DIRECTORIES = [
    "notebooks",
    "tests/unit",
    "tests/integration",
    "scripts",
    "artifacts",
    ".github/workflows",
]


ROOT_FILES = [
    ".env.example",
    ".gitignore",
    ".dockerignore",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "README.md",
    "LICENSE",
]


NOTEBOOK_FILES = [
    "01_eda.ipynb",
    "02_feature_engineering.ipynb",
    "03_model_experiments.ipynb",
]


TEST_FILES = [
    "conftest.py",
    "unit/test_features.py",
    "unit/test_models.py",
    "unit/test_recommendations.py",
    "integration/test_database.py",
    "integration/test_api.py",
]


SCRIPT_FILES = [
    "check_database.py",
    "train_model.py",
]


GITHUB_WORKFLOW_FILES = [
    ".github/workflows/ci.yml",
]


# ==================================================
# LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


# ==================================================
# FILE CREATION HELPER
# ==================================================

def create_file(file_path: Path, content: str = "") -> None:
    """Create a file without overwriting existing content."""

    if file_path.exists():
        logger.info("Already exists: %s", file_path)
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    logger.info("Created: %s", file_path)


# ==================================================
# PROJECT STRUCTURE CREATION
# ==================================================

def create_project_structure() -> None:
    """Generate the GitHub recommendation system structure."""

    # Safety check
    if PROJECT_ROOT.name == ".venv":
        raise RuntimeError(
            "Project root cannot be inside a virtual environment."
        )

    if PROJECT_ROOT == PROJECT_ROOT.parent:
        raise RuntimeError("Invalid project root.")

    try:

        # ------------------------------------------
        # 1. Create source package
        # ------------------------------------------

        PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

        create_file(
            PACKAGE_DIR / "__init__.py",
            '"""GitHub Repository Recommendation System."""\n\n'
            '__version__ = "0.1.0"\n',
        )

        # ------------------------------------------
        # 2. Create package modules
        # ------------------------------------------

        for directory, files in PACKAGE_STRUCTURE.items():

            package_subdir = PACKAGE_DIR / directory

            package_subdir.mkdir(
                parents=True,
                exist_ok=True,
            )

            create_file(package_subdir / "__init__.py")

            for filename in files:
                create_file(package_subdir / filename)

        # ------------------------------------------
        # 3. Create project directories
        # ------------------------------------------

        for directory in PROJECT_DIRECTORIES:

            directory_path = PROJECT_ROOT / directory

            directory_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.info("Directory ready: %s", directory_path)

        # ------------------------------------------
        # 4. Create root-level files
        # ------------------------------------------

        for filename in ROOT_FILES:

            create_file(PROJECT_ROOT / filename)

        # ------------------------------------------
        # 5. Create notebooks
        # ------------------------------------------

        for filename in NOTEBOOK_FILES:

            create_file(
                PROJECT_ROOT / "notebooks" / filename,
                (
                    '{\n'
                    ' "cells": [],\n'
                    ' "metadata": {},\n'
                    ' "nbformat": 4,\n'
                    ' "nbformat_minor": 5\n'
                    '}\n'
                ),
            )

        # ------------------------------------------
        # 6. Create test files
        # ------------------------------------------

        for filename in TEST_FILES:

            create_file(
                PROJECT_ROOT / "tests" / filename
            )

        # ------------------------------------------
        # 7. Create test package initializer
        # ------------------------------------------

        create_file(
            PROJECT_ROOT / "tests" / "__init__.py"
        )

        # ------------------------------------------
        # 8. Create scripts
        # ------------------------------------------

        for filename in SCRIPT_FILES:

            create_file(
                PROJECT_ROOT / "scripts" / filename
            )

        # ------------------------------------------
        # 9. Create GitHub workflow
        # ------------------------------------------

        for filename in GITHUB_WORKFLOW_FILES:

            create_file(
                PROJECT_ROOT / filename
            )

        # ------------------------------------------
        # 10. Create artifacts placeholder
        # ------------------------------------------

        create_file(
            PROJECT_ROOT / "artifacts" / ".gitkeep"
        )

        # ------------------------------------------
        # 11. Completion message
        # ------------------------------------------

        logger.info("=" * 55)
        logger.info("PROJECT STRUCTURE CREATED SUCCESSFULLY")
        logger.info("Project root: %s", PROJECT_ROOT)
        logger.info("Source package: %s", PACKAGE_DIR)
        logger.info("=" * 55)

    except OSError:
        logger.exception("Failed to create project structure.")
        raise


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":
    create_project_structure()
