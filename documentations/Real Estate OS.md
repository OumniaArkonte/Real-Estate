# Real Estate OS Documentation

## Overview

The Real Estate OS is a comprehensive AI-driven platform designed to manage property valuation operations through a specialized module: the Property Valuation Team. Agents in this module collaborate in **Coordinate Mode** to ensure accurate, efficient, and data-driven property assessments.

### Core Purpose

This system transforms traditional property valuation into an intelligent, automated process. It ensures that every step—from data collection to final recommendation—is handled with precision, consistency, and actionable insights.

## Module Architecture

### Teams and Modes

#### Module: Property Valuation Team (Coordinate Mode)

**Mode**: Coordinate - Agents work independently but share data and insights for comprehensive property assessment

* **Agent 1 (DataCollectionAgent)**: Collects property attributes, comparable sales, and market signals
* **Agent 2 (KnowledgeBaseAgent)**: Ingests, normalizes, and indexes property knowledge
* **Agent 3 (ValuationAgent)**: Applies multi-method property valuation
* **Agent 4 (MarketComparisonAgent)**: Contextualizes valuation against market trends
* **Agent 5 (AdvisoryAgent)**: Provides actionable recommendations
* **Agent 6 (ValidationAgent)**: Validates valuations and audits source data

## Dependencies Between Agents

### Intra-Team Dependencies

* **DataCollectionAgent → ValuationAgent & KnowledgeBaseAgent**: Supplies structured property and comparable data
* **KnowledgeBaseAgent → All Agents**: Provides clean knowledge base for analytics
* **ValuationAgent → MarketComparisonAgent & AdvisoryAgent**: Delivers multi-method valuation results
* **MarketComparisonAgent → ValidationAgent & AdvisoryAgent**: Supplies market context and signals
* **ValidationAgent → AdvisoryAgent**: Sends confidence scores and flags inconsistencies
* **AdvisoryAgent → Output**: Integrates all inputs to produce final recommendations

## Detailed Agent Analysis

### Agent 1: DataCollectionAgent

**Purpose**: Collects and normalizes property data for valuation and knowledge ingestion

**Key Responsibilities**:

* Extracts property attributes: address, size, bedrooms, bathrooms, lot, year, condition, amenities
* Collects comparable sales within defined geographic areas
* Gathers market signals: DOM, inventory, price trends, local projects

**Pre-built Tools**: `FileTools`, `GoogleSearchTools`, `PandasTools`, `FinancialDatasetsTools`
**Custom Tools**:

```python
@tool(description="Collect property data")
def collect_property_data(source_url: str) -> dict:
    pass

@tool(description="Retrieve comparable sales")
def retrieve_comparables(property_id: str) -> list:
    pass

@tool(description="Gather market signals")
def collect_market_signals(location: str) -> dict:
    pass
```

---

### Agent 2: KnowledgeBaseAgent

**Purpose**: Manages property knowledge ingestion, normalization, and indexing

**Key Responsibilities**:

* Organizes documents and datasets for property analysis
* Standardizes formats and semantic chunking
* Builds and updates searchable vector indices

**Pre-built Tools**: `FileTools`, `PandasTools`, `kb_ingest_indexer`, `dataset_registry`
**Custom Tools**:

```python
@tool(description="Ingest property knowledge")
def ingest_property_knowledge(documents: list) -> dict:
    pass

@tool(description="Build vector index")
def build_vector_index(dataset: dict) -> str:
    pass
```

---

### Agent 3: ValuationAgent

**Purpose**: Computes multi-method property valuations

**Key Responsibilities**:

* Calculates price per square foot, adjusted comparables, ML regression predictions
* Aggregates valuations into final weighted result
* Explains key factors affecting valuation

**Pre-built Tools**: `FileTools`, `PandasTools`, `CalculatorTools`, `PythonTools`, `avm_engine`, `comps_analyzer`
**Custom Tools**:

```python
@tool(description="Apply AVM methodologies")
def apply_avm(property_data: dict) -> dict:
    pass

@tool(description="Generate valuation summary")
def generate_valuation_summary(property_data: dict) -> dict:
    pass
```

---

### Agent 4: MarketComparisonAgent

**Purpose**: Compares valuation against local and regional market trends

**Key Responsibilities**:

* Computes delta to market percentiles
* Monitors inventory levels, DOM, and price adjustments
* Provides context for trends, risks, and opportunities

**Pre-built Tools**: `FileTools`, `PandasTools`, `FinancialDatasetsTools`, `market_trend_analyzer`, `market_monitor`
**Custom Tools**:

```python
@tool(description="Compare property to market")
def compare_to_market(valuation: dict, market_data: dict) -> dict:
    pass

@tool(description="Generate market context")
def generate_market_context(property_id: str) -> dict:
    pass
```

---

### Agent 5: AdvisoryAgent

**Purpose**: Produces actionable recommendations based on valuation and market context

**Key Responsibilities**:

* Generates buy/hold/sell advice
* Provides maintenance and repair plans
* Highlights negotiation points and opportunities

**Pre-built Tools**: `FileTools`, `CalculatorTools`, `maintenance_cost_estimator`
**Custom Tools**:

```python
@tool(description="Generate property recommendations")
def generate_recommendations(valuation: dict, market_context: dict) -> dict:
    pass
```

---

### Agent 6: ValidationAgent

**Purpose**: Ensures accuracy and reliability of valuations and source data

**Key Responsibilities**:

* Cross-validates multi-method valuations
* Audits source data for freshness and completeness
* Assigns confidence scores and flags inconsistencies

**Pre-built Tools**: `FileTools`, `PandasTools`, `CalculatorTools`, `cross_validation_checker`, `source_consistency_audit`
**Custom Tools**:

```python
@tool(description="Validate valuations")
def validate_valuation(valuation: dict) -> dict:
    pass

@tool(description="Audit data sources")
def audit_sources(data_sources: list) -> dict:
    pass
```

---

## Integration and Workflow

### Cross-Agent Communication

* **Shared Data Layer**: MLS integration, property databases, market datasets
* **Event-Driven Updates**: Agents update others upon data changes
* **Quality Gates**: ValidationAgent ensures data reliability before AdvisoryAgent recommendations
* **Feedback Loops**: Continuous improvement through analytics and performance metrics

### Workflow Examples

1. **Data Collection & Knowledge Management**:

   * DataCollectionAgent gathers property info → KnowledgeBaseAgent indexes it
2. **Valuation Computation**:

   * ValuationAgent receives structured property & comparables → calculates valuations
3. **Market Comparison & Advisory**:

   * MarketComparisonAgent contextualizes valuation → AdvisoryAgent generates recommendations
4. **Validation & Final Reporting**:

   * ValidationAgent cross-checks data and valuations → final validated report delivered

## Success Metrics

* Valuation accuracy and confidence
* Market comparison completeness
* Advisory recommendation relevance and actionability
* Source data integrity and audit completeness

This Property Valuation OS module ensures **accurate, comprehensive, and actionable property insights**, creating a data-driven ecosystem for real estate valuation.
