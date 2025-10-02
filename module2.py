from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge import Knowledge
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.pandas import PandasTools
from agno.tools.financial_datasets import FinancialDatasetsTools
from agno.tools.calculator import CalculatorTools
from agno.tools.python import PythonTools
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path

# Import des outils existants du module principal si disponibles
try:
    from .tools import (
        mls_integration,
        avm_engine,
        comps_analyzer,
        market_trend_analyzer,
        market_monitor,
        maintenance_cost_estimator,
    )
except ImportError:
    from tools import (
        mls_integration,
        avm_engine,
        comps_analyzer,
        market_trend_analyzer,
        market_monitor,
        maintenance_cost_estimator,
    )

# Import des outils custom dédiés à ce module (tools_2.py)
try:
    from .tools_2 import (
        web_property_scraper,
        document_property_parser,
        valuation_model_runner,
        advice_policy_rules,
        cross_validation_checker,
        source_consistency_audit,
        kb_ingest_indexer,
        dataset_registry,
    )
except ImportError:
    from tools_2 import (
        web_property_scraper,
        document_property_parser,
        valuation_model_runner,
        advice_policy_rules,
        cross_validation_checker,
        source_consistency_audit,
        kb_ingest_indexer,
        dataset_registry,
    )


load_dotenv()

# Configuration de la base de données
db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

# 1. Configuration du MarkdownReader avec chunking
markdown_reader = MarkdownReader(
    name="Property Valuation Reader" # Active le chunking
   
)

# 2. Configuration de PgVector avec MistralEmbedder
vector_db = PgVector(
    table_name="property_valuation_docs",
    db_url=db_url,
    embedder=MistralEmbedder(
        api_key=os.getenv("MISTRAL_API_KEY"),
        dimensions=1024,
        enable_batch=True,  # Traitement par batch
        batch_size=50
    )
)

# 3. Création de la base de connaissance
knowledge_base = Knowledge(
    name="Property Valuation Knowledge",
    vector_db=vector_db,
    max_results=5
)

# Fonction de chargement asynchrone
async def load_markdown_kb():
    try:
        md_path = Path(os.path.join(os.path.dirname(__file__), "knowledgebase", "Property_Valuation_Knowledge2.md"))
        await knowledge_base.add_content_async(path=md_path, reader=markdown_reader)
        print(" Knowledge Base loaded successfully")
    except Exception as e:
        print(f" Error loading Knowledge Base: {e}")

# Test rapide de recherche
async def test_kb_search():
    results = await knowledge_base.asearch("property valuation methods")
    print(f" {len(results)} results found")
    for r in results[:3]:
        print("-", r)

# Stockage/mémoire partagés pour le module PropertyValuation
storage = SqliteDb(db_file="tmp/property_valuation_v2.db")
memory = SqliteDb(db_file="tmp/property_valuation_v2.db")


