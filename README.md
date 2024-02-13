# Project Name: GitBot - Your Intelligent Coding Assistant

## Welcome to GitBot!

GitBot is your ultimate coding companion, designed to streamline your development process, provide insightful assistance, and enhance your productivity. With GitBot, you have access to a range of powerful features that revolutionize the way you interact with code repositories, seek answers to coding queries, and collaborate with your team.

## Features

### 1. Clone and Index GitHub Repositories

Clone GitHub repositories effortlessly with just a few clicks. GitBot extracts text data from repository files, splits it into manageable chunks, and indexes it into a database for efficient analysis.

### 2. Intelligent Question-Answering System

GitBot features a state-of-the-art question-answering system powered by langchain's reACT agent supported by RAG system for the repositories codebase. Ask any coding-related question, and GitBot will provide accurate and insightful answers, leveraging its vast repository of knowledge.

### 3. Web Search and Error Resolution
Integrated inbuilt and custom built tools like Google search , Stack overflow search , repository retriever and repository-issues tool
Easily search the web for information related to your coding queries. GitBot seamlessly integrates with popular search engines and programming error databases to provide quick solutions to your coding dilemmas.

### 4. State-of-the-Art Language Models

GitBot utilizes cutting-edge open-source language models to deliver intelligent assistance. Leveraging the power of Mixtral 8x7b and Llama2-70b, GitBot offers unparalleled accuracy and efficiency in understanding and processing natural language queries.

### 5. Streamlit-Based Interactive Interface

Experience a user-friendly and intuitive interface with GitBot's Streamlit application. Interact with GitBot in real-time, receive instant responses to your queries, and explore the depths of your code repositories with ease.

## Getting Started

### Prerequisites

- Docker installed on your system

### Installation

1. Clone this repository to your local machine:
    ```
    git clone https://github.com/your_username/your_repository.git
    ```

2. Navigate to the project directory:
    ```
    cd your_repository
    ```

3. Create an environment file named `.env` in the root directory of your project and fill it with the following details:
    ```
    TOGETHER_API_KEY="your together api key"
    SERPAPI_API_KEY=" your serp api key"
    ASTRA_DB_APPLICATION_TOKEN=" your astra db application token"
    ASTRA_DB_API_ENDPOINT="your astra db api endpoint"
    ```


4. Run the Docker container:
    ```
    docker compose up
    ```

5. Access the GitBot Streamlit application at `http://localhost:8501` in your web browser.



