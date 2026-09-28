import os

PROFILE = os.getenv("DATASET_PROFILE", "DEV").upper()

PROFILES = {
    "DEV": {
        "EXPERTS": 5,
        "PEOPLE": 20,
        "PROJECTS": 10,
        "TECHNOLOGIES": 25,
        "MEMORIES": 500,
        "DECISIONS": 100,
        "INCIDENTS": 50,
        "MEETINGS": 60,
        "BATCH_SIZE": 100,
    },
    "DEMO": {
        "EXPERTS": 15,
        "PEOPLE": 100,
        "PROJECTS": 30,
        "TECHNOLOGIES": 50,
        "MEMORIES": 5000,
        "DECISIONS": 1000,
        "INCIDENTS": 300,
        "MEETINGS": 500,
        "BATCH_SIZE": 500,
    },
    "FULL": {
        "EXPERTS": 50,
        "PEOPLE": 500,
        "PROJECTS": 100,
        "TECHNOLOGIES": 200,
        "MEMORIES": 100000,
        "DECISIONS": 10000,
        "INCIDENTS": 5000,
        "MEETINGS": 20000,
        "BATCH_SIZE": 2000,
    },
    "STRESS": {
        "EXPERTS": 100,
        "PEOPLE": 2000,
        "PROJECTS": 250,
        "TECHNOLOGIES": 300,
        "MEMORIES": 500000,
        "DECISIONS": 50000,
        "INCIDENTS": 25000,
        "MEETINGS": 50000,
        "BATCH_SIZE": 5000,
    }
}

CURRENT_CONFIG = PROFILES.get(PROFILE, PROFILES["DEV"])
