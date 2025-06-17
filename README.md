# Wildfire Detection Using Satellite Imagery

## Overview
This repository contains a complete open-source pipeline for detecting wildfires from Sentinel‑2 satellite imagery. The project introduces a publicly available dataset created by aligning NASA Fire Information for Resource Management System (FIRMS) alerts with Sentinel‑2 images. In addition to the dataset, the repository provides utilities for data preprocessing, visualization and model training.

## Dataset
- **Source**: Sentinel-2 imagery matched with NASA FIRMS fire alerts
- **Coverage**: Locations across Azerbaijan and additional global sites
- **Structure**: Processed image folders for training, validation and testing

This collection addresses the scarcity of labeled satellite images for wildfire research and enables reproducible experiments. Example code for preparing the data is included in the `lib` directory.

## Library
The accompanying Python modules offer tools for:
- Downloading and processing Sentinel‑2 imagery
- Preparing CSV files for visualization
- Training and fine‑tuning convolutional neural networks

These utilities can be imported as a library or used directly within the provided notebooks.

## Baseline Model
A reference model using transfer learning with popular CNN architectures is included. Training notebooks demonstrate how to fine‑tune these networks for wildfire detection and show strong detection performance.

## Project Website
Visualization examples, dataset and additional resources are available at [wildfireaze.github.io](https://wildfireaze.github.io). The website is driven by the CSV data generated in this repository.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/gunelaliyevaa/wildfire-detection-using-satellite-imagery
   ```
2. Follow the notebooks in the repository to preprocess data and train the model.
