## Evolutionary Computing Optimization
Project developed as final evaluation of 'Optimization and decision making using AI' course.
Multiobjective problem that aims to maximaze the minimal distance of pharmacies and minimize the minimal distance of hospitals given a geographic coverage.
NSGA-II was chosen as EC algorithm, using the folowing characteristics:
  - Chromosome: [float, float]
  - Evaluation: Haversine formula
  - Crossover: Simulated binary crossover that modify in-place the input individuals
  - Mutation: Gaussian distribution
  - Parent selection: Tournament selection based on dominance between two individuals
  - Next generation selection: NSGA-II selection operator on the individuals

  **Input:** Geographic location center (latitude, longitude) and radius (meters).

  **Model:** Gets the distance from the input location informed to all pharmacies and all hospitals of the indicated coverage and returns the minimum distances.

  **Output:** Latitudes and longitudes that provides the longest distance for pharmacies and the shortest distance to hospitals.