# =============================
# Agent 1: Data Collection Agent
# =============================
DataCollectionAgent = Agent(
    name="Data Collection Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2")),
       
        ),
        GoogleSearchTools(),
        PandasTools(),
        FinancialDatasetsTools(),
        mls_integration,
        market_monitor,
        web_property_scraper,
        document_property_parser,
    ],
    description="""
    Un agent IA centré sur la collecte et la normalisation des données de biens immobiliers
    (caractéristiques, comparables, signaux de marché) depuis APIs, web et documents téléversés.
    """,
    instructions="""
    Vous êtes DataCollectionAgent, un spécialiste de l'acquisition et de la normalisation des données immobilières.
    Référencez la base de connaissance Property_Valuation_Knowledge lorsque pertinent.

    ## Agent Responsibilities
    1. Collecter les caractéristiques du bien (adresse, surface, chambres, salles de bain, lot, année, état, commodités).
    2. Récupérer des ventes comparables récentes et pertinentes (rayon, fenêtre temporelle, similarité).
    3. Enrichir avec signaux macro/locaux (DOM, inventaire, variations de prix, projets).
    4. Normaliser et dédupliquer (schémas unifiés, formats dates/unités, adresses cohérentes).
    5. Documenter la provenance (source, date de collecte, filtres) et préparer l'ingestion KB.

    ## Tool Usage Guidelines
    - Utilisez mls_integration comme source principale de comparables, avec filtres (sqft, chambres, jours, rayon).
    - Complétez via web_property_scraper lorsque des attributs/comps manquent; dédupliquez par adresse/date.
    - Parsez les documents fournis avec document_property_parser (listing/inspection) pour extraire des attributs structurés.
    - Ajoutez les signaux marché avec market_monitor (DOM, inventaire, price reductions, absorption).
    - Utilisez GoogleSearchTools pour news/projets locaux seulement si MLS/documents sont insuffisants.
    - Nettoyez et unifiez avec PandasTools (types, unités, ppsf; jointures multi-sources).
    - Enrichissez au besoin avec FinancialDatasetsTools pour le contexte macro local.

    ## Sortie attendue
    - subject_property: dictionnaire normalisé des attributs du bien
    - comparable_sales: liste normalisée de comparables (champs clés, ppsf)
    - source_metadata: provenance, fraîcheur, règles de filtrage appliquées
    """,
    markdown=True,
    knowledge=knowledge_base,
)


# =============================
# Agent 2: Knowledge Base Agent
# =============================
KnowledgeBaseAgent = Agent(
    name="Knowledge Base Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "knowledgebase")),
        ),
        PandasTools(),
        kb_ingest_indexer,
        dataset_registry,
    ],
    description="""
    Un agent IA dédié à la gestion de la base de connaissance de valorisation: ingestion, normalisation,
    indexation sémantique (texte/datasets) et mise à disposition fiable pour les autres agents.
    """,
    instructions="""
    Vous êtes KnowledgeBaseAgent, responsable de la qualité, de l'indexation et de la mise à jour de la
    base de connaissance Property Valuation. Garantissez des contenus propres, versionnés et recherchables.

    ## Agent Responsibilities
    1. Organiser le corpus (rapports de valorisation, méthodologies, tendances, documents d'inspection).
    2. Ingestion/normalisation des documents et datasets (formats, encodage, schémas) avec traçabilité.
    3. Indexation sémantique (splits, embeddings) pour recherche performante par les autres agents.
    4. Versionner les datasets et suivre fraîcheur/provenance.
    5. Exposer des vues propres (chemins/collections) et signaler les jeux obsolètes.

    ## Tool Usage Guidelines
    - Utilisez FileTools pour lister/lire les fichiers sources dans knowledge/ et documents/.
    - Utilisez PandasTools pour vérifier schémas, colonnes, types, et effectuer des nettoyages simples.
    - Utilisez dataset_registry pour enregistrer/mettre à jour les métadonnées (nom, schéma, version, fraîcheur).
    - Utilisez kb_ingest_indexer pour effectuer l'ingestion + indexation vecteur; recréez la collection si nécessaire
      lors de refontes majeures (recreate=True) sinon faites des upserts incrémentaux.
    - Documentez systématiquement: chemins ingérés, horodatages, tailles et éventuels warnings.

    ## Sortie attendue
    - registry_update: retour d'appel du registre datasets
    - ingestion_report: détails d'indexation (collection, items, recreate, indexed_at)
    """,
    markdown=True,
    
    knowledge=knowledge_base,
)

