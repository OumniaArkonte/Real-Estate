import pandas as pd
# Créer des comparables simulés
comps_data = {
    "address": [
        "123 Main St",
        "456 Oak Ave",
        "789 Pine Rd"
    ],
    "sqft": [2150, 2200, 2300],
    "bedrooms": [4, 4, 4],
    "bathrooms": [3, 3, 3],
    "lot_size": [0.25, 0.30, 0.20],
    "year_built": [2014, 2016, 2015],
    "condition": ["Good", "Excellent", "Good"],
    "sale_price": [400000, 450000, 420000]
}

# Créer un DataFrame pandas
comps_df = pd.DataFrame(comps_data)

# Sauvegarder le DataFrame dans un fichier CSV
comps_df.to_csv('comparables.csv', index=False)

# Retourner le nom du fichier CSV
'comparables.csv'