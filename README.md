[![FINOS - Incubating](https://cdn.jsdelivr.net/gh/finos/contrib-toolbox@master/images/badge-incubating.svg)](https://finosfoundation.atlassian.net/wiki/display/FINOS/Incubating)

# FINOS DTCC Hackathon 

### Disclaimer

This repository contains an experimental AI-powered KYC (Know Your Customer) agent developed as part of a hackathon project. It is intended solely as a technology showcase and does not represent or reflect any actual KYC processes, policies, or compliance requirements of any organization, financial institution, or regulatory body.

This project is provided as-is, without any warranties or guarantees regarding accuracy, security, or compliance with legal and regulatory frameworks. It should not be used in any production environment or relied upon for real-world identity verification or fraud prevention.

By using this repository, you acknowledge that:

This project is for demonstration and educational purposes only.
The authors, contributors, and maintainers are not responsible for any misuse, legal implications, or consequences arising from its use.
It is your responsibility to ensure compliance with applicable laws and regulations before implementing any KYC-related solutions.
For any concerns or inquiries, please refer to the repository's license terms and contribution guidelines.


<div align="center">

<div align="center">

## Project Name
# **AI KYC AGENT**
  
KYC Agent: Automate Routine work of KYC process

🔎 **AI KYC AGENT**: An innovative AI-powered KYC agent that streamlines KYC processes, reduces costs, and enhances compliance. The financial industry is increasingly reliant on Know Your Customer (KYC) processes to mitigate risk and comply with regulations. This provides an alernative to traditional KYC methods which are often manual, time-consuming, and prone to errors. 

</div>

### Table of contents 

- [Why AI KYC AGENT?](#why-kycai)
- [Getting Started](#getting-started)
- [Key Features](#key-features)
- [Understanding Flows and Crews](#understanding-flows-and-crews)
- [Examples](#examples)
- [How AI KYC AGENT Compares](#how-kycai-compares)
- [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
- [Contribution](#contribution)
- [Project Members](#project-members)
- [License](#license)

# Why AI KYC AGENT?

### Why Is KYC Important?
Know Your Customer (KYC) processes are essential in the financial industry to prevent fraud, money laundering, and other illicit activities. Regulatory compliance ensures that businesses operate within legal frameworks, protecting both institutions and customers from financial crimes.

### The Problem with Manual KYC
Traditional KYC methods rely heavily on manual reviews, which come with several challenges:
- Time-Consuming – Verifications often take days, delaying customer onboarding.
- High Costs – Labor-intensive processes lead to increased operational expenses.
- Error-Prone – Human oversight can result in inconsistencies, leading to compliance risks.
- Scalability Issues – As customer bases grow, manual processes struggle to keep up.

### How This Solves These Challenges
Our AI-powered KYC agent offers a smarter alternative by:
- ✅ Reducing Costs – Eliminating the need for extensive manual labor.
- ✅ Enhancing Compliance – Ensuring accuracy and adherence to regulatory requirements.
- ✅ Scaling Efficiently – Handling large volumes of customers without sacrificing quality.
- ✅ Automating Documentation Processing – Faster processing with real-time processing.

By leveraging advanced AI, this solution transforms KYC into a streamlined, cost-effective, and highly compliant process—empowering businesses to operate more efficiently in an increasingly regulated landscape.

# Getting started 
AI KYC AGENT has two flows which act as a comprehensive KYC Agent. The first flow is a KYC procedure Agent, to analyse Policy Documents via the KYC Procedure agent. The second flow to analyse Client Documentation via the KYC Ops Agent. 

### 1. Installation

Ensure you have Python >=3.10 <3.13 installed on your system. 

First, install .... :

```shell
pip install ...
```

### 2. Setting Up with the YAML Configuration

To create a new project, run the following CLI (Command Line Interface) command:

```shell
... 
```

This command creates a new project folder with the following structure:

```
my_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── my_project/
        ├── __init__.py
        ├── main.py
        ├── 
        ├── 
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```


### 3. Running Your AI KYC AGENT

Before running your crew, make sure you have the following keys set as environment variables in your `.env` file:

- ...
- ...

Lock the dependencies and install them by using the CLI command but first, navigate to your project directory:

```shell
cd ...
...
```


# Key features 



![KYC Agent Technical Flow](images/technical_flowchart.png)

# Examples 
A demo of the AI KYC AGENT use case is provided below:

# How AI KYC AGENT Compares
How does AI KYC AGENT compare to other KYC agents availible? 

# FAQ 


# Contribution
We welcome contributions to this project! Whether you're fixing a bug, adding a new feature, or improving the documentation, we appreciate your help in making this project better.

For detailed information on how the system is architected, how features are implemented, and the technologies used, please refer to the [TECHNICAL.md](./TECHNICAL.md) file. This file provides an in-depth look into the project’s structure, including explanations of key components, deployment instructions, and the overall technology stack. It also contains functional diagrams, feature requirements, and best practices for developing and maintaining the project.

If you’d like to contribute, we’ve outlined the process for submitting your changes in the [TECHNICAL.md](./TECHNICAL.md). It covers how to fork the repository, create new branches, and submit pull requests, along with our code review process. Before contributing, we recommend reviewing this document to familiarize yourself with the project’s technical setup and coding standards.

By referring to the [TECHNICAL.md](./TECHNICAL.md), you’ll have a clear understanding of how to make meaningful contributions to the project, ensuring consistency and alignment with the overall architecture and goals. Thank you for your interest, and we look forward to your contributions!

# Project Members 
Team members involved in the DTCC Hackathon with FINOS, resposible for the initial PoC of the AI KYC AGENT. 


**Team Member**     | **Title**              | **Resposible Topics**  
------------------  | ---------------------- | ------------------  
Maxim Romanovsky    | Team Lead              | All areas
Valeria Bladinieres | Fullstack Engineer     | RAG, Agent, Frontend CI/CD 
Haydn Griffith-Jones| Product Owner          | Product 
Matthew Barley      | ML Engineer            | Agent, RAG, Prompt Engineering
Somnath Pailwan     | Fullstack Engineer     | Frontend, Backend, CI/CD
Pulkit Khera        | ML Engineer            | Data pipelines, RAG, CI/CD
Elena Podgornova    | Fullstack Engineer     | Backend, Frontend, CI/CD
Nikolay Tolstokulakov | Infra Engineer       | CI/CD, Backend, RAG
Meeka Lenisa        | Data Scientist         | Product, Evaluation Framework, Prompt Engineering
Alessio Sordo       | ML Engineer            | Evaluation framework, Agent, Backend, Prompt Engineering


# License

Copyright 2025 FINOS

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)