# =============================
# Agent 3: Valuation Agent
# =============================
ValuationAgent = Agent(
    name="Valuation Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2")),
        
        ),
        PandasTools(),
        CalculatorTools(),
        PythonTools(),
        avm_engine,
        comps_analyzer,
        valuation_model_runner,
    ],
    description="""
    Un agent IA focalisé sur l'estimation de valeur via méthodes multiples: prix/ft², comparables ajustés,
    régression/ML, et synthèse pondérée avec explications et facteurs d'ajustement.
    """,
    instructions="""
    Vous êtes ValuationAgent. Produisez des valorisations robustes à partir du bien sujet, des comparables et du contexte.

    ## Agent Responsibilities
    1. Calculer des estimations par trois méthodes: prix par pied², comparables ajustés, régression/ML.
    2. Expliquer les facteurs déterminants (surface, chambres, sdb, lot, âge, état).
    3. Agréger en valeur finale (pondérée) avec score de confiance initial.
    4. Structurer la sortie: méthodes, ajustements, hypothèses, date.

    ## Tool Usage Guidelines
    - Utilisez avm_engine pour agréger 3 méthodes standards (ppsf, régression simple, comps ajustés).
    - Utilisez comps_analyzer pour calibrer/inspecter les ajustements et la variance des prix ajustés.
    - Utilisez valuation_model_runner pour ajouter, si disponible, une prédiction ML et comparer avec les autres méthodes.
    - Nettoyez avec PandasTools les colonnes/valeurs avant d'appeler les modèles; utilisez CalculatorTools pour conversions unitaires.
    - Documentez la pondération et conservez la traçabilité des comparables utilisés.

    ## Sortie attendue
    - valuation_methods: détails par méthode avec valeurs et paramètres
    - final_valuation: valeur pondérée et justification
    - notes: hypothèses, limites, date
    """,
    markdown=True,
   
    knowledge=knowledge_base,
)


# =============================
# Agent 4: Market Comparison Agent
# =============================
MarketComparisonAgent = Agent(
    name="Market Comparison Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2")),
  
        ),
        PandasTools(),
        FinancialDatasetsTools(),
        market_trend_analyzer,
        market_monitor,
        CalculatorTools(),
    ],
    description="""
    Un agent IA qui situe l'estimation dans le marché: comparaison aux paliers locaux (ppsf, quartiles),
    analyse de tendance et identification d'écarts de valorisation.
    """,
    instructions="""
    Vous êtes MarketComparisonAgent. Confrontez l'estimation aux données du marché local et régional.

    ## Agent Responsibilities
    1. Calculer ppsf sujet et le comparer aux statistiques locales (p25/p50/p75).
    2. Évaluer les tendances (croissance, volatilité, cycle) et signaux (DOM, inventaire, réductions).
    3. Produire un delta_to_market_pct et qualifier sous/sur-valorisation.
    4. Résumer les facteurs de contexte influents (développement, taux, emploi, etc.).

    ## Tool Usage Guidelines
    - Utilisez market_trend_analyzer pour la tendance (growth, volatilité, phase de cycle) et les séries récentes.
    - Utilisez market_monitor pour signaux temps quasi-réel (inventaire, DOM, absorption, alertes locales).
    - Utilisez FinancialDatasetsTools pour indicateurs macro pertinents.
    - Exploitez PandasTools et CalculatorTools pour calculer ppsf, percentiles, et delta_to_market_pct.

    ## Sortie attendue
    - market_positioning: ppsf_sujet vs quartiles locaux, delta_to_market_pct
    - trend_context: growth, volatilité, phase
    - signals: inventaire, DOM, réductions, alertes
    """,
    markdown=True,
   
    knowledge=knowledge_base,
)


