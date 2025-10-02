from agno.tools import tool
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


@tool(
    name="web_property_scraper",
    description="Scrape multi-sources (requêtes web/listings) et normalise les champs principaux du bien et des comparables",
    show_result=True,
)
def web_property_scraper(
    query: str,
    location: str,
    max_results: int = 50,
    radius_km: float = 3.0,
) -> Dict[str, Any]:
    """
    Simule un scraping léger multi-sources (listings/portails) avec normalisation minimale.

    Args:
        query: Chaîne de recherche (adresse/attributs)
        location: Localisation cible (ville/quartier)
        max_results: Nombre max de résultats souhaités
        radius_km: Rayon de recherche en kilomètres

    Returns:
        Dictionnaire contenant les résultats normalisés et les métadonnées de collecte
    """
    normalized_results: List[Dict[str, Any]] = []

    # Génère quelques résultats simulés et normalisés (ppsf calculé si possible)
    sample = [
        {
            "address": "123 Sample St, {}".format(location),
            "list_price": 460000,
            "sqft": 2200,
            "bedrooms": 3,
            "bathrooms": 2.5,
            "lot_size": 0.22,
            "year_built": 2012,
            "amenities": ["garage", "garden"],
            "source": "web",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        {
            "address": "456 Example Ave, {}".format(location),
            "list_price": 485000,
            "sqft": 2400,
            "bedrooms": 4,
            "bathrooms": 3,
            "lot_size": 0.30,
            "year_built": 2015,
            "amenities": ["garage"],
            "source": "web",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    ]

    for item in sample[: max_results]:
        ppsf = None
        if item.get("list_price") and item.get("sqft"):
            try:
                ppsf = round(item["list_price"] / item["sqft"], 2)
            except Exception:
                ppsf = None
        normalized_results.append({**item, "price_per_sqft": ppsf})

    return {
        "query": query,
        "location": location,
        "radius_km": radius_km,
        "results": normalized_results,
        "normalized": True,
        "collected_at": datetime.now().isoformat(),
    }


@tool(
    name="document_property_parser",
    description="Extrait des attributs structurés d'un bien depuis des documents texte (listing/inspection)",
    show_result=True,
)
def document_property_parser(
    file_path: str,
    doc_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Parseur minimaliste de documents texte: détecte adresse, surface, chambres/sdb, année, et autres motifs simples.

    Args:
        file_path: Chemin vers un fichier texte lisible
        doc_type: Type de document (listing, inspection, autre)

    Returns:
        Dictionnaire des champs extraits + résumé des lignes correspondantes
    """
    extracted: Dict[str, Any] = {
        "address": None,
        "sqft": None,
        "bedrooms": None,
        "bathrooms": None,
        "lot_size": None,
        "year_built": None,
        "amenities": [],
    }

    matched_lines: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Lecture impossible: {str(e)}", "file_path": file_path, "doc_type": doc_type}

    # Motifs simples (robustes aux variations de casse)
    patterns = {
        "address": r"address\s*[:\-]?\s*(.+)$",
        "sqft": r"(sqft|square\s*feet)\s*[:\-]?\s*(\d{3,6})",
        "bedrooms": r"bed(room)?s?\s*[:\-]?\s*(\d{1,2})",
        "bathrooms": r"bath(room)?s?\s*[:\-]?\s*(\d{1,2}(?:\.\d)?)",
        "lot_size": r"lot\s*size\s*[:\-]?\s*(\d{1,2}(?:\.\d{1,2})?)",
        "year_built": r"year\s*built\s*[:\-]?\s*(\d{4})",
    }

    for key, pat in patterns.items():
        m = re.search(pat, content, re.IGNORECASE | re.MULTILINE)
        if m:
            val = m.group(1) if key == "address" else m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
            matched_lines.append(m.group(0))
            try:
                if key in ["sqft"]:
                    extracted[key] = int(val)
                elif key in ["bedrooms"]:
                    extracted[key] = int(float(val))
                elif key in ["bathrooms", "lot_size"]:
                    extracted[key] = float(val)
                elif key in ["year_built"]:
                    extracted[key] = int(val)
                else:
                    extracted[key] = val.strip()
            except Exception:
                extracted[key] = val

    # Amenities basées sur mots-clés simples
    amenities_map = ["garage", "pool", "garden", "balcony", "fireplace"]
    for amenity in amenities_map:
        if re.search(rf"\b{amenity}\b", content, re.IGNORECASE):
            extracted["amenities"].append(amenity)

    return {
        "file_path": file_path,
        "doc_type": doc_type,
        "extracted": extracted,
        "matched_examples": matched_lines[:5],
        "parsed_at": datetime.now().isoformat(),
    }


# =============================
# Outils Knowledge Base (Agent 2)
# =============================

@tool(
    name="kb_ingest_indexer",
    description="Ingestion et indexation vecteur de documents/datasets de valorisation pour la base de connaissance",
    show_result=True,
)
def kb_ingest_indexer(
    paths: List[str],
    collection: str,
    recreate: bool = False,
) -> Dict[str, Any]:
    """
    Simule une pipeline d'ingestion: lecture, split, embeddings, et upsert dans un index vecteur.

    Args:
        paths: Liste de chemins de fichiers/dossiers à ingérer
        collection: Nom de la collection cible
        recreate: Si True, recrée la collection (destructive)

    Returns:
        Détails d'ingestion: nombre d'éléments, collection, recréation, horodatage
    """
    return {
        "collection": collection,
        "ingested_items": len(paths),
        "recreated": recreate,
        "indexed_at": datetime.now().isoformat(),
    }


@tool(
    name="valuation_model_runner",
    description="Exécute un modèle ML/AutoML de valorisation (features -> valeur + explications)",
    show_result=True,
)
def valuation_model_runner(
    model_name: str,
    features: Dict[str, Any],
    version: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Simule l'exécution d'un modèle ML versionné. Retourne une prédiction et un squelette d'explicabilité.
    """
    # Heuristique simple sur ppsf si disponible
    pred = None
    if features and features.get("sqft") and features.get("price_per_sqft"):
        try:
            pred = round(features["sqft"] * features["price_per_sqft"], 2)
        except Exception:
            pred = None
    return {
        "model_name": model_name,
        "version": version,
        "prediction": pred,
        "explain": {"top_features": ["sqft", "price_per_sqft", "bedrooms", "bathrooms"]},
        "run_at": datetime.now().isoformat(),
    }


@tool(
    name="advice_policy_rules",
    description="Génère une recommandation (buy/hold/sell) selon règles (écart marché, risque, horizon)",
    show_result=True,
)
def advice_policy_rules(
    delta_to_market_pct: float,
    risk_level: str,
    horizon_months: int,
) -> Dict[str, Any]:
    """
    Moteur de règles minimal pour transformer des signaux en recommandation simple.
    """
    decision = "hold"
    rationale = []
    if delta_to_market_pct < -5:
        decision = "buy"
        rationale.append("Sous-évaluation détectée")
    elif delta_to_market_pct > 5:
        decision = "sell"
        rationale.append("Surévaluation par rapport au marché")
    if risk_level.lower() in ["high", "elevated"]:
        rationale.append("Risque élevé: prudence recommandée")
        if decision == "buy":
            decision = "hold"
    if horizon_months < 6 and decision == "buy":
        rationale.append("Horizon court: liquidité prioritaire")
        decision = "hold"
    return {"recommendation": decision, "rationale": rationale, "inputs": {
        "delta_to_market_pct": delta_to_market_pct,
        "risk_level": risk_level,
        "horizon_months": horizon_months,
    }}


@tool(
    name="cross_validation_checker",
    description="Valide la cohérence entre méthodes (ppsf, comparables ajustés, régression/ML)",
    show_result=True,
)
def cross_validation_checker(
    method_values: Dict[str, float],
    comparables_count: int,
    days_since_sales_avg: float,
) -> Dict[str, Any]:
    """
    Vérifie l'accord entre méthodes et pondère la confiance selon quantité/récence des comps.
    """
    values = [v for v in method_values.values() if isinstance(v, (int, float))]
    consistency = True
    flags: List[str] = []
    confidence_bonus = 0.0
    if values:
        avg = sum(values) / len(values)
        max_dev = max(abs(v - avg) / avg for v in values if avg)
        if max_dev > 0.2:
            consistency = False
            flags.append("Divergence > 20% entre méthodes")
    if comparables_count >= 3:
        confidence_bonus += 0.2
    if days_since_sales_avg < 180:
        confidence_bonus += 0.2
    return {"consistency": consistency, "flags": flags, "confidence_bonus": round(confidence_bonus, 2)}


@tool(
    name="source_consistency_audit",
    description="Audit des sources (fraîcheur, dispersion de prix, provenance)",
    show_result=True,
)
def source_consistency_audit(
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Évalue des indicateurs simples de qualité des sources: fraîcheur moyenne, dispersion approximative.
    """
    freshness_ok = True
    issues: List[str] = []
    dispersion = 0.0
    try:
        prices = [s.get("sale_price") for s in sources if isinstance(s.get("sale_price"), (int, float))]
        if len(prices) >= 2:
            avg = sum(prices) / len(prices)
            if avg:
                dispersion = max(abs(p - avg) / avg for p in prices)
                if dispersion > 0.35:
                    issues.append("Dispersion de prix élevée entre sources")
        # Freshness heuristique: acception par défaut
        freshness_ok = True
    except Exception:
        issues.append("Erreur lors de l'audit des sources")
    return {"freshness_ok": freshness_ok, "dispersion": round(dispersion, 3), "issues": issues}

@tool(
    name="dataset_registry",
    description="Catalogue/versionnement de datasets (nom, schéma, version, fraîcheur)",
    show_result=True,
)
def dataset_registry(
    action: str,
    name: str,
    schema: Optional[Dict[str, Any]] = None,
    version: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Petit registre de datasets pour documenter schémas/versions et opérations basiques.

    Args:
        action: 'register' | 'update' | 'info'
        name: Nom du dataset
        schema: Schéma optionnel (colonnes, types)
        version: Version du dataset

    Returns:
        Résumé d'opération pour traçabilité
    """
    return {
        "action": action,
        "name": name,
        "version": version,
        "schema": schema,
        "updated_at": datetime.now().isoformat(),
    }


