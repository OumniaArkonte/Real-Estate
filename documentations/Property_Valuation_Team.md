# 🏠 Module: Property Valuation Team

## Team Overview
**Team Name:** Property Valuation Team  
**Team Mode:** Coordinate  
**Purpose:** Accurate property assessment, market positioning, and actionable recommendations through AI-driven multi-agent analysis

---

### 📊 Agent 1: Data Collection Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Data Acquisition Specialist - Collects and normalizes property data from MLS, web, and uploaded documents  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Data Collection Agent automates the gathering and normalization of property attributes, comparable sales, and market signals, ensuring structured data is ready for valuation and knowledge ingestion.

#### 🔑 Primary Functions:

1. **Property Data Collection**
   - Extract property attributes (address, size, bedrooms, bathrooms, lot, year, condition, amenities)
   - Collect data from MLS, web sources, and uploaded documents
   - Normalize and deduplicate data across sources

2. **Comparable Sales Retrieval**
   - Identify recent and relevant comparable sales
   - Apply filters for distance, time window, and property similarity
   - Aggregate and clean comparable sales data

3. **Market Signal Enrichment**
   - Collect DOM, inventory, price variations, and local project data
   - Normalize macro and local market indicators
   - Document source provenance and freshness

#### 🛠 Tools:

- `FileTools`, `GoogleSearchTools`, `PandasTools`, `FinancialDatasetsTools`, `mls_integration`, `market_monitor`, `web_property_scraper`, `document_property_parser`

#### 📊 Results:

- `subject_property`: normalized property attributes  
- `comparable_sales`: structured list of comparable transactions  
- `source_metadata`: provenance, freshness, applied filters

---

### 📊 Agent 2: Knowledge Base Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Knowledge Management Specialist - Ingestion, normalization, and vector indexing of property knowledge  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Knowledge Base Agent manages the ingestion, cleaning, and semantic indexing of documents and datasets for fast and reliable retrieval by other agents.

#### 🔑 Primary Functions:

1. **Corpus Management**
   - Organize documents (valuation reports, methodologies, inspection reports)
   - Track dataset versions, freshness, and provenance

2. **Data Ingestion & Normalization**
   - Standardize formats, encoding, and schemas
   - Apply semantic chunking and embeddings

3. **Vector Indexing**
   - Create searchable vector collections
   - Update incrementally or rebuild collections as needed

#### 🛠 Tools:

- `FileTools`, `PandasTools`, `kb_ingest_indexer`, `dataset_registry`

#### 📊 Results:

- `registry_update`: dataset registry status  
- `ingestion_report`: indexing details and KB updates

---

### 📊 Agent 3: Valuation Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Valuation Specialist - Computes multi-method property valuations  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Valuation Agent calculates property valuations using multiple methods (price per sqft, adjusted comparables, ML regression), aggregates them, and provides detailed explanations.

#### 🔑 Primary Functions:

1. **Multi-Method Valuation**
   - Calculate ppsf, adjusted comparables, and ML-based predictions
   - Aggregate into final weighted valuation

2. **Factor Analysis**
   - Explain key drivers: size, rooms, bathrooms, lot, age, condition
   - Adjust valuations based on comparable sales and market context

3. **Output Structuring**
   - Present detailed methods, adjustments, assumptions, and valuation date

#### 🛠 Tools:

- `FileTools`, `PandasTools`, `CalculatorTools`, `PythonTools`, `avm_engine`, `comps_analyzer`, `valuation_model_runner`

#### 📊 Results:

- `valuation_methods`: detailed per-method valuations  
- `final_valuation`: aggregated property value  
- `notes`: assumptions, limitations, and date

---

### 📊 Agent 4: Market Comparison Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Market Intelligence Specialist - Compares property value to local/regional market  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Market Comparison Agent evaluates the subject property against local market trends, calculates deltas, and contextualizes valuations with market indicators.

#### 🔑 Primary Functions:

1. **Market Positioning**
   - Compare ppsf of subject property vs local percentiles (p25/p50/p75)
   - Compute `delta_to_market_pct`

2. **Trend & Signal Analysis**
   - Evaluate growth, volatility, and market phase
   - Monitor DOM, inventory, and price adjustments

3. **Contextual Insights**
   - Provide macro and local context affecting property value
   - Identify market opportunities or risks

#### 🛠 Tools:

- `FileTools`, `PandasTools`, `FinancialDatasetsTools`, `market_trend_analyzer`, `market_monitor`, `CalculatorTools`

#### 📊 Results:

- `market_positioning`, `trend_context`, `signals`

---

### 📊 Agent 5: Advisory Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Recommendation Specialist - Generates actionable property advice  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Advisory Agent provides recommendations (buy/hold/sell), maintenance plans, and negotiation points based on valuation and market analysis.

#### 🔑 Primary Functions:

1. **Recommendation Generation**
   - Determine buy/hold/sell stance based on delta_to_market_pct and risk factors
   - Provide concise rationale

2. **Maintenance Planning**
   - Estimate priority and cost of repairs/upgrades
   - Suggest actionable improvements

3. **Negotiation Insights**
   - Highlight key negotiation points based on market/value discrepancies

#### 🛠 Tools:

- `FileTools`, `CalculatorTools`, `maintenance_cost_estimator`, `advice_policy_rules`

#### 📊 Results:

- `recommendation`, `maintenance_plan`, `negotiation_points`

---

### 📊 Agent 6: Validation Agent

**Model:** `MistralChat(id="mistral-small-latest")`  
**Role:** Quality Assurance Specialist - Validates valuations and audits source data  
**Architecture:** Team Member (Property Valuation Team)

#### ❤️ What it does:

Validation Agent ensures the accuracy and consistency of property valuations across methods and audits data sources for reliability.

#### 🔑 Primary Functions:

1. **Cross-Validation**
   - Compare valuation methods and detect discrepancies

2. **Source Auditing**
   - Check data freshness, completeness, and price dispersion

3. **Confidence Scoring**
   - Assign confidence scores and flag critical issues

#### 🛠 Tools:

- `FileTools`, `PandasTools`, `CalculatorTools`, `cross_validation_checker`, `source_consistency_audit`

#### 📊 Results:

- `validation_report`, `source_audit`

---

## 🤝 Team Coordination

### **Coordinate Mode Workflow:**

1. **DataCollectionAgent** → Provides structured property & comparable data to **ValuationAgent** and **KnowledgeBaseAgent**  
2. **KnowledgeBaseAgent** → Supplies clean knowledge base resources to all agents  
3. **ValuationAgent** → Produces multi-method valuations for **MarketComparisonAgent** and **AdvisoryAgent**  
4. **MarketComparisonAgent** → Contextualizes valuations vs market and sends insights to **ValidationAgent** and **AdvisoryAgent**  
5. **ValidationAgent** → Validates valuations and sources, feeds confidence scores to **AdvisoryAgent**  
6. **AdvisoryAgent** → Produces final recommendations integrating all inputs

### **Output Standards:**

- Comprehensive property report including valuation, market comparison, confidence score, and actionable recommendations  
- Traceable data provenance and metadata for all analyses  
- Multi-method valuations and aggregated final value  
- Condition-based adjustments, trend insights, and risk assessment

### **Goal:**

Provide **accurate, comprehensive, and reliable property valuations** with actionable insights for real estate decision-making.