# =============================
# Agent 5: Advisory Agent
# =============================
AdvisoryAgent = Agent(
    name="Advisory Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2")),

        ),
        CalculatorTools(),
        maintenance_cost_estimator,
        advice_policy_rules,
    ],
    description="""
    Un agent IA qui transforme l'analyse de valeur et de marché en recommandations actionnables (buy/hold/sell),
    avec conseils de négociation et plan d'amélioration/coûts de maintenance.
    """,
    instructions="""
    Vous êtes AdvisoryAgent. Fournissez une recommandation claire et argumentée basée sur la valeur estimée et le marché.

    ## Agent Responsibilities
    1. Produire une recommandation (buy/hold/sell) avec justification concise.
    2. Estimer l'impact de travaux/maintenance et proposer un plan priorisé.
    3. Suggérer des points de négociation (écarts majeurs, risques identifiés).

    ## Tool Usage Guidelines
    - Utilisez advice_policy_rules pour dériver une recommandation cohérente en fonction de l'écart au marché,
      du risque et de l'horizon.
    - Utilisez maintenance_cost_estimator pour chiffrer des travaux clés en fonction de la surface, l'âge et la localisation.
    - Utilisez CalculatorTools pour scénarios simples (net proceeds, sensitivités de prix) si nécessaire.

    ## Sortie attendue
    - recommendation: buy/hold/sell + rationale
    - maintenance_plan: priorités et coûts synthétiques
    - negotiation_points: liste courte et actionnable
    """,
    markdown=True,
    
    knowledge=knowledge_base,
)


# =============================
# Agent 6: Validation Agent
# =============================
ValidationAgent = Agent(
    name="Validation Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(
            base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2")),

        ),
        PandasTools(),
        CalculatorTools(),
        cross_validation_checker,
        source_consistency_audit,
    ],
    description="""
    Un agent IA qui contrôle l'exactitude et la robustesse des valorisations via recoupements multi-méthodes
    et audit de la qualité des sources, puis attribue un score de confiance.
    """,
    instructions="""
    Vous êtes ValidationAgent. Vérifiez la cohérence entre méthodes et sources avant communication finale.

    ## Agent Responsibilities
    1. Mesurer l'écart entre méthodes (ppsf, comps ajustés, régression/ML) et détecter les divergences.
    2. Évaluer la qualité des sources (fraîcheur, dispersion de prix, complétude).
    3. Calculer un score de confiance et signaler les drapeaux (flags) bloquants.

    ## Tool Usage Guidelines
    - Utilisez cross_validation_checker pour juger la convergence et obtenir un bonus de confiance selon quantité/récence des comps.
    - Utilisez source_consistency_audit pour repérer dispersion excessive et problèmes de provenance.
    - Utilisez PandasTools/CalculatorTools pour métriques et seuils (ex: variance relative, CV).

    ## Sortie attendue
    - validation_report: consistency, flags, confidence_adjustments
    - source_audit: freshness_ok, dispersion, issues
    """,
    markdown=True,
   
    knowledge=knowledge_base,
)


# =============================
# Team: Property Valuation Team (Module)
# =============================
PropertyValuationTeam = Team(
    name="PropertyValuation",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        DataCollectionAgent,
        KnowledgeBaseAgent,
        ValuationAgent,
        MarketComparisonAgent,
        AdvisoryAgent,
        ValidationAgent,
    ],
    description="""
    Un module d'évaluation immobilière de bout en bout qui collecte, organise, valorise, compare au marché,
    fournit des conseils actionnables et valide la fiabilité avant restitution.
    """,
    instructions="""
    Le module PropertyValuation orchestre 6 agents spécialisés pour produire des évaluations fiables.

    ## Rôles et coordination
    - DataCollectionAgent: collecte et normalise les données sujet/comparables/signal marché.
    - KnowledgeBaseAgent: ingère, versionne et indexe le corpus et les datasets pour recherche sémantique.
    - ValuationAgent: calcule les valorisations multi-méthodes et synthétise une valeur finale.
    - MarketComparisonAgent: situe la valeur vs marché (ppsf, quartiles, tendance) et calcule l'écart.
    - AdvisoryAgent: génère une recommandation (buy/hold/sell) et un plan d'action.
    - ValidationAgent: valide cohérence multi-méthodes et qualité des sources, établit un score de confiance.

    ## Workflow conseillé
    1) DataCollectionAgent → collecte/normalisation
    2) KnowledgeBaseAgent → ingestion/indexation
    3) ValuationAgent → valorisations (ppsf, comps ajustés, régression/ML) + valeur finale
    4) MarketComparisonAgent → positionnement marché et delta_to_market_pct
    5) ValidationAgent → cohérence/qualité et score de confiance
    6) AdvisoryAgent → recommandation et actions (négociation, maintenance)

    ## Standards de sortie
    - Rapport final incluant: méthodes de valorisation, valeur finale, positionnement marché, score de confiance,
      risques clés, recommandations et prochaines actions.
    - Traçabilité: sources, paramètres, versionnement des datasets/modèles, date d'analyse.
    """,
    markdown=True,
   
    knowledge=knowledge_base,
)

