# latent-space-mol-search

**Project Status:** `Phase 1: Proof of Concept & Architecture Design (Active)`

## Overview
This repository contains the architectural blueprint and data engineering pipelines for a latent-space-mol=search design system. The objective is to transition from traditional discrete feature selection to a continuous-space generative model. 

By utilizing a Recurrent Variational Autoencoder (VAE), discrete chemical structures (SMILES strings) are mapped into a continuous latent space. A Genetic Algorithm (GA) then searches this multi-dimensional mathematical terrain to optimize molecular properties (e.g., QED, LogP) before decoding the vectors back into novel, optimized chemical structures.

## System Architecture
The pipeline is divided into three decoupled services: Data Engineering, Deep Learning, and Evolutionary Optimization.

```text
[Raw SMILES Data: ZINC/ChEMBL] 
       │
       ▼
[PySpark Ingestion Pipeline]  --> Filters length < 120, removes salts/duplicates, converts to Parquet.
       │
       ▼
[VAE Encoder (RNN/LSTM)]      --> Maps sequence tokens to Latent Distribution (μ, σ).
       │
       ▼
[Latent Space (z)]            <-- [Genetic Algorithm] searches continuous space via arithmetic crossover & Gaussian mutation.
       │
       ▼
[VAE Decoder (RNN/LSTM)]      --> Autoregressively reconstructs optimized SMILES strings.
       │
       ▼
[RDKit Validation]            --> Calculates fitness (drug-likeness, synthetic accessibility).
```
## Tech Stack
* **Data Engineering:** Python, PySpark, Parquet
* **Deep Learning:** PyTorch (Variational Autoencoder, Reparameterization Trick)
* **Cheminformatics:** RDKit (Molecular property scoring)
* **Optimization:** Custom Continuous Genetic Algorithm

## Current Project Phase
Given the massive scale of chemical datasets (e.g., ZINC15 contains millions of compounds), the current phase focuses on establishing a robust, distributed data preprocessing pipeline before provisioning GPU clusters for model training.

* **[Implemented]** PySpark ingestion logic and Parquet schema conversion.
* **[Implemented]** VAE Object-Oriented class stubs (Encoder, Reparameterization Layer, Decoder).
* **[Implemented]** Continuous GA mathematical operators (Arithmetic Crossover).
* **[Pending]** Distributed cluster execution on Google Cloud Dataproc.
* **[Pending]** VAE training loop (minimizing Reconstruction Loss + KL Divergence).

