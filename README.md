# visuo-ETL

## Process Flow

- **SchemaAnalyzerAgent**:
  - Parses the Target Schema into individual fields.
  - Get all the tables and its field from the csv and store it as a dictionary.
  - For each Target Field, use the tables dict to get the mapping using Gemini LLM
  - A Dict with Target Fields as key and mapping as the value. 
      - Mapping has 3 keys:
          - `source_field`
          - `transformation (if any)`
          - `isDirect` (True if one-to-one mapping, False if transformation is needed) 