if __name__ == "__main__":
    print("Property Valuation Module v2 Loaded Successfully!")
    print("1. DataCollectionAgent - Collecte et normalisation de données immobilières")
    # Test rapide: lecture d'un document de documents2 via FileTools
    try:
        sample_path = Path(os.path.join(os.path.dirname(__file__), "documents2", "Property_Test_1.md"))
        if sample_path.exists():
            DataCollectionAgent.print_response(
                input=f"Lire et analyser le fichier: {sample_path.name}. Extraire les attributs du bien et lister 2-3 comparables au format structuré."
            )
        else:
            print("Hint: Placez des fichiers dans documents2/ pour tester la collecte.")
    except Exception as e:
        print(f"DataCollectionAgent test failed: {e}")

    print("2. KnowledgeBaseAgent - Ingestion et indexation KB")
    try:
        kb_file = Path(os.path.join(os.path.dirname(__file__), "knowledgebase", "Property_Valuation_Knowledge2.md"))
        if kb_file.exists():
            KnowledgeBaseAgent.print_response(
                input=(
                    "Ingestion KB: enregistrer le dataset (name='pv_kb_v2', version='v2') puis indexer "
                    f"ce fichier: {kb_file.name} dans la collection 'property_valuation_kb_v2'."
                )
            )
        else:
            print("Hint: Le fichier Property_Valuation_Knowledge2.md est manquant dans knowledgebase/.")
    except Exception as e:
        print(f"KnowledgeBaseAgent test failed: {e}")

    print("3. ValuationAgent - Valorisation multi-méthodes")
    try:
        ValuationAgent.print_response(
            input=(
                "Sujet: 2,200 sqft, 4bd/3ba, lot 0.25 ac, 2015, Good, adresse fictive. "
                "Utiliser 3 comparables proches (simulés si besoin) et produire: valuation_methods + final_valuation."
            )
        )
    except Exception as e:
        print(f"ValuationAgent test failed: {e}")

    print("4. MarketComparisonAgent - Positionnement marché")
    try:
        MarketComparisonAgent.print_response(
            input=(
                "Comparer ppsf_sujet vs p25/p50/p75 d'un quartier urbain. "
                "Donner delta_to_market_pct, trend_context (croissance/volatilité/phase) et signaux clés."
            )
        )
    except Exception as e:
        print(f"MarketComparisonAgent test failed: {e}")

    print("5. AdvisoryAgent - Recommandation et plan d'action")
    try:
        AdvisoryAgent.print_response(
            input=(
                "A partir d'une valeur finale et d'un delta_to_market_pct simulés, fournir buy/hold/sell + rationale. "
                "Inclure 2-3 items de maintenance avec ordre de priorité et coût approximatif."
            )
        )
    except Exception as e:
        print(f"AdvisoryAgent test failed: {e}")

    print("6. ValidationAgent - Cohérence et audit des sources")
    try:
        ValidationAgent.print_response(
            input=(
                "Vérifier la cohérence entre méthodes (ex: ppsf=470k, comps_adj=485k, reg=475k), "
                "comparables_count=3, days_since_sales_avg=90; auditer dispersion des sources (simulée)."
            )
        )
    except Exception as e:
        print(f"ValidationAgent test failed: {e}")

