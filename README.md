# MDB_final_project

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (version >= 3.6)
- pip (Python package installer)

## Installation

1. **Flask:**
   ```bash
   pip3 install Flask
   ```

2. **Pandas:**
   ```bash
   pip3 install pandas
   ```

3. **MongoDB:**
   ```bash
   pip3 install pymongo
   ```
   Install MongoDB Compass [here](https://www.mongodb.com/try/download/compass)

4. **Neo4j:**
   ```bash
   pip3 install neo4j
   ```
   Install Neo4j server [here](https://neo4j.com/download/)

5. **Book Review Data:**
   
   The dataset being used is [here](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews?select=books_data.csv)

   **License:**
   The book review dataset is provided under the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/). This means the dataset is released into the public domain, and you are free to use, modify, distribute, and perform the work, even for commercial purposes, without asking permission.

   ## Instructions

   1. Create a folder named `data` in the root directory and put `books_data.csv` and `Books_rating.csv` inside this folder

   2. Open MongoDB Compass and your Neo4j server

   3. Run `generateFormattedRatings.py`. This will create the file `Books_rating_refactored.csv` in the `data` directory

   4. Make the password to your Neo4j server `password` or go to `Neo4jModel` in `models.py` and change the password. Also make sure you have the GDS plugin installed

   5. Put `Books_rating_refactored.csv` into the `import` folder of your Neo4j server

   6. Run `populateMongo.py` and `populateNeo4j.py`

   7. Run `app.py` and go to `localhost:8888`

   8. If you wish to use the custom recommendations feature run the following queries on your Neo4j server:
   
   ```
   CALL gds.graph.project(
   'user-proj',
   ['User','Book'],
   {LIKES:{type: 'RATED',
      properties: {rating: {property: 'score'}}}
   });
   ```
   ```
   CALL gds.nodeSimilarity.mutate('user-proj', {relationshipWeightProperty: 'rating', similarityMetric: 'cosine',
    mutateRelationshipType: 'SIMILAR', mutateProperty: 'score'
   })
   ```
   ```
   CALL gds.graph.relationship.write( 'customer-proj',  'SIMILAR', 'score'  ) 
   YIELD graphName, relationshipType, relationshipProperty, relationshipsWritten, propertiesWritten
   ```
   The reason why this is not done for you is that calculating the cosine similarity between all the users takes about an hour.
