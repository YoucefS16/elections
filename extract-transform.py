import os
import pandas as pd

DEPARTEMENT = "31"

DATA_DIR = "data"
CLEAN_DIR = "clean"

CANDIDATS_FILE = os.path.join(DATA_DIR, "candidats-2026.csv")
COMMUNES_FILE = os.path.join(DATA_DIR, "communes.csv")
INSEE_FILE = os.path.join(DATA_DIR, "insee_communes.csv")
DEPARTEMENTS_FILE = os.path.join(DATA_DIR, "departements-france.csv")
REGIONS_FILE = os.path.join(DATA_DIR, "regions-france.csv")


def normalize_code(value, length):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.endswith(".0"):
        value = value[:-2]

    return value.zfill(length)


def save_csv(df, path, sep, encoding="utf-8"):
    df.to_csv(path, index=False, sep=sep, encoding=encoding)


def main():
    os.makedirs(CLEAN_DIR, exist_ok=True)

    # Lecture
    candidats = pd.read_csv(CANDIDATS_FILE, sep=";", dtype=str, encoding="utf-8")
    communes = pd.read_csv(COMMUNES_FILE, sep=",", dtype=str, encoding="utf-8")
    insee = pd.read_csv(INSEE_FILE, sep=";", dtype=str, encoding="latin1")
    departements = pd.read_csv(DEPARTEMENTS_FILE, sep=",", dtype=str, encoding="utf-8")
    regions = pd.read_csv(REGIONS_FILE, sep=",", dtype=str, encoding="utf-8")

    # Normalisation des codes

    # candidats
    candidats["Code département"] = candidats["Code département"].apply(
        lambda x: normalize_code(x, 2)
    )

    # communes
    communes["code_departement"] = communes["code_departement"].apply(
        lambda x: normalize_code(x, 2)
    )
    communes["code_region"] = communes["code_region"].apply(
        lambda x: normalize_code(x, 2)
    )
    communes["code_commune_INSEE"] = communes["code_commune_INSEE"].apply(
        lambda x: normalize_code(x, 5)
    )

    # supprimer les doublons sur le code commune INSEE
    communes = communes.drop_duplicates(subset=["code_commune_INSEE"]).copy()

    # insee
    insee["DEP"] = insee["DEP"].apply(lambda x: normalize_code(x, 2))
    insee["REG"] = insee["REG"].apply(lambda x: normalize_code(x, 2))
    insee["CODGEO"] = insee["CODGEO"].apply(lambda x: normalize_code(x, 5))

    # departements-france
    departements["code_departement"] = departements["code_departement"].apply(
        lambda x: normalize_code(x, 2)
    )
    departements["code_region"] = departements["code_region"].apply(
        lambda x: normalize_code(x, 2)
    )

    # regions-france
    regions["code_region"] = regions["code_region"].apply(
        lambda x: normalize_code(x, 2)
    )

    # Filtres département 31
    candidats = candidats[candidats["Code département"] == DEPARTEMENT].copy()
    communes = communes[communes["code_departement"] == DEPARTEMENT].copy()
    insee = insee[insee["DEP"] == DEPARTEMENT].copy()

    # departements : on garde tous les départements

    # Têtes de liste uniquement
    candidats = candidats[
        candidats["Tête de liste"].astype(str).str.strip().str.upper() == "OUI"
    ].copy()

    # Sauvegarde
    save_csv(candidats, os.path.join(CLEAN_DIR, "candidats-2026.csv"), sep=";")
    save_csv(communes, os.path.join(CLEAN_DIR, "communes.csv"), sep=",")
    save_csv(insee, os.path.join(CLEAN_DIR, "insee_communes.csv"), sep=";")
    save_csv(departements, os.path.join(CLEAN_DIR, "departements-france.csv"), sep=",")
    save_csv(regions, os.path.join(CLEAN_DIR, "regions-france.csv"), sep=",")

    print("Nettoyage terminé.")
    print(f"Département filtré : {DEPARTEMENT}")
    print(f"Candidats gardés : {len(candidats)}")
    print(f"Communes gardées : {len(communes)}")
    print(f"INSEE gardées : {len(insee)}")
    print(f"Départements gardés : {len(departements)}")
    print(f"Régions gardées : {len(regions)}")
    print("Fichiers créés dans le dossier clean/")


if __name__ == "__main__":
    main